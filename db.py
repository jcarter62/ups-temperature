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

    def strip_bquote(self, s):
        out = s
        if s[0] == 'b' and s[1] == '\'':
            out = ''
            i = 2
            while i < (s.__len__() - 1):
                out = out + s[i]
                i = i + 1
        return out


    def get_recent_data(self, ip ):
        result = {}
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()

        cur.execute(self.most_recent_def)
        conn.commit()

        cmd = 'select id, ip, name, location, temperature, ts from recent where ip = ? '
        cur.execute(cmd, (ip,))
        row = cur.fetchone()
        if row:
            result = {
                "id": int(row[0]),
                "ip": str(row[1]),
                "name": self.strip_bquote(str(row[2])),
                "location": self.strip_bquote(str(row[3])),
                "temperature": str(row[4]),
                "ts": row[5]
            }

        cur.close()
        return result


    def get_dev_last_hour(self, ip ):
        hour_ago = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%m:%S')
        result = list()
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()

        cmd = 'select id, ip, name, location, temperature, ts, ' + \
              "datetime(ts,12) as t2 " + \
              'from data ' + \
              'where (ip = ?) and (ts >= ?)' + \
              'order by ts  '
        cur.execute(cmd, (ip, hour_ago))
        rows = cur.fetchall()
        for row in rows:
            item = {
                "id": int(row[0]),
                "ip": str(row[1]),
                "name": self.strip_bquote(str(row[2])),
                "location": self.strip_bquote(str(row[3])),
                "temperature": float(row[4]),
                "ts": str(row[5])
            }
            result.append(item)

        cur.close()
        return result


    def close(self):
        pass
