import sqlite3
from sqlite3 import Error
import datetime

class DB:

    def __init__(self, dbname='appdata.sqlite'):
        self.dbname = dbname
        self.data_def = \
            'create table if not exists data ' + \
            '( id INTEGER PRIMARY KEY NOT NULL,' + \
            ' ip TEXT, name TEXT, location TEXT, ' + \
            ' temperature FLOAT, ' + \
            ' ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL) '

        self.most_recent_def = \
            'create table if not exists recent ' + \
            '( id INTEGER PRIMARY KEY NOT NULL,' + \
            ' ip TEXT, name TEXT, location TEXT, ' + \
            ' temperature FLOAT, ' + \
            ' ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL) '


    def save_record(self, record):
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()

        cur.execute(self.data_def)
        cmd = 'insert into data (ip, name, location, temperature) values ( ?, ?, ?, ? )'
        cur.execute(cmd, ( record['ip'], record['name'], record['location'], record['temperature'] ) )
        conn.commit()
        cur.close()

    def save_most_recent(self, record):
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()

        cur.execute(self.most_recent_def)
        conn.commit()

        cmd = "delete from recent where ip = '{}' ".format( record['ip'])
        cur.execute(cmd)
        conn.commit()

        cmd = 'insert into recent (ip, name, location, temperature) values ( ?, ?, ?, ? )'
        cur.execute(cmd, (record['ip'], record['name'], record['location'], record['temperature']))
        conn.commit()
        cur.close()


    def timestamp(self):
        ts = datetime.datetime.now().timestamp()
        return ts

    def close(self):
        pass
