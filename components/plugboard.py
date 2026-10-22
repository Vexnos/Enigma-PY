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
        plugboard_swaps (dict[str, str]): The list of swaps.
    """
    plugboard_swaps: dict[str, str]

    def __init__(self, plugboard_swaps: str) -> None:
        if self.has_no_duplicates(plugboard_swaps):
            self.only_two_chars(plugboard_swaps)
            self.set_plugboard_swaps(plugboard_swaps)
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
        return self.plugboard_swaps[char]

    # --------------------------------------------------------------------
    # Only two characters in a swap
    # --------------------------------------------------------------------
    def only_two_chars(self, swaps: str) -> None:
        """ Check if each plugboard swap has only two characters """
        for swap in swaps.split():
            if len(swap) != 2:
                raise ValueError(
                    f'Each plugboard swap can only contain two characters'
                )

    # --------------------------------------------------------------------
    # Set Plugboard Swaps
    # --------------------------------------------------------------------
    def set_plugboard_swaps(self, swaps: str) -> None:
        alphabet = {char: char for char in string.ascii_uppercase}
        
        for swap in swaps.upper().split():
            a, b = swap[0], swap[1]
            alphabet[a] = b
            alphabet[b] = a

        self.plugboard_swaps = alphabet