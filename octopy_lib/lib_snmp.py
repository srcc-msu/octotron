from octopy import *

def SnmpGeneralModule(timeout = UPDATE_TIME_NOT_SPECIFIED):
	return {
		"sensor" : {
			"configChangeSNMP"       : Boolean(timeout, True),
			"accessViolationConsole" : Boolean(timeout, True),
			"accessViolationHTTP"    : Boolean(timeout, True),
			"passwordChange"         : Boolean(timeout, True),
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
