#
from pysnmp.entity.rfc3413.oneliner import cmdgen

# SNMP Community String (Read-Only)
SNMP_COMMUNITY = 'public'
NAME_OID = '1.3.6.1.2.1.1.5.0'
LOCATION_OID = '1.3.6.1.2.1.1.6.0'
TEMPERATURE_OID = '1.3.6.1.4.1.318.1.1.10.2.3.2.1.4.1'


class UpsSnmp:

    def __init__(self, ip):
        self.ip = ip
        self.state = ''
        self.name = ''
        self.location = ''
        self.temperature = 0
        self.result = {
            'ip': self.ip,
            'name': self._get_string_value(NAME_OID),
            'location': self._get_string_value(LOCATION_OID),
            'temperature': self._get_float_value(TEMPERATURE_OID)}

    def _get_string_value(self, oid):
        cmd = cmdgen.CommandGenerator()

        error_indication, error_status, error_index, var_binds = cmd.getCmd(
            cmdgen.CommunityData('public', mpModel=0),
            cmdgen.UdpTransportTarget((self.ip, 161)),
            cmdgen.MibVariable(oid)
        )

        if not error_indication and not error_status:
            result = var_binds[0][1]._value

        return result

    def _get_float_value(self, oid):
        cmd = cmdgen.CommandGenerator()

        error_indication, error_status, error_index, var_binds = cmd.getCmd(
            cmdgen.CommunityData('public', mpModel=0),
            cmdgen.UdpTransportTarget((self.ip, 161)),
            cmdgen.MibVariable(oid)
        )

        if not error_indication and not error_status:
            result = float(var_binds[0][1]._value)

        if result < 50:
            result = (float(result) * (9.0/5.0)) + 32.0

        return result

    def get_data(self):
        return self.result

