"""

===============================================
   file: rotor.py
project: Rotor Components of the Enigma Machine
 author: Vexnos
   date: 2026-10-03
===============================================

"""
# ------------------------------------------------------------------------
# Rotor Class
# ------------------------------------------------------------------------
class Rotor:
    """A rotor which can encrypt letters in the same manner as the 
    Enigma Machine

    This class manages the rotor portion of the Enigma Machine.
    It will pass letters through and encrypt them according to a rotor's 
    wiring.

    It also manages turning the rotors, its ring-settings and 
    window-settings.

    Attributes:
        wiring (str): The wiring of the rotor.
        notch (int): The turnover notch position of the rotor.
        position (int): The position of the rotor.
        ring_setting (int): The ring seting of the rotor.
    """
    wiring: str
    notches: list[int]
    position: int
    ring_setting: int

    def __init__(
        self, 
        wiring: str, 
        notches: str, 
        position: int = 0, 
        ring_setting: int = 0
    ) -> None:
        self.wiring = wiring
        self.notches = [Rotor.to_index(notch) for notch in notches]
        self.position = position
        self.ring_setting = ring_setting

    # --------------------------------------------------------------------
    # Individual Rotor Logic
    # --------------------------------------------------------------------
    def rotate(self, n: int = 1) -> None:
        """Rotate the rotor 
        
        Get the current rotor position, add the amount of times to rotate
        and get that modulo 26.
        This ensures the rotor can never turn higher than 26 because there 
        are only 26 characters.
        
        Args:
            n (int): Amount of times to rotate

        Returns:
            None
        """
        self.position = (self.position + n) % 26

    # --------------------------------------------------------------------
    # Set Window Setting
    # --------------------------------------------------------------------
    def set_window_setting(self, window_setting: int) -> None:
        """ Set the window position for settings ONLY """
        self.position = window_setting

    # --------------------------------------------------------------------
    # Set Ring Setting
    # --------------------------------------------------------------------
    def set_ring_setting(self, ring_setting: int) -> None:
        """ Set the ring position for settings ONLY """
        self.ring_setting = ring_setting % 26

    # --------------------------------------------------------------------
    # Signal Moving through Rotor
    # --------------------------------------------------------------------
    def move(self, letter: str, backwards: bool = False) -> str:
        """Pass a letter through the rotor.

        Finds the index position of the inputted letter in the alphabet, 
        then finds the letter in that same indexed position on the rotor 
        wheel's wiring (also accounting for the rotor's rotation).

        However, that letter is relative to the rotor's internal 
        coordinates (internal wiring).
        So we return to the machine's coordinates (or wiring) by getting 
        the index of that letter relative to the alphabet and accounting 
        for the rotor's position.
        
        Finally, the letter on the alphabet which corresponds to that 
        index is returned.

        Args:
            letter (str): The inputted letter to pass through the rotor.
            backwards (bool): Defaults to False. 
            If True, backwards motion will happen instead of forwards.

        Returns:
            str: The resulting letter.
        """
        # Find index of inputted letter and add the position of the rotor
        index: int = Rotor.to_index(letter)
        index = (index + self.position - self.ring_setting) % 26

        if backwards:
            # Find encrypted letter on rotor coordinates (Inverse Wiring)
            wired_letter: str = Rotor.to_letter(index)
            wired_index: int = self.wiring.index(wired_letter)
        else:
            # Find encrypted letter on rotor coordinates (Forward Wiring)
            wired_letter: str = self.wiring[index]
            wired_index: int = Rotor.to_index(wired_letter)

        # Convert to machine coordinates
        wired_index = (wired_index - self.position + self.ring_setting) % 26

        # Convert index to a letter and return
        return Rotor.to_letter(wired_index)

    # --------------------------------------------------------------------
    # Get Rotor Position
    # --------------------------------------------------------------------
    def get_position(self) -> int:
        """ Return the position of the rotor """
        return self.position

    # --------------------------------------------------------------------
    # Get Notch Position
    # --------------------------------------------------------------------
    def get_notches(self) -> list[int]:
        """ Return notch positions """
        return self.notches

    # --------------------------------------------------------------------
    # Index to Letter
    # --------------------------------------------------------------------
    @staticmethod
    def to_letter(index: int) -> str:
        """Convert an index number to a corresponding letter in the 
        alphabet.

        This works by adding the Ordinal of 'A' which is 65 plus the 
        index of the letter, then converting that ordinal number into 
        a readable character.

        Args:
            index (int): The index of the letter.
            
        Returns:
            str: The corresponding letter.
        """
        return chr(ord('A') + index)

    # --------------------------------------------------------------------
    # Letter to Index
    # --------------------------------------------------------------------
    @staticmethod
    def to_index(letter: str) -> int:
        """Convert a letter to a corresponding index number from the 
        alphabet.

        This works by subtracting the Ordinal of the inputted letter from 
        the ordinal of 'A' which is 65 and that gives us the position of 
        that letter in the alphabet.

        Args:
            letter (str): The letter.

        Returns:
            int: The corresponding index.
        """
        return ord(letter) - ord('A')

# ------------------------------------------------------------------------
# Reflector Class
# ------------------------------------------------------------------------
class Reflector:
    """A reflector which reflects letters back into the rotors on the 
    Enigma Machine.

    Attributes:
        wiring (str): The wiring of the reflector.
    """
    def __init__(self, wiring: str) -> None:
        self.wiring = wiring

    def reflect(self, letter: str) -> str:
        index: int = ord(letter) - ord('A')
        return self.wiring[index]