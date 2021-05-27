# Parse your iMessages

This is a Python 3 script used to parse and count the messages sent through iMessage, and stored in your MacBook's chat.db file. When run, it sorts and finds the conversations with the highest message counts, and prints the respective phone number along with converstaion message count for each.

## How to use:
```sh
$ python3 messages.py
18008889090: 48509
16006551111: 15190
...
13332221111: 10090
```

## Options

`-n` or `--number` flag: Configure how many phone numbers to include in the list. Default is set to 10.

Example:
```sh
$ python3 messages.py -n 20
```

`-c` or `--use_contacts` flag: Use the macOS Contacts API to find names (if they exist) in the AddressBook stored on the MacBook, and replace phone numbers with their respective Contact names, if found.

Example:
```
$ python3 messages.py -c
Will Treaty: 48509
Horace Altman: 15190
...
Halt O'Carrick: 10090
```

Note to use this flag - you must have the `pyobjc` package installed:
```sh
$ python3 messages.py -c   
Error: Contacts API not installed. run 'pip3 install pyobjc'
$ python3 -m pip pyobjc
$ python3 messages.py -c
```