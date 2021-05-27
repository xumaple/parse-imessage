import sqlite3
import pandas as pd
import pwd
import os
from shutil import copyfile
from datetime import datetime

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
    for name in sorted(d.items(), key=lambda x: x[1])[-20:][::-1]:
        print(name)
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
