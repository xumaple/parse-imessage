import sqlite3
import pandas as pd
import pwd
import os
from shutil import copyfile
from datetime import datetime
import argparse
import re

parser = argparse.ArgumentParser(description='Parse your messages')
parser.add_argument('--use_contacts', '-c', action='store_true')
useContacts = parser.parse_args().use_contacts
    

# make copy of database
db_path = pwd.getpwuid(os.getuid()).pw_dir + '/Library/Messages/chat.db'
new_db_path = os.path.dirname(os.path.realpath(__file__)) + '/chat.db-' + datetime.now().strftime('%Y%m-%d%H-%M%S')
# os.system('sudo cp {} {}'.format(db_path, new_db_path))
copyfile(db_path, new_db_path)

# connect to the database
conn = sqlite3.connect(new_db_path)
cur = conn.cursor()

# get the names of the tables in the database
# cur.execute(" select name from sqlite_master where type = 'table' ")
# cur.execute("pragma table_info(chat")
def call(s):
    cur.execute(s)
    options = set(cur.fetchall())
    d = {k[0]: k[1] for k in options}
    return d

def getPhoneNumber(s):
    s = re.sub(r'\W+', '', s)
    if len(s) == 10:
        s = '1'+s
    return s

def print_call(d, contacts):
    for name in sorted(d.items(), key=lambda x: x[1])[-20:][::-1]:
        k, v = name
        k = getPhoneNumber(k)
        if useContacts:
            k = contacts.get(k, k)
        print('{}: {}'.format(k, v))

# Source: https://github.com/ronaldoussoren/pyobjc/blob/master/pyobjc-framework-Contacts/Examples/print-contacts.py
def getContacts(d):
    if useContacts is None:
        return {}
    import Contacts

    def print_info(contact, stop):
        if contact.isKeyAvailable_(Contacts.CNContactGivenNameKey):
            for num in contact.phoneNumbers():
                name = contact.givenName()
                if contact.isKeyAvailable_(Contacts.CNContactFamilyNameKey) and contact.familyName() != '':
                    name += ' ' + contact.familyName()
                d[getPhoneNumber(num.value().stringValue())] = name

        else:
            print("Contact without phone number")
        return False
    fetchRequest = Contacts.CNContactFetchRequest.alloc().initWithKeysToFetch_(
        [Contacts.CNContactGivenNameKey, Contacts.CNContactFamilyNameKey, Contacts.CNContactPhoneNumbersKey]
    )

    store = Contacts.CNContactStore.alloc().init()
    ok, error = store.enumerateContactsWithFetchRequest_error_usingBlock_(
        fetchRequest, None, print_info
    )
    if not ok:
        print("Fetching contacts failed", error)
    return d


d = call(
"""
SELECT
    chat.chat_identifier,
    count(chat.chat_identifier) AS message_count
FROM
    chat
    JOIN chat_message_join ON chat. "ROWID" = chat_message_join.chat_id
    JOIN message ON chat_message_join.message_id = message. "ROWID"
GROUP BY
    chat.chat_identifier
ORDER BY
    message_count DESC;
"""
)
contacts = getContacts({})
print_call(d, contacts)
