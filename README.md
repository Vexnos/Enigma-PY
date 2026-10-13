# Enigma Machine
This is an implementation of the Enigma M3 Machine in Python. It supports Rotors 1-8, Reflectors A-C, the Plugboard, and Ring Settings.

This implementation of the Enigma Machine prints the encryption key in the post 1940 format. The pre 1940 version is scheduled to be implemented at a later date.

You can either choose manual mode where you must set the settings of the machine in the `enigma.py` file. Or you can choose json mode where you can load your desired settings and messages from a json file. An example file is provided.

```json
{
    "daily_keys": "AAA BBB CCC DDD",
    "key": "HOCKEY",
    "rotors": "V IV II",
    "reflector": "B",
    "window_setting": "KEY",
    "ring_setting": "AAA",
    "plugboard_swaps": "",
    "plaintext": "Lorem Ipsum",
    "ciphertext": "HOC YIP | VPXH"
}
```

There is also a provided `codesheet.py` which will automatically generate a monthly codesheet for you and your friends. Once generated, you can use the `load_settings.py` to automatically load the day's settings in your json file.