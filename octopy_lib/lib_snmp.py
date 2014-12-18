from octopy import *

def SnmpGeneralModule(update_time = UPDATE_TIME_NOT_SPECIFIED):
	return {
		"sensor" : {
			"configChangeSNMP"       : Boolean(update_time, True),
			"accessViolationConsole" : Boolean(update_time, True),
			"accessViolationHTTP"    : Boolean(update_time, True),
			"passwordChange"         : Boolean(update_time, True),
		},

		"react" : {
			Equals("configChangeSNMP", False) :
				Danger("tag", "INFRASTRUCUTRE").Msg("loc", "{ip}")
					.Msg("descr", "SNMP trap: configChangeSNMP")
					.Msg("msg"  , "SNMP trap: configChangeSNMP on {ip}"),
			Equals("accessViolationConsole", False) :
				Danger("tag", "INFRASTRUCUTRE").Msg("loc", "{ip}")
					.Msg("descr", "SNMP trap: accessViolationConsole")
					.Msg("msg"  , "SNMP trap: accessViolationConsole on {ip}"),
			Equals("accessViolationHTTP", False) :
				Danger("tag", "INFRASTRUCUTRE").Msg("loc", "{ip}")
					.Msg("descr", "SNMP trap: accessViolationHTTP")
					.Msg("msg"  , "SNMP trap: accessViolationHTTP on {ip}"),
			Equals("passwordChange", False) :
				Danger("tag", "INFRASTRUCUTRE").Msg("loc", "{ip}")
					.Msg("descr", "SNMP trap: passwordChange")
					.Msg("msg"  , "SNMP trap: passwordChange on {ip}"),
		}
	}
