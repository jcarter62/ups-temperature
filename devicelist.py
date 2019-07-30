class DeviceList:
    def __init__(self):
        self.addresses = [
            {'ip': '192.168.5.96'},
            {'ip': '192.168.5.99'},
            {'ip': '172.16.100.130'},
            {'ip': '172.16.100.132'},
            {'ip': '172.16.100.134'}]

    def devices(self):
        return self.addresses
