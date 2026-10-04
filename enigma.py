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


#-------Functions-------


#-------Main-Routine-------
I = Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q')
# II = Rotor('AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E')
# III = Rotor('BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V')
# IV = Rotor('ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J')
# V = Rotor('VZBRGITYUPSDNHLXAWMJQOFECK', 'Z')

A = Reflector('EJMZALYXVBWFCRQUONTSPIKHGD')
B = Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT')
C = Reflector('FVPJIAOYEDRZXWGCTKUQSBNMHL')

# I.rotate()
print(I.get_wiring())
print(I.forward('A'))
print(I.backward('E'))