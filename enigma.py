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
VI: JPGVOUMFYQBENHZRDKASXLICTW, ZM
VII: NZJHGRCXMYSWBOUFAIVLPEKQDT ZM
VIII: FKQHTLXOCBJSPDZRAMEWNIUYGV, ZM

A: EJMZALYXVBWFCRQUONTSPIKHGD
B: YRUHQSLDPXNGOKMIEBFZCWVJAT
C: FVPJIAOYEDRZXWGCTKUQSBNMHL

====================================

"""
# ------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------

from components import *

# ------------------------------------------------------------------------
# Enigma Machine
# ------------------------------------------------------------------------
class EnigmaMachine:
    """The Enigma Machine, able to encrypt messages by passing letters 
    through a plugboard, rotors and a reflector.

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

    # --------------------------------------------------------------------
    # Run the Enigma
    # --------------------------------------------------------------------
    def run(self, plaintext: str) -> str:
        """Run the enigma machine.

        Encrypts the plaintext by iterating over each char in the plaintext.
        """
        plaintext = self.validate_plaintext(plaintext)
        ciphertext: list[str] = []
        for char in plaintext:
            ciphertext.append(self.encrypt(char))
        result: str = ''.join(ciphertext)

        # Add a whitespace every 5 characters.
        return ' '.join(result[i : i + 5] for i in range(0, len(result), 5))

    # --------------------------------------------------------------------
    # Encrypt for each Char
    # --------------------------------------------------------------------
    def encrypt(self, char: str) -> str:
        """Encrypt a char from plaintext

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
        for rotor in self.rotors:
            char = rotor.move(char)
        char = self.reflector.reflect(char)
        for rotor in reversed(self.rotors):
            char = rotor.move(char, backwards=True)
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
        middle_at_notch: bool = (
            self.rotors[1].get_position() 
            in self.rotors[1].get_notches()
        )

        right_at_notch: bool = (
            self.rotors[0].get_position() 
            in self.rotors[0].get_notches()
        )

        if middle_at_notch:
            self.rotors[2].rotate()

        if middle_at_notch or right_at_notch:
            self.rotors[1].rotate()
        
        self.rotors[0].rotate()

    # --------------------------------------------------------------------
    # Validate Plaintext
    # --------------------------------------------------------------------
    def validate_plaintext(self, plaintext: str) -> str:
        """Validate the plaintext 
        
        Args:
            plaintext (str): Plaintext to encrypt.
        
        Returns:
            str: The validated plaintext
        """
        plaintext = plaintext.upper().strip().replace(' ', '')
        return ''.join([char for char in plaintext if char.isalpha()])

    # --------------------------------------------------------------------
    # Set Rotor Selection
    # --------------------------------------------------------------------
    def set_rotors(self, rotors: str) -> None:
        """Select rotor configuration

        Set the rotor config and check they are all exist, are unique and 
        there's three selected.

        Args:
            rotors (str): The rotors selected

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
            'V': Rotor('VZBRGITYUPSDNHLXAWMJQOFECK', 'Z'),
            'VI': Rotor('JPGVOUMFYQBENHZRDKASXLICTW', 'ZM'),
            'VII': Rotor('NZJHGRCXMYSWBOUFAIVLPEKQDT', 'ZM'),
            'VIII': Rotor('FKQHTLXOCBJSPDZRAMEWNIUYGV', 'ZM'),
            'BETA': Rotor('LEYJVCNIXWPBQMDRTAKZGFUHOS', ''),
            'GAMMA': Rotor('FSOKANUERHMBTIYCWLQPZXVGJD', '')
        }

        all_rotors = ', '.join(available_rotors)

        rotors_list: list[str] = rotors.split()

        rotors_list.reverse()

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
                    f'Invalid rotor: {rotor} selected. Please select '
                    f'from {all_rotors}'
                )

            final_rotors.append(available_rotors[rotor])
            
        if len(final_rotors) < 3 or len(final_rotors) > 4: # Check there are three rotors
            raise ValueError('You must have 3-4 rotors specified only.')
        
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
            'BT': Reflector('ENKQAUYWJICOPBLMDXZVFTHRGS'),
            'C': Reflector('FVPJIAOYEDRZXWGCTKUQSBNMHL'),
            'CT': Reflector('RDOBJNTKVEHMLFCWZAXGYIPSUQ')
        }

        reflector = reflector.upper()
        reflectors = ', '.join(available_reflectors)

        if reflector not in available_reflectors: 
            # Given reflector doesn't exist
            raise ValueError(
                f'Argument {reflector} was not found in the list of'
                f' available reflectors. Choose from {reflectors}'
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
        elif len(setting) < 3 or len(setting) > 4:
            # Three characters are required, one for each rotor
            raise ValueError(
                f'Argument {setting} must be a length of 3-4 characters.'
            )
        else:
            setting = setting[::-1]

            for i, rotor in enumerate(self.rotors):
                rotor.set_window_setting(
                    Rotor.to_index(setting[i]) % 26
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
            raise ValueError(
                f'Argument {setting} must only contain alphabetical'
                ' characters.'
            ) # Invalid character (was not found in the alphabet)
        elif len(setting) < 3 or len(setting) > 4:
            raise ValueError(
                f'Argument {setting} must be a length of 3-4 characters.'
            ) # Three characters are required, one for each rotor
        else:
            setting = setting[::-1]

            for i, rotor in enumerate(self.rotors):
                rotor.set_ring_setting(
                    Rotor.to_index(setting[i]) % 26
                )

    # --------------------------------------------------------------------
    # Set Plugboard Swaps
    # --------------------------------------------------------------------
    def set_plugboard_swaps(self, swaps: str) -> None:
        self.plugboard_swaps.set_plugboard_swaps(swaps)

# ------------------------------------------------------------------------
# Main Function
# ------------------------------------------------------------------------
def main() -> None:
    # Settings
    settings = {
        'rotors': 'I II III',
        'reflector': 'B',
        'window_setting': 'AAA',
        'ring_setting': 'AAA',
        'plugboard_swaps': ''
    }

    plaintext = input('Your Message: ')

    enigma = EnigmaMachine(
        settings['rotors'], 
        settings['reflector'], 
        settings['window_setting'], 
        settings['ring_setting'], 
        settings['plugboard_swaps']
    )

    print(enigma.run(plaintext))

# ------------------------------------------------------------------------
# Main Routine
# ------------------------------------------------------------------------
if __name__ == '__main__':
    main()