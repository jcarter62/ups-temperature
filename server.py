from flask import Flask, escape, request, jsonify, render_template
from devicelist import DeviceList
from ups_snmp import UpsSnmp
from db import DB
from db_path import DbPath

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/api/v1/latest', methods=['POST'])
def api_v1_latest():
    data_list = []
    d = DeviceList()
    db = get_db_connection()

    for dev in d.devices():
        data_list.append(db.get_recent_data(dev['ip']))

    result = jsonify({'data': data_list})
    return result


@app.route('/api/v1/devices', methods=['POST'])
def api_v1_devices():
    data_list = []
    d = DeviceList()
    db = get_db_connection()

    for dev in d.devices():
        onedev = db.get_recent_data(dev['ip'])
        item = {
            'ip': dev['ip'],
            'name': onedev['name'],
            'location': onedev['location']
        }
        data_list.append(item)

    result = jsonify({'data': data_list})
    return result


@app.route('/api/v1/dev_last_hour/<ip>', methods=['POST'])
def api_v1_device(ip):
    data_list = []
    db = get_db_connection()
    for item in db.get_dev_last_hour(ip):
        data_list.append(item)

    # sort ascending by ts.
    result_object = {"data": data_list}

    result = jsonify(result_object)
    return result


def get_db_connection():
    database_path = DbPath().database_path()
    if database_path > '':
        db = DB(database_path)
    else:
        db = DB()

    return db

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

