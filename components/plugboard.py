"""

===================================================
   file: plugboard.py
project: Plugboard Components of the Enigma Machine
 author: Vexnos
   date: 2026-10-03
===================================================

"""

import string

# ------------------------------------------------------------------------
# Plugboard Class
# ------------------------------------------------------------------------
class Plugboard:
    """A plugboard which can swap letters.

    This class handles the plugboard logic portion of the Enigma Machine. 
    It will pass letters through and swap them with a counterpart 
    according to user entered swaps.

    Attributes:
        plugboard_swaps (list[str]): The list of swaps.
    """
    plugboard_swaps: list[str]

    def __init__(self, plugboard_swaps: str) -> None:
        if self.has_no_duplicates(plugboard_swaps):
            self.plugboard_swaps = plugboard_swaps.upper().split()
            self.only_two_chars()
        else:
            raise ValueError(
                f'Attribute {plugboard_swaps} cannot contain duplicates.'
            )

    # --------------------------------------------------------------------
    # No Duplicate Letters
    # --------------------------------------------------------------------
    def has_no_duplicates(self, swaps: str) -> bool:
        """ Check there are no duplicate letters in the defined swaps """
        swaps = swaps.replace(' ', '')
        return len(swaps) == len(set(swaps))

    # --------------------------------------------------------------------
    # Swap the letters
    # --------------------------------------------------------------------
    def swap(self, char: str) -> str:
        """Swap the char if it matches a swap pair.

        Takes a char and passes it through a dictionary of the alphabet
        where the keys are the alphabet and the values are the swapped
        alphabet.

        Args:
            char (str): User inputted char

        Returns:
            str: Either the user inputted char or the swapped char
        """
        alphabet = {char: char for char in string.ascii_uppercase}

        for swap in self.plugboard_swaps:
            a, b = swap[0], swap[1]
            alphabet[a] = b
            alphabet[b] = a

        return alphabet[char]

    # --------------------------------------------------------------------
    # Only two characters in a swap
    # --------------------------------------------------------------------
    def only_two_chars(self) -> None:
        """ Check if each plugboard swap has only two characters """
        for swap in self.plugboard_swaps:
            if len(swap) != 2:
                raise ValueError(
                    f'Attribute {self.plugboard_swaps}'
                    ' can only contain two characters for a swap.'
                )

    # --------------------------------------------------------------------
    # Set Plugboard Swaps
    # --------------------------------------------------------------------
    def set_plugboard_swaps(self, swaps: str) -> None:
        self.plugboard_swaps = swaps.upper().split()