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
        notch (int): The turnover notch position of the rotor.
        positing (int): The position of the rotor.
        ring_setting (int): The ring seting of the rotor.
    """
    wiring: str
    notch: int
    position: int
    ring_setting: int

    @staticmethod
    def to_letter(index: int) -> str:
        """Convert an index number to a corresponding letter in the alphabet.

        This works by adding the Ordinal of 'A' which is 65 plus the index of the letter, then converting that ordinal number into a readable character.

        Args:
            index (int): The index of the letter.
         
        Returns:
            str: The corresponding letter.
        """
        return chr(ord('A') + index)

    @staticmethod
    def to_index(letter: str) -> int:
        """Convert a letter to a corresponding index number from the alphabet.

        This works by subtracting the Ordinal of the inputted letter from the ordinal of 'A' which is 65 and that gives us the position of that letter in the alphabet.

        Args:
            letter (str): The letter.

        Returns:
            int: The corresponding index.
        """
        return ord(letter) - ord('A')

    def __init__(self, wiring: str, notch: str, position: int = 0, ring_setting: int = 0) -> None:
        self.wiring = wiring
        self.notch = (Rotor.to_index(notch) - ring_setting) % 26 # Index, calculate the notch position based on the Ring Setting and take the modulo of 26.
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

    def move(self, letter: str, backwards: bool = False) -> str:
        """Pass a letter through the rotor in the forward direction.

        Finds the index position of the inputted letter in the alphabet, then finds the letter in that same indexed position on the rotor wheel's wiring (also accounting for the rotor's rotation).

        Then the index position of that letter is found relative to the alphabet (again accounting for the rotor's rotation). 
        
        Finally, the letter on the alphabet which corresponds to that index is returned.

        Args:
            letter (str): The inputted letter to pass through the rotor.
            backwards (bool): Defaults to False. If True, backwards motion will happen instead of forwards.

        Returns:
            str: The resulting letter.
        """
        # Find index of inputted letter and add the position of the rotor
        index: int = Rotor.to_index(letter)
        index = (index + self.position - self.ring_setting) % 26

        if backwards:
            wired_letter: str = Rotor.to_letter(index)
            wired_index: int = self.wiring.index(wired_letter)
            wired_index = (wired_index - self.position + self.ring_setting) % 26

            # Convert index to a letter and return
            return Rotor.to_letter(wired_index)
        else:
            # Find encrypted letter on rotor coordinates and convert to machine coordinates
            wired_letter: str = self.wiring[index]
            wired_index: int = Rotor.to_index(wired_letter)
            wired_index = (wired_index - self.position + self.ring_setting) % 26

            # Convert index to a letter and return
            return Rotor.to_letter(wired_index)

    def get_position(self) -> int:
        """ Return the position of the rotor """
        return self.position

    def get_notch(self) -> int:
        """ Return the notch position """
        return self.notch
    
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