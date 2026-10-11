"""

=============================
   file: codesheet.py
project: Codesheet Generation
 author: Vexnos
   date: 2026-10-11
=============================

"""
# ------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------
import string
from calendar import monthrange
from datetime import date
from random import sample, randint, shuffle
from rotor import Rotor

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------
def get_year_and_month() -> tuple[int, int]:
    """ Get the current year and month """
    today: list[str] = str(date.today()).split('-')
    return (int(today[0]), int(today[1]))

def to_letter(index: int) -> str:
    return Rotor.to_letter(index)

def gen_key() -> str:
    return ''.join([to_letter(randint(0, 25)) for _ in range(3)])

def main() -> None:
    """ Main function """
    year, month = get_year_and_month()

    days_in_month = monthrange(year, month)[1]

    available_rotors = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']

    contents = []

    contents.append('Datum,Walzenlage,Ringstellung,Stockerverbindungen,Kenngruppen')
    for day in range(1, days_in_month + 1):
        picked_rotors = sample(available_rotors, 3)

        ring_setting = [to_letter(randint(0, 25)) for _ in range(3)]

        alphabet = [char for char in string.ascii_uppercase]
        shuffle(alphabet)
        plugboard_swaps = [f'{alphabet[shift + 1]}{alphabet[shift + 2]}' for shift in range(1, 20, 2)]

        message_keys = [gen_key() for _ in range(4)]

        contents.append(f'{day},{" ".join(picked_rotors)},{" ".join(ring_setting)},{" ".join(plugboard_swaps)},{" ".join(message_keys)}')

    with open(f'codesheet_{month}_{year}.csv', 'w') as file:
        file.write('\n'.join(contents))

# ------------------------------------------------------------------------
# Main Routine
# ------------------------------------------------------------------------
if __name__ == '__main__':
    main()