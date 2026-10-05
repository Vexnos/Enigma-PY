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
    window_settings: str
    ring_settings: str

    def __init__(self, message: str, rotors: list[Rotor], reflector: Reflector, window_settings: str = 'AAA', ring_settings: str = 'AAA') -> None:
        self.message = message.strip().upper() # Remove whitespaces and set to uppercase.
        self.rotors = rotors
        self.reflector = reflector
        self.window_settings = window_settings
        self.ring_settings = ring_settings

    def run(self) -> None:
        for char in self.message:
            self.encrypt(char)

    def encrypt(self, char: str) -> None:
        ...

    def rotate_rotors(self) -> None:
        self.rotors[1].rotate()

#-------Functions-------


#-------Main-Routine-------
I = Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q')
II = Rotor('AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E')
III = Rotor('BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V')
# IV = Rotor('ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J')
# V = Rotor('VZBRGITYUPSDNHLXAWMJQOFECK', 'Z')

A = Reflector('EJMZALYXVBWFCRQUONTSPIKHGD')
B = Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT')
C = Reflector('FVPJIAOYEDRZXWGCTKUQSBNMHL')

enigma = EnigmaMachine('Hello', [I, II, III], B)

I.rotate()
letter = I.move('A')
print(letter)
letter = II.move(letter)
print(letter)
letter = III.move(letter)
print(letter)
letter = B.reflect(letter)
print(letter)
letter = III.move(letter, backwards=True)
print(letter)
letter = II.move(letter, backwards=True)
print(letter)
letter = I.move(letter, backwards=True)
print(letter)
