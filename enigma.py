"""

====================================
   file: enigma.py
project: Enigma Machine in Python
 author: Vexnos | Daniel Lagesse
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


#-------Classes|Methods-------
class Rotor:
    wiring: str
    notch: str

    def __init__(self, wiring: str, notch: str) -> None:
        self.wiring = wiring
        self.notch = notch

    def rotate(self) -> None:
        self.wiring = self.wiring[1:] + self.wiring[0]

    def forward(self, letter: str) -> str:
        index: int = ord(letter) - ord('A')
        return self.wiring[index]

    def backward(self, letter: str) -> str:
        index: int = self.wiring.index(letter)
        return chr(ord('A') + index)

class Reflector(Rotor):
    def __init__(self, wiring: str) -> None:
        self.wiring = wiring

    def reflect(self, letter: str) -> str:
        return super().forward(letter)

#-------Functions-------


#-------Main-Routine-------
I = Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q')
II = Rotor('AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E')
III = Rotor('BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V')
IV = Rotor('ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J')
V = Rotor('VZBRGITYUPSDNHLXAWMJQOFECK', 'Z')

A = Reflector('EJMZALYXVBWFCRQUONTSPIKHGD')
B = Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT')
C = Reflector('FVPJIAOYEDRZXWGCTKUQSBNMHL')

# II.rotate()
print(II.forward('A'))
print(II.backward('A'))