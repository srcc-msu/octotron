from octopy import *

SNMP_UPDATE_TIME = Minutes(1)

snmp_general_module = {
	"sensor" : {
		"configChangeSNMP" : Boolean(True, SNMP_UPDATE_TIME),
		"accessViolationConsole" : Boolean(True, SNMP_UPDATE_TIME),
		"accessViolationHTTP" : Boolean(True, SNMP_UPDATE_TIME),
		"passwordChange" : Boolean(True, SNMP_UPDATE_TIME),
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
