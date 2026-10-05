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

#-------Classes|Methods-------
class EnigmaMachine:
    message: str
    rotors: list[Rotor]
    relfector: Reflector

    def __init__(self, message: str, rotors: list[Rotor], reflector: Reflector, window_settings: str = 'AAA', ring_settings: str = 'AAA', plugboard_swaps: str = '') -> None:
        self.message = message.upper().strip().replace(' ', '') # Remove whitespaces and set to uppercase.
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard_swaps = Plugboard(plugboard_swaps)

        # Individual Rotors
        self.right_rotor: Rotor = self.rotors[2] # First rotor
        self.middle_rotor: Rotor = self.rotors[1]
        self.left_rotor: Rotor = self.rotors[0]

        # Window settings
        self.rotors[0].rotate(Rotor.to_index(window_settings[0]) % 26)
        self.rotors[1].rotate(Rotor.to_index(window_settings[1]) % 26)
        self.rotors[2].rotate(Rotor.to_index(window_settings[2]) % 26)

        # Ring settings
        self.rotors[0].set_ring_setting(Rotor.to_index(ring_settings[0]) % 26)
        self.rotors[1].set_ring_setting(Rotor.to_index(ring_settings[1]) % 26)
        self.rotors[2].set_ring_setting(Rotor.to_index(ring_settings[2]) % 26)

    def run(self) -> None:
        encrypted_message: list[str] = []
        for char in self.message:
            encrypted_message.append(self.encrypt(char))
        print(''.join(encrypted_message))

    def encrypt(self, char: str) -> str:
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
        if self.middle_rotor.get_position() == self.middle_rotor.get_notch():
            self.left_rotor.rotate()
            self.middle_rotor.rotate() # Double stepping anomaly
            print('Rotating left rotor...')
        if self.right_rotor.get_position() == self.right_rotor.get_notch():
            print('Rotating middle rotor...')
            self.middle_rotor.rotate()
        self.right_rotor.rotate()
        print('Rotating right rotor...')

#-------Functions-------
def main() -> None:
    I = Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q')
    II = Rotor('AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E')
    III = Rotor('BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V')
    IV = Rotor('ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J')
    V = Rotor('VZBRGITYUPSDNHLXAWMJQOFECK', 'Z')

    A = Reflector('EJMZALYXVBWFCRQUONTSPIKHGD')
    B = Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT')
    C = Reflector('FVPJIAOYEDRZXWGCTKUQSBNMHL')

    message: str = input('Please enter your message: ')

    enigma = EnigmaMachine(message, [III, II, I], B, 'AAA', 'AAA', '')
    enigma.run()

#-------Main-Routine-------
if __name__ == '__main__':
    main()