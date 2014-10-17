from octopy import *

snmp_general_module = {
	"sensor" : {
		"configChangeSNMP" : True,
		"accessViolationConsole" : True,
		"accessViolationHTTP" : True,
		"passwordChange" : True,
	},

	"react" : {
		Equals("configChangeSNMP", False) :
			Danger("tag", "INFRASTRUCUTRE")
				.Msg("descr", "SNMP trap: configChangeSNMP")
				.Msg("msg"  , "SNMP trap: configChangeSNMP on {ip}"),
		Equals("accessViolationConsole", False) :
			Danger("tag", "INFRASTRUCUTRE")
				.Msg("descr", "SNMP trap: accessViolationConsole")
				.Msg("msg"  , "SNMP trap: accessViolationConsole on {ip}"),
		Equals("accessViolationHTTP", False) :
			Danger("tag", "INFRASTRUCUTRE")
				.Msg("descr", "SNMP trap: accessViolationHTTP")
				.Msg("msg"  , "SNMP trap: accessViolationHTTP on {ip}"),
		Equals("passwordChange", False) :
			Danger("tag", "INFRASTRUCUTRE")
				.Msg("descr", "SNMP trap: passwordChange")
				.Msg("msg"  , "SNMP trap: passwordChange on {ip}"),
	}
}
