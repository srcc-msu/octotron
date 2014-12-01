from octopy import *

SNMP_UPDATE_TIME = UPDATE_TIME_NOT_SPECIFIED

snmp_general_module = {
	"sensor" : {
		"configChangeSNMP"       : Boolean(SNMP_UPDATE_TIME, True),
		"accessViolationConsole" : Boolean(SNMP_UPDATE_TIME, True),
		"accessViolationHTTP"    : Boolean(SNMP_UPDATE_TIME, True),
		"passwordChange"         : Boolean(SNMP_UPDATE_TIME, True),
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
