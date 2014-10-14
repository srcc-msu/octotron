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
			Danger("INFRASTRUCUTRE", "SNMP trap: configChangeSNMP"),
		Equals("accessViolationConsole", False) :
			Danger("INFRASTRUCUTRE", "SNMP trap: accessViolationConsole"),
		Equals("accessViolationHTTP", False) :
			Danger("INFRASTRUCUTRE", "SNMP trap: accessViolationHTTP"),
		Equals("passwordChange", False) :
			Danger("INFRASTRUCUTRE", "SNMP trap: passwordChange"),
	}
}
