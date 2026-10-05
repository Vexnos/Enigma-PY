"""

===================================================
   file: plugboard.py
project: Plugboard Components of the Enigma Machine
 author: Vexnos
   date: 2026-10-03
===================================================

"""
#-------Libraries-------


#-------Classes|Methods-------
class Plugboard:
    """A plugboard which can swap letters.

    This class handles the plugboard logic portion of the Enigma Machine. It will pass letters through and swap them with a counterpart according to user entered swaps.

    Attributes:
        plugboard_swaps (list[str]): The list of swaps.
    """
    plugboard_swaps: list[str]

    def __init__(self, plugboard_swaps: str) -> None:
        self.plugboard_swaps = plugboard_swaps.upper().split()

    def swap(self, char: str) -> str:
        """Swap the char if it matches a swap pair.

        Takes a char and checks it against user entered plugboard swaps. If one is found, find its position and return the swapped char.
        If no char is found, return itself so the rest of the encryption process can continue.

        Args:
            char (str): User inputted char

        Returns:
            str: Either the user inputted char or the swapped char
        """
        # Don't waste time calculating if there are no user defined plugboard swaps
        if len(self.plugboard_swaps) == 0 or self.plugboard_swaps is None:
            return char

        # Iterate over and find the first swap pair that char is in
        swap: str | None = next((swap for swap in self.plugboard_swaps if char in swap), None)
        if swap is not None: # Find its position in the pair and swap with the other position
            pos: int = swap.index(char) 
            return swap[1] if pos == 0 else swap[0]
        else: # A pair wasn't found, return the original char
            return char