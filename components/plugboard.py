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
    plugboard_swaps: list[str]

    def __init__(self, plugboard_swaps: str) -> None:
        self.plugboard_swaps = plugboard_swaps.upper().split()

    def swap(self, char: str) -> str:
        if len(self.plugboard_swaps) == 0 or self.plugboard_swaps is None:
            return char
        
        swap: str | None = next((swap for swap in self.plugboard_swaps if char in swap), None)
        if swap is not None:
            pos: int = swap.index(char)
            return swap[1] if pos == 0 else swap[0]
        else:
            return char