"""

================================
   file: load_settings.py
project: Load Codesheet Settings
 author: Vexnos
   date: 2026-10-11
================================

"""
# ------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------
import json5
import csv
from datetime import date

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------
def import_csv(date: list[str], mode: int) -> dict:
    try:
        with open(f'codesheets/codesheet_{date[1]}_{date[0]}_M{mode}.csv', 'r') as file:
            contents = csv.DictReader(file)

            date_today = date.pop()
            if date_today[0] == '0':
                date_today = date_today.replace('0', '')

            datum_row = next(
                (row for row in contents if row['Datum'] == date_today),
                None
            )

            if datum_row is None:
                raise ValueError(
                    f'Date {date_today!r} returned nothing!'
                )
        return datum_row
    except FileNotFoundError:
        raise FileNotFoundError(
            f'Codesheet was not found. Year or Month must be invalid.'
        )

def import_json() -> dict:
    with open('messages/rotating.json5') as file:
        contents = json5.load(file)
    return contents

def export_json(contents: dict, date: list[str]) -> None:
    with open('messages/rotating.json5', 'w') as file:
        json5.dump(contents, file, indent=4)
    print(f'Settings loaded for {"-".join(date)}')

def main() -> None:
    datum: list[str] = str(date.today()).split('-')
    datum_settings = import_csv(datum, 3)

    json_settings = import_json()

    json_settings['daily_keys'] = datum_settings['Kenngruppen']
    json_settings['rotors'] = datum_settings['Walzenlage']
    json_settings['plugboard_swaps'] = datum_settings['Stockerverbindungen']
    json_settings['ring_setting'] = datum_settings['Ringstellung'].replace(' ', '')

    export_json(json_settings, datum)

# ------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------
if __name__ == '__main__':
    main()