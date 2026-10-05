"""

===============================================
   file: rotor.py
project: Rotor Components of the Enigma Machine
 author: Vexnos
   date: 2026-10-03
===============================================

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
    notch: int
    position: int
    ring_setting: int

    def __init__(self, wiring: str, notch: str, position: int = 0, ring_setting: int = 0) -> None:
        self.wiring = wiring
        self.notch = ord(notch) - ord('A')
        self.position = position
        self.ring_setting = ring_setting

    def rotate(self, n: int = 1) -> None:
        """Rotate the rotor 
        
        Get the current rotor position, add the amount of times rotate and get the modulo of that from 26.
        This ensures the rotor can never turn higher than 26 because there are only 26 characters.
        
        Args:
            n (int): Amount of times to rotate

        Returns:
            None
        """
        self.position = (self.position + n) % 26 # Remainder of 26 to ensure the rotor loops around

    def set_ring_setting(self, ring_setting: int) -> None:
        """ Set the ring position for settings ONLY """
        self.ring_setting = ring_setting % 26 # Remainder of 26 to ensure the rotor loops around

    def forward(self, letter: str) -> str:
        """Pass a letter through the rotor in the forward direction.

        Finds the index position of the inputted letter on the alphabet, then returns the letter which is on the same index on the rotor wiring.

        Args:
            letter (str): The inputted letter to pass through the rotor.

        Returns:
            str: The resulting letter.
        """
        index: int = ord(letter) - ord('A')
        index = (index - self.position) % 26
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

class Reflector:
    """A reflector which reflects letters back into the rotors on the Enigma Machine.

    Attributes:
        wiring (str): The wiring of the reflector.
    """
    def __init__(self, wiring: str) -> None:
        self.wiring = wiring

    def reflect(self, letter: str) -> str:
        index: int = ord(letter) - ord('A')
        return self.wiring[index]