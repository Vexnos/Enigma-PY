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
import components.load_settings
import string
import random
import json

# ------------------------------------------------------------------------
# Interface
# ------------------------------------------------------------------------
class Interface:
    enigma: EnigmaMachine
    plaintext_path: str
    plaintext: str
    key: str
    daily_keys: str

    def __init__(self, plaintext_path: str) -> None:
        self.plaintext_path = plaintext_path
        self.plaintext_info = self.import_plaintext(plaintext_path)
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
    # Encrypt
    # --------------------------------------------------------------------
    def encrypt(self) -> None:
        # Window setting to first half of key
        self.enigma.set_window_setting(self.key[0:3])
    
        # Run the second half of the key through Enigma
        key_print: str = self.enigma.run(self.key[3:6])

        self.enigma.set_window_setting(self.key[3:6])

        creation_time = strftime('%H%M')
        
        daily_key: str = self.set_daily_key(self.daily_keys)
    
        ciphertext: str = self.enigma.run(self.plaintext)
        ciphertext = f'{daily_key} {creation_time} = {len(ciphertext.replace(" ", ""))} = {self.key[0:3]} {key_print} | {ciphertext}'
    
        self.plaintext_info['ciphertext'] = ciphertext
        print(ciphertext)
        if input('Export? (y/n): ').lower().startswith('y'):
            self.export_ciphertext(
                self.plaintext_path, 
                self.plaintext_info
            )

    # --------------------------------------------------------------------
    # Decrypt
    # --------------------------------------------------------------------
    def decrypt(self) -> None:
        ciphertext: str = input('Ciphertext: ')

        metadata, ciphertext = ciphertext.split(' | ')
        time, length, key = metadata.split(' = ')
        key, encrypted_key = key.split()

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
        with open(f'messages/{file_path}.json', 'r') as file:
            contents: dict[str, str] = json.load(file)
        return contents

    # --------------------------------------------------------------------
    # Export Message to JSON
    # --------------------------------------------------------------------
    def export_ciphertext(self, file_path: str, contents: dict) -> None:
        """ Export ciphertext to json """
        with open(f'messages/{file_path}.json', 'w') as file:
            json.dump(contents, file, indent=4)
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
            length is not 6
        """
        key = key.upper().strip()
        if len(key) == 6:
            if not key.isalpha():
                raise ValueError(
                    f'Argument {key} must only contain alphabetical characters.'
                )
        elif len(key) == 0:
            # Generate a key automatically if one is not specified
            key_chars = [random.choice(string.ascii_uppercase) for _ in range(6)]
            key = ''.join(key_chars)
        else:
            raise ValueError(f'Argument {key} must contain 6 characters.')
        return key

    # --------------------------------------------------------------------
    # Set Daily Key
    # --------------------------------------------------------------------
    def set_daily_key(self, daily_keys: str) -> str:
        """ Select a daily key and append two random letters """
        key: str = random.choice(daily_keys.split())
        combo = ['#', '@', '$']
        random.shuffle(combo)
        combo = ''.join(combo)
        combo = combo.replace('#', key)
        combo = combo.replace('@', random.choice(string.ascii_uppercase))
        combo = combo.replace('$', random.choice(string.ascii_uppercase))
        return combo

# ------------------------------------------------------------------------
# Main Function
# ------------------------------------------------------------------------
def main() -> None:
    """ Main function """
    components.load_settings.main()
    interface = Interface('rotating')

    if input('Decrypt? (y/N): ').lower().startswith('y'):
        interface.decrypt()
    else:    
        interface.encrypt()

# ------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------
if __name__ == '__main__':
    main()