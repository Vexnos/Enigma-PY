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
    """A rotor which can and encrypt letters in the same manner as the Enigma Machine

    This class manages the rotor portion of the Enigma Machine, it will pass letters through and encrypt them according to a rotor's wiring.
    It also manages turning the rotors, its ring-settings and window-settings.

    Attributes:
        wiring (str): The wiring of the rotor.
        notch (str): The turnover notch position of the rotor.
    """
    wiring: str
    notch: str

    def __init__(self, wiring: str, notch: str) -> None:
        self.wiring = wiring
        self.notch = notch

    def rotate(self) -> None:
        """ Rotates the rotor wiring by taking the first string and moving it to the end of the wiring. """
        self.wiring = self.wiring[1:] + self.wiring[0]

    def forward(self, letter: str) -> str:
        """Pass a letter through the rotor in the forward direction.

        Finds the index position of the inputted letter on the alphabet, then returns the letter which is on the same index on the rotor wiring.

        Args:
            letter (str): The inputted letter to pass through the rotor.

        Returns:
            str: The resulting letter.
        """
        index: int = ord(letter) - ord('A')
        return self.wiring[index]

    def backward(self, letter: str) -> str:
        """Pass a letter through the rotor in the inverse direction.

        Finds the index position of the inputted letter on the rotor, then returns the letter which is on the same index on the alphabet.

        Args:
            letter (str): The inputted letter to pass through the rotor.

        Returns:
            str: The resulting letter.
        """
        index: int = self.wiring.index(letter)
        return chr(ord('A') + index)
    
    def get_wiring(self) -> str:
        return self.wiring

class Reflector(Rotor):
    """A reflector which reflects letters back into the rotors on the Enigma Machine.

    This subclass extends the Rotor class to be used as a reflector since the logic is very similar.
    The turnover notch is not necessary for the reflector to work.

    Attributes:
        wiring (str): The wiring of the reflector.
    """
    def __init__(self, wiring: str) -> None:
        self.wiring = wiring

    def reflect(self, letter: str) -> str:
        """ Since reflect is the same logic as moving forward through a rotor, we can just re-use the method. """
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

# I.rotate()
print(I.get_wiring())
print(I.forward('A'))
print(I.backward('E'))