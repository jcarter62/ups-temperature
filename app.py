from devicelist import DeviceList
from ups_snmp import UpsSnmp
from db import DB
from db_path import DbPath


d = DeviceList()
database_path = DbPath().database_path()
if database_path > '':
    db = DB(database_path)
else:
    db = DB()

for dev in d.devices():
    ups = UpsSnmp(dev['ip'])
    db.save_record(ups.result)
    db.save_most_recent(ups.result)








