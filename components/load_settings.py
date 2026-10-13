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
import json
import csv
from datetime import date

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------
def import_csv(date: list[str]) -> dict:
    with open(f'codesheet_{date[1]}_{date[0]}.csv', 'r') as file:
        contents = csv.DictReader(file)

        datum_row = next(
            (row for row in contents if row['Datum'] == date[2])
        )
    return datum_row

def import_json() -> dict:
    with open('messages/rotating.json') as file:
        contents = json.load(file)
    return contents

def export_json(contents: dict, date: list[str]) -> None:
    with open('messages/rotating.json', 'w') as file:
        json.dump(contents, file, indent=4)
    print(f'Settings loaded for {"-".join(date)}')

def main() -> None:
    datum: list[str] = str(date.today()).split('-')
    datum_settings = import_csv(datum)

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