from octopy import *

snmp_general_module = {
	"sensor" : {
		"configChangeSNMP" : True,
		"accessViolationConsole" : True,
		"accessViolationHTTP" : True,
		"passwordChange" : True,
	},

	"react" : {
		Equals("configChangeSNMP", False) : Danger("SNMP trap: configChangeSNMP", "type"),
		Equals("accessViolationConsole", False) : Danger("SNMP trap: accessViolationConsole", "type"),
		Equals("accessViolationHTTP", False) : Danger("SNMP trap: accessViolationHTTP", "type"),
		Equals("passwordChange", False) : Danger("SNMP trap: passwordChange", "type"),
	}
}
