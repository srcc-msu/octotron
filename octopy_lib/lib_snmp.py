from octopy import *

snmp_general_module = {
	"sensor" : {
		"configChangeSNMP" : True,
		"accessViolationConsole" : True,
		"accessViolationHTTP" : True,
		"passwordChange" : True,
	},

	"react" : {
		("configChangeSNMP", False) : Reaction(Danger("SNMP trap: configChangeSNMP", "type")),
		("accessViolationConsole", False) : Reaction(Danger("SNMP trap: accessViolationConsole", "type")),
		("accessViolationHTTP", False) : Reaction(Danger("SNMP trap: accessViolationHTTP", "type")),
		("passwordChange", False) : Reaction(Danger("SNMP trap: passwordChange", "type")),
	}
}
