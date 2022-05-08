#It's a Install Script.

import sqlite3
import os

if not os.path.exists('./Data') :
    os.makedirs('./Data')
if not os.path.isfile('./Data/Message.db'):
    NDB = sqlite3.connect('./Data/Message.db')
    cur = NDB.cursor()
    cur.execute(f'''
        Create table 
        message (
        MainID integer Primary Key,
        font text,
        sub_type text,
        message_id integer,
        message_type text,
        raw_message text,
        sender_age text,
        sender_nickname text,
        sender_sex text,
        sender_id integer,
        SubID text,
        target_id integer,
        self_id integer,
        time integer
        )''')
    cur.execute('insert into message values(NULL,?,?,?,?,?,?,?,?,?,?,?)', ('','message',1000,'group','installer','0','Installer','None',1000,'10001000',1000,1000,10000))
    cur.execute(f'''
        Create table 
        group_message (
        SubID text Primary Key,
        anonyous text,
        group_id int,
        sender_area text,
        sender_group_nickname text,
        sender_level text,
        sender_role text,
        sender_title text
        )''')
    cur.execute('insert into group_message values(?,?,?,?,?,?,?,?)', ('10001000','',1001,'','Installer','','owner','instal'))
    NDB.commit()
    NDB.close()