"""
=================================
   file: interface.py
project: Enigma Machine in Python
 author: Vexnos
   date: 2026-10-13
=================================
"""
# ------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------

from enigma import EnigmaMachine
from time import strftime
from components.load_settings import import_csv
from datetime import date
import string
import random
import json5

# ------------------------------------------------------------------------
# Interface
# ------------------------------------------------------------------------
class Interface:
    """The Interface class for the Enigma machine

    This class acts as the interface for the enigma machine in enigma.py.
    It can load json files or encrypt from an input.

    If no file path is specified into plaintext_path, a message key will
    be automatically generated.

    Decryption will search through a codesheet by using the daily keys and
    load the settings for that day to decrypt a message.

    Attributes:
        enigma (EnigmaMachine): The loaded enigma machine
        plaintext_path (str): Path to plaintext json file
        plaintext (str): The plaintext
        key (str): Message key
        daily_keys (str): Daily Keys from a codesheet
        mode (int): The mode of the enigma machine (m3, or m4)
    """
    enigma: EnigmaMachine
    plaintext_path: str
    plaintext: str
    key: str
    daily_keys: str
    mode: int    

    def __init__(self, mode: str, plaintext_path: str = '') -> None:
        modes = {
            'M3': 3,
            'M4': 4
        }

        self.mode = modes[mode.upper()]

        self.plaintext_path = plaintext_path
        if len(self.plaintext_path) > 0:
            self.plaintext_info = self.import_plaintext(plaintext_path)
            self._json_init()
        else:
            self._norm_init()
            
    # --------------------------------------------------------------------
    # JSON Initialization
    # --------------------------------------------------------------------
    def _json_init(self) -> None:
        """ Initialize for JSON features """
        self.plaintext: str = self.plaintext_info['plaintext']
        self.key: str = self.validate_key(self.plaintext_info['key'])
        self.daily_keys: str = self.plaintext_info['daily_keys']

        self.enigma = EnigmaMachine(
            self.plaintext_info['rotors'], 
            self.plaintext_info['reflector'], 
            self.plaintext_info['window_setting'], 
            self.plaintext_info['ring_setting'], 
            self.plaintext_info['plugboard_swaps']
        )

    # --------------------------------------------------------------------
    # Normal Initialization
    # --------------------------------------------------------------------
    def _norm_init(self) -> None:
        """ Initialize normally (non-JSON features) """
        datum: list[str] = str(date.today()).split('-')
        datum_settings = import_csv(datum, self.mode)

        key_chars = [
            random.choice(string.ascii_uppercase) for _ in range(self.mode * 2)
        ]

        reflector: str = input('Reflector: ')

        self.plaintext = ''
        self.key = ''.join(key_chars)
        self.daily_keys = datum_settings['Kenngruppen']

        self.enigma = EnigmaMachine(
            datum_settings['Walzenlage'], 
            reflector, 
            'A' * self.mode, 
            datum_settings['Ringstellung'], 
            datum_settings['Stockerverbindungen']
        )

    # --------------------------------------------------------------------
    # Encrypt
    # --------------------------------------------------------------------
    def encrypt(self) -> None:
        """ Encrypt message """
        # If no plaintext path is specified, let the user input
        if len(self.plaintext) == 0:
            self.plaintext = input('Plaintext: ')

        midpoint = len(self.key) // 2 # Split the key in half
        key_start = self.key[:midpoint]
        key_end = self.key[midpoint:]

        # Window setting to first half of key
        self.enigma.set_window_setting(key_start)
    
        # Run the second half of the key through Enigma
        key_print: str = self.enigma.run(key_end)

        # Window setting to second half of key
        self.enigma.set_window_setting(key_end)

        creation_time = strftime('%H%M')

        # Randomly choose a daily key
        daily_key: str = self.set_daily_key(self.daily_keys)

        ciphertext: str = self.enigma.run(self.plaintext)
        ciphertext = ' '.join(ciphertext[i : i + 5] for i in range(0, len(ciphertext), 5))
        ciphertext = f'{daily_key} {creation_time} = {len(ciphertext.replace(" ", ""))} = {key_start} {key_print} | {ciphertext}'
    
        print(ciphertext)
        if len(self.plaintext_path) > 0:
            self.plaintext_info['ciphertext'] = ciphertext
            if input('Export? (y/n): ').lower().startswith('y'):
                self.export_ciphertext(
                    self.plaintext_path, 
                    self.plaintext_info
                )

    # --------------------------------------------------------------------
    # Decrypt
    # --------------------------------------------------------------------
    def decrypt(self) -> None:
        """ Decrypt message """
        # Year and month for codesheet
        year: str = input('Year: ')
        month: str = input('Month: ')

        ciphertext: str = input('Ciphertext: ')

        # Split into sections
        metadata, ciphertext = ciphertext.split(' | ')
        time, length, key = metadata.split(' = ')
        key, encrypted_key = key.split()

        # Find settings of the message's day
        settings = self.find_settings(time, year, month)
        self.enigma.set_rotors(settings['rotors'])
        self.enigma.set_ring_setting(settings['ring_setting'])
        self.enigma.set_plugboard_swaps(settings['plugboard_swaps'])

        # Find raw key and decrypt
        self.enigma.set_window_setting(key)
        raw_key = self.enigma.run(encrypted_key)
        self.enigma.set_window_setting(raw_key)
        plaintext = self.enigma.run(ciphertext)

        print(f'{time} = {length} = {key} {raw_key} | {plaintext}')

    # --------------------------------------------------------------------
    # Import Message from JSON
    # --------------------------------------------------------------------
    def import_plaintext(self, file_path: str) -> dict[str, str]:
        """ Import a message from a JSON file """
        with open(f'messages/{file_path}.json5', 'r') as file:
            contents: dict[str, str] = json5.load(file)
        return contents

    # --------------------------------------------------------------------
    # Export Message to JSON
    # --------------------------------------------------------------------
    def export_ciphertext(self, file_path: str, contents: dict) -> None:
        """ Export ciphertext to json """
        with open(f'messages/{file_path}.json5', 'w') as file:
            json5.dump(contents, file, indent=4)
            print(f'Exported to {file_path}')

    # --------------------------------------------------------------------
    # Validate Key from JSON
    # --------------------------------------------------------------------
    def validate_key(self, key: str) -> str:
        """Validate the message decryption key

        Validates the key, fails if key is invalid. If a key is not 
        specified a random one will be generated.
        
        Args:
            key (str): The key to validate
        
        Returns:
            str: if key is valid or a random key was generated

        Raises:
            ValueError: If non-alphabetical characters are entered or key
            length is not 6 or 8 (support for M4)
        """
        key = key.upper().strip()
        if len(key) == 6 or len(key) == 8:
            if not key.isalpha():
                raise ValueError(
                    f'Argument {key} must only contain alphabetical characters.'
                )
        elif len(key) == 0:
            # Generate a key automatically if one is not specified
            key_chars = [random.choice(string.ascii_uppercase) for _ in range(6)]
            key = ''.join(key_chars)
        else:
            raise ValueError(
                f'Argument {key} must contain 6 or 8 characters.'
            )
        return key

    # --------------------------------------------------------------------
    # Set Daily Key
    # --------------------------------------------------------------------
    def set_daily_key(self, daily_keys: str) -> str:
        """Select a daily key and append two random letters
        
        Args:
            daily_keys (str): The four keys for the day

        Returns:
            str: The chosen key
        """
        key: str = random.choice(daily_keys.split())
        combo = ['#', '@', '$']
        random.shuffle(combo)
        combo = ''.join(combo)
        combo = combo.replace('#', key)
        combo = combo.replace('@', random.choice(string.ascii_uppercase))
        combo = combo.replace('$', random.choice(string.ascii_uppercase))
        return combo

    # --------------------------------------------------------------------
    # Reverse find Daily Key
    # --------------------------------------------------------------------
    def find_daily_key(self, days: list, day_key: str) -> list:
        """Find the daily key in the codesheet.

        Tries to find the daily key in the specified codesheet.
        If one is not found, fail.

        If it succeeds, return the day's settings.

        Args:
            days (list): List of days and their information
            day_key (str): The daily key

        Returns:
            list: The settings of the day

        Raises:
            ValueError: If no day matching the key is found.
        """
        for day in days:
            keys = day[-1].split()
            for key in keys:
                if key in day_key:
                    return day
        else:
            raise ValueError(
                f'The key {day_key} was not found in the codesheet.'
                ' Please try specifying another codesheet.')

    # --------------------------------------------------------------------
    # Get Key Settings
    # --------------------------------------------------------------------
    def find_settings(self, time: str, year: str, month: str) -> dict:
        """Get the settings of the daily key

        Finds the enigma settings of the daily key in a specified
        codesheet.

        Args:
            time (str): The time of the message creation
            year (str): The year of the codesheet
            month (str): The month of the codesheet

        Returns:
            dict: The enigma settings of that day
        """
        day_key = time.split()[0]

        if len(year) == 0 or len(month) == 0:
            datum = str(date.today()).split('-')
            year = datum[0] # Datum is the german word for date
            month = datum[1]

        with open(f'codesheets/codesheet_{month}_{year}_M{self.mode}.csv', 'r') as file:
            contents = file.readlines()
        contents.remove(contents[0])
        days = [item.strip('\n').split(',') for item in contents]
        
        day: list = self.find_daily_key(days, day_key)

        return {
            'rotors': day[1],
            'ring_setting': day[2].replace(' ', ''),
            'plugboard_swaps': day[3],
        }

# ------------------------------------------------------------------------
# Main Function
# ------------------------------------------------------------------------
def main() -> None:
    """ Main function """
    mode = input('Mode: ')
    interface = Interface(mode)

    if input('Decrypt? (y/N): ').lower().startswith('y'):
        interface.decrypt()
    else:    
        interface.encrypt()

# ------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------
if __name__ == '__main__':
    main()