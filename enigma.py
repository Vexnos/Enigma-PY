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
#-------Libraries-------
from components import *
import json

#-------Classes|Methods-------
class EnigmaMachine:
    """The Enigma Machine, able to encrypt messages by passing letters through a plugboard and rotors.

    This is the main class of this project. It works by taking in the user's inputted attributes and encrypting their message accordingly.
    It also works with three other imported classes: Rotor, Reflector, and Plugboard.

    Attributes:
        message (str): The message to encrypt/decrypt
        rotors (list[Rotor]): The rotors to use (maximum of 3). It should be noted that the first rotor in the order is actually the last one in the list of rotors. While this may appear confusing, it's to maintain parity with other Enigma simulators and keep the visualisation simple.
        reflector (Reflector): The reflector to be used.
        window_settings (str): The initial position of the rotors.
        ring_settings (str): The ring settings of each rotor.
        plugboard_swaps (str): Letters to swap around during encryption.
    """
    message: str
    rotors: list[Rotor]
    reflector: Reflector
    window_settings: str
    ring_settings: str
    plugboard_swaps: Plugboard

    def __init__(self, message: str, rotors: str, reflector: str, window_settings: str, ring_settings: str, plugboard_swaps: str = '') -> None:
        self.set_message(message) # Remove whitespaces and set to uppercase.
        self.set_rotors(rotors)
        self.set_reflector(reflector)
        self.set_window_setting(window_settings)
        self.set_ring_setting(ring_settings)
        self.plugboard_swaps = Plugboard(plugboard_swaps)

        # Individual Rotors
        self.right_rotor: Rotor = self.rotors[2] # First rotor
        self.middle_rotor: Rotor = self.rotors[1]
        self.left_rotor: Rotor = self.rotors[0]

        # Window settings
        self.rotors[0].rotate(Rotor.to_index(self.window_settings[0]) % 26)
        self.rotors[1].rotate(Rotor.to_index(self.window_settings[1]) % 26)
        self.rotors[2].rotate(Rotor.to_index(self.window_settings[2]) % 26)

        # Ring settings
        self.rotors[0].set_ring_setting(Rotor.to_index(self.ring_settings[0]) % 26)
        self.rotors[1].set_ring_setting(Rotor.to_index(self.ring_settings[1]) % 26)
        self.rotors[2].set_ring_setting(Rotor.to_index(self.ring_settings[2]) % 26)

    def run(self) -> None:
        """Run the enigma machine.

        Encrypts the message by iterating over each char in the message.
        """
        encrypted_message: list[str] = []
        for char in self.message:
            encrypted_message.append(self.encrypt(char))
        result: str = ''.join(encrypted_message)
        print(' '.join(result[i : i + 5] for i in range(0, len(result), 5))) # Add a whitespace every 5 characters.

    def encrypt(self, char: str) -> str:
        """Encrypt a char from a message

        Takes the char and feeds it through a series of methods like the Enigma machine.
        unecrypted char -> plugboard -> rotor 1 (forwards) -> rotor 2 (forwards) -> rotor 3 (forwards) -> reflector -> rotor 3 (backwards) -> rotor 2 (backwards) -> rotor 1 (backwards) -> plugboard -> encrypted char

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

    def rotate_rotors(self) -> None:
        """Rotor rotation

        Rotates the right rotor each keypress. The middle rotor will rotate if the right rotor is at its notch, but also if the middle rotor is at its notch due to the double step anomaly which is implemented here. The left rotor will also rotate if the middle rotor is at its notch.
        """
        if self.middle_rotor.get_position() == self.middle_rotor.get_notch():
            self.left_rotor.rotate()
            self.middle_rotor.rotate() # Double stepping anomaly
        if self.right_rotor.get_position() == self.right_rotor.get_notch():
            self.middle_rotor.rotate()
        self.right_rotor.rotate()

    def set_message(self, message: str) -> None:
        """Set the message 
        
        Args:
            message (str): The message to encrypt.
        
        Returns:
            None

        Raises:
            ValueError: If message doesn't only contain alphabetical characters.
        """
        message = message.upper().strip().replace(' ', '')
        if not str.isalpha(message):
            raise ValueError(f'Argument {message} must only contain alphabetical characters.')
        self.message = message

    def set_rotors(self, rotors: str) -> None:
        """Select rotor configuration

        Set the rotor config if only 3 are selected, otherwise fail.

        Args:
            rotors (list[Rotor]): The rotors selected

        Returns:
            None

        Raises:
            ValueError: If there are not 3 selected rotors.
        """
        available_rotors: dict[str, Rotor] = {
            'I': Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q'),
            'II': Rotor('AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E'),
            'III': Rotor('BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V'),
            'IV': Rotor('ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J'),
            'V': Rotor('VZBRGITYUPSDNHLXAWMJQOFECK', 'Z')
        }

        rotors_list: list[str] = rotors.split()
        final_rotors: list[Rotor] = []

        for rotor in rotors_list:
            if rotor not in available_rotors:
                raise ValueError(f'Invalid rotor: {rotor} selected. Please try again')

            final_rotors.append(available_rotors[rotor])
            
        if len(final_rotors) != 3:
            raise ValueError('You must have 3 rotors specified only.')
        
        self.rotors = final_rotors

    def set_reflector(self, reflector: str) -> None:
        """ Set the reflector """
        available_reflectors: dict[str, Reflector] = {
            'A': Reflector('EJMZALYXVBWFCRQUONTSPIKHGD'),
            'B': Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT'),
            'C': Reflector('FVPJIAOYEDRZXWGCTKUQSBNMHL')
        }

        if len(reflector) != 1:
            raise ValueError(f'Argument {reflector} must be one character.')

        if reflector.upper() not in available_reflectors:
            raise ValueError(f'Argument {reflector} was not found in the list of available reflectors. Choose A, B, or C')

        self.reflector = available_reflectors[reflector]

    def set_window_setting(self, setting: str) -> None:
        """ Set the window setting """
        if not str.isalpha(setting):
            raise ValueError(f'Argument {setting} must only contain alphabetical characters.')
        elif len(setting) != 3:
            raise ValueError(f'Argument {setting} must be a length of 3 characters.')
        else:
            self.window_settings = setting

    def set_ring_setting(self, setting: str) -> None:
        """ Set the ring setting """
        if not str.isalpha(setting):
            raise ValueError(f'Argument {setting} must only contain alphabetical characters.')
        elif len(setting) != 3:
            raise ValueError(f'Argument {setting} must be a length of 3 characters.')
        else:
            self.ring_settings = setting

#-------Functions-------
def import_message(file_path: str) -> None:
    with open(f'messages/{file_path}', 'r') as file:
        contents: dict[str, str] = json.load(file)

def main() -> None:
    """ Main function """

    # Message
    message: str = input('Please enter your message: ')

    # Settings
    enigma = EnigmaMachine(message, 'III II I', 'B', 'AAA', 'AAA', '')
    enigma.run()

#-------Main-Routine-------
if __name__ == '__main__':
    main()