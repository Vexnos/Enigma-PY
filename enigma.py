"""

====================================
   file: enigma.py
project: Enigma Machine in Python
 author: Vexnos
   date: 2026-10-03
====================================
   
ALPHABET: ABCDEFGHIJKLMNOPQRSTUVWXYZ

I: EKMFLGDQVZNTOWYHXUSPAIBRCJ, Q
II: AJDKSIRUXBLHWTMCQGZNPYFVOE, E
III: BDFHJLCPRTXVZNYEIWGAKMUSQO, V
IV: ESOVPZJAYQUIRHXLNFTGKDCMWB, J
V: VZBRGITYUPSDNHLXAWMJQOFECK, Z

A: EJMZALYXVBWFCRQUONTSPIKHGD
B: YRUHQSLDPXNGOKMIEBFZCWVJAT
C: FVPJIAOYEDRZXWGCTKUQSBNMHL

====================================

"""
# ------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------

from components import *
import json

# ------------------------------------------------------------------------
# Enigma Machine
# ------------------------------------------------------------------------
class EnigmaMachine:
    """The Enigma Machine, able to encrypt messages by passing letters 
    through a plugboard and rotors.

    This is the main class of this project. 
    It works by taking in the user's inputted attributes and encrypting 
    their message accordingly.
    It also works with three other imported classes: Rotor, Reflector, 
    and Plugboard.

    It should be noted that the first rotor in the order is actually 
    the last one in the list of rotors. 
    While this may appear confusing, it's to maintain parity with other 
    Enigma simulators and keep the visualisation simple.

    Attributes:
        rotors (list[Rotor]): The rotors to use (maximum of 3). 
        reflector (Reflector): The reflector to be used.
        window_settings (str): The initial position of the rotors.
        ring_settings (str): The ring settings of each rotor.
        plugboard_swaps (str): Letters to swap around during encryption.
    """
    rotors: list[Rotor]
    reflector: Reflector
    window_settings: str
    ring_settings: str
    plugboard_swaps: Plugboard

    def __init__(
        self, 
        rotors: str, 
        reflector: str, 
        window_settings: str, 
        ring_settings: str, 
        plugboard_swaps: str = ''
    ) -> None:
        self.set_rotors(rotors)
        self.set_reflector(reflector)
        self.set_window_setting(window_settings)
        self.set_ring_setting(ring_settings)
        self.plugboard_swaps = Plugboard(plugboard_swaps)

        # Individual Rotors
        self.right_rotor: Rotor = self.rotors[2] # First rotor
        self.middle_rotor: Rotor = self.rotors[1]
        self.left_rotor: Rotor = self.rotors[0]

        # Ring settings
        self.rotors[0].set_ring_setting(
            Rotor.to_index(self.ring_settings[0]) % 26
        )
        self.rotors[1].set_ring_setting(
            Rotor.to_index(self.ring_settings[1]) % 26
        )
        self.rotors[2].set_ring_setting(
            Rotor.to_index(self.ring_settings[2]) % 26
        )

    # --------------------------------------------------------------------
    # Run the Enigma
    # --------------------------------------------------------------------
    def run(self, message: str) -> str:
        """Run the enigma machine.

        Encrypts the message by iterating over each char in the message.
        """
        message = self.validate_message(message)
        encrypted_message: list[str] = []
        for char in message:
            encrypted_message.append(self.encrypt(char))
        result: str = ''.join(encrypted_message)

        # Add a whitespace every 5 characters.
        return ' '.join(result[i : i + 5] for i in range(0, len(result), 5))

    # --------------------------------------------------------------------
    # Encrypt for each Char
    # --------------------------------------------------------------------
    def encrypt(self, char: str) -> str:
        """Encrypt a char from a message

        Takes the char and feeds it through a series of methods like the 
        Enigma machine.

        Process: 
        unecrypted char -> plugboard -> rotor 1 (forwards) -> 
        rotor 2 (forwards) -> rotor 3 (forwards) -> reflector -> 
        rotor 3 (backwards) -> rotor 2 (backwards) -> rotor 1 (backwards) 
        -> plugboard -> encrypted char

        Args:
            char (str): The char to encrypt

        Returns:
            str: The encrypted char
        """
        self.rotate_rotors()
        char = self.plugboard_swaps.swap(char)
        char = self.right_rotor.move(char)
        char = self.middle_rotor.move(char)
        char = self.left_rotor.move(char)
        char = self.reflector.reflect(char)
        char = self.left_rotor.move(char, backwards=True)
        char = self.middle_rotor.move(char, backwards=True)
        char = self.right_rotor.move(char, backwards=True)
        char = self.plugboard_swaps.swap(char)
        return char

    # --------------------------------------------------------------------
    # Rotate rotors in tandem with Rotor class
    # --------------------------------------------------------------------
    def rotate_rotors(self) -> None:
        """Rotor rotation

        Rotates the right rotor each keypress. 

        The middle rotor will rotate if the right rotor is at its notch, 
        but also if the middle rotor is at its notch due to the double 
        step anomaly which is implemented here. 

        The left rotor will also rotate if the middle rotor is at
        its notch.
        """
        if (
            self.middle_rotor.get_position() 
            == self.middle_rotor.get_notch()
        ):
            self.left_rotor.rotate()
            self.middle_rotor.rotate() # Double stepping anomaly
        if (
            self.right_rotor.get_position() 
            == self.right_rotor.get_notch()
        ):
            self.middle_rotor.rotate()
        self.right_rotor.rotate()

    # --------------------------------------------------------------------
    # Validate Message
    # --------------------------------------------------------------------
    def validate_message(self, message: str) -> str:
        """Validate the message 
        
        Args:
            message (str): The message to encrypt.
        
        Returns:
            str: The validated message
        """
        message = message.upper().strip().replace(' ', '')
        return ''.join([char for char in message if char.isalpha()])

    # --------------------------------------------------------------------
    # Set Rotor Selection
    # --------------------------------------------------------------------
    def set_rotors(self, rotors: str) -> None:
        """Select rotor configuration

        Set the rotor config and check they are all exist, are unique and 
        there's three selected.

        Args:
            rotors (list[Rotor]): The rotors selected

        Returns:
            None

        Raises:
            ValueError: If there are not 3 selected rotors; if a selected 
            rotor doesn't exist; or if a rotor duplicate is selected.
        """
        available_rotors: dict[str, Rotor] = {
            'I': Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q'),
            'II': Rotor('AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E'),
            'III': Rotor('BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V'),
            'IV': Rotor('ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J'),
            'V': Rotor('VZBRGITYUPSDNHLXAWMJQOFECK', 'Z')
        }

        rotors_list: list[str] = rotors.split()

        # Make a new list to append Rotor objects to
        final_rotors: list[Rotor] = []

        # Check all rotors are unique
        if len(rotors_list) != len(set(rotors_list)):
            raise ValueError(
                'There is a duplicate rotor selected. '
                'Please only select a rotor once.'
            )

        for rotor in rotors_list:
            # Validate selected rotor exists and translate to rotor object
            if rotor not in available_rotors:
                raise ValueError(
                    f'Invalid rotor: {rotor} selected. Please try again'
                )

            final_rotors.append(available_rotors[rotor])
            
        if len(final_rotors) != 3: # Check there are three rotors
            raise ValueError('You must have 3 rotors specified only.')
        
        self.rotors = final_rotors

    # --------------------------------------------------------------------
    # Set the Reflector
    # --------------------------------------------------------------------
    def set_reflector(self, reflector: str) -> None:
        """Set the reflector

        Set the reflector unless there is no reflector selected; or the 
        reflector doesn't exist.

        Args:
            reflector (str): The reflector as a string

        Returns:
            None

        Raises:
            ValueError: If the reflector string is empty or the character 
            is invalid.
        """
        available_reflectors: dict[str, Reflector] = {
            'A': Reflector('EJMZALYXVBWFCRQUONTSPIKHGD'),
            'B': Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT'),
            'C': Reflector('FVPJIAOYEDRZXWGCTKUQSBNMHL')
        }

        reflector = reflector.upper()

        if len(reflector) != 1:
            # A character was not given, either a whitespace or a number.
            raise ValueError(
                f'Argument {reflector} must be one character.'
            )

        if reflector not in available_reflectors: 
            # Given reflector doesn't exist
            raise ValueError(
                f'Argument {reflector} was not found in the list of'
                ' available reflectors. Choose A, B, or C'
            )

        self.reflector = available_reflectors[reflector]

    # --------------------------------------------------------------------
    # Set Window Setting
    # --------------------------------------------------------------------
    def set_window_setting(self, setting: str) -> None:
        """Set the window setting

        Validate the inputted window settings. 
        Return a ValueError if invalid.
        
        Args:
            setting (str): The given settings for each rotor
        
        Returns:
            None

        Raises:
            ValueError: If there are not three settings present for each 
            rotor; or the input did not contain alphabetical characters
        """
        setting = setting.upper().replace(' ','').strip()
        if not setting.isalpha():
            # Invalid character (was not found in the alphabet)
            raise ValueError(
                f'Argument {setting} must only contain alphabetical '
                'characters.'
            )
        elif len(setting) != 3:
            # Three characters are required, one for each rotor
            raise ValueError(
                f'Argument {setting} must be a length of 3 '
                'characters.'
            ) 
        else:
            self.window_settings = setting

            # Window settings
            self.rotors[0].set_window_setting(
                Rotor.to_index(self.window_settings[0]) % 26
            )
            self.rotors[1].set_window_setting(
                Rotor.to_index(self.window_settings[1]) % 26
            )
            self.rotors[2].set_window_setting(
                Rotor.to_index(self.window_settings[2]) % 26
            )

    # --------------------------------------------------------------------
    # Set Ring Setting
    # --------------------------------------------------------------------
    def set_ring_setting(self, setting: str) -> None:
        """Set the ring setting
        
        Validate the inputted ring settings. Return a ValueError if 
        invalid.
        
        Args:
            setting (str): The given settings for each rotor
        
        Returns:
            None

        Raises:
            ValueError: If there are not three settings present for each 
            rotor; or the input did not contain alphabetical characters
        """
        setting = setting.upper().replace(' ','').strip()
        if not setting.isalpha():
            raise ValueError(f'Argument {setting} must only contain alphabetical characters.') # Invalid character (was not found in the alphabet)
        elif len(setting) != 3:
            raise ValueError(f'Argument {setting} must be a length of 3 characters.') # Three characters are required, one for each rotor
        else:
            self.ring_settings = setting

# ------------------------------------------------------------------------
# Import Message from JSON
# ------------------------------------------------------------------------
def import_message(file_path: str) -> dict[str, str]:
    """ Import a message from a JSON file """
    with open(f'messages/{file_path}.json', 'r') as file:
        contents: dict[str, str] = json.load(file)
    return contents

# ------------------------------------------------------------------------
# Validate Key from JSON
# ------------------------------------------------------------------------
def validate_key(key: str) -> None:
    """ Validate the message decryption key """
    key = key.upper().strip()
    if not key.isalpha():
        raise ValueError(
            f'Argument {key} must only contain alphabetical characters.'
        )
    if len(key) != 6:
        raise ValueError(f'Argument {key} must contain 6 characters.')

# ------------------------------------------------------------------------
# Main Function
# ------------------------------------------------------------------------
def main(json_mode: bool = False) -> None:
    """ Main function """
    if not json_mode:
        # Settings
        rotors: str = 'I II III'
        reflector: str = 'B'
        window_setting: str = 'AAA'
        ring_setting: str = 'AAA'
        plugboard_swaps: str = ''

        message = input('Your Message: ')
    else:
        message_info = import_message('template')
        validate_key(message_info['key'])

        message: str = message_info['message']
        key: str = message_info['key']
        rotors: str = message_info['rotors']
        reflector: str = message_info['reflector']
        window_setting: str = message_info['window_setting']
        ring_setting: str = message_info['ring_setting']
        plugboard_swaps: str = message_info['plugboard_swaps']

    enigma = EnigmaMachine(
        rotors, 
        reflector, 
        window_setting, 
        ring_setting, 
        plugboard_swaps
    )

    if json_mode:
        # Window setting to first half of key
        enigma.set_window_setting(key[0:3])

        # Run the second half of the key through Enigma
        key_print: str = enigma.run(key[3:6])

        # Rotate to the raw second half of key
        enigma.set_window_setting(key[3:6])

        # Print the keys
        print(f'{key[0:3]}\n{key_print}')

    print(enigma.run(message)) # Run the message through

# ------------------------------------------------------------------------
# Main Routine
# ------------------------------------------------------------------------
if __name__ == '__main__':
    main(json_mode=False)