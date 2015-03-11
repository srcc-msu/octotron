from octopy import *

def PingModule(timeout = Minutes(10), key = "ip"):
	return {
		"sensor" : {
			"ping" : Boolean(timeout),
		},

		"react" : {
			Equals("ping", False).Repeat(2) :
				( Danger("tag", "NETWORK").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: ping failed twice")
					.Msg("msg"  , "{type}[{" + key + "}]: ping failed twice")
				, Recover("tag", "NETWORK").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: ping ok")
					.Msg("msg"  , "{type}[{" + key + "}]: ping ok")),
		}
	}

def SshModule(timeout = Minutes(10), key = "ip"):
	return {
		"sensor" : {
			"ssh" : Boolean(timeout),
		},

		"react" : {
			Equals("ssh", False).Repeat(2) :
				( Danger("tag", "NETWORK").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: ssh failed twice")
					.Msg("msg"  , "{type}[{" + key + "}]: ssh failed twice")
				, Recover("tag", "NETWORK").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: ssh ok")
					.Msg("msg"  , "{type}[{" + key + "}]: ssh ok")),
		}
	}

def SnmpModule(timeout = Minutes(10), key = "ip"):
	return {
		"sensor" : {
			"snmp" : Boolean(timeout),
		},

		"react" : {
			Equals("snmp", False).Repeat(2) :
				( Danger("tag", "INFRASTRUCTURE").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: snmp check failed twice")
					.Msg("msg"  , "{type}[{" + key + "}]: snmp check failed twice")
				, Recover("tag", "INFRASTRUCTURE").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: snmp check ok")
					.Msg("msg"  , "{type}[{" + key + "}]: snmp check ok")),
		}
	}