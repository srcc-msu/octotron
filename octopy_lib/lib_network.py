from octopy import *

def PingModule(timeout = Minutes(10), key = "ip", status = Warning):
	return {
		"sensor" : {
			"ping" : Boolean(timeout),
		},

		"trigger" : {
			"ping_failed" : Match("ping", False)
		},

		"react" : {
			"notify_ping_failed" : Reaction()
				.On("ping_failed", 3, 0)
				.Begin(status("tag", "NETWORK").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: ping failed three times")
					.Msg("msg"  , "{type}[{" + key + "}]: ping failed three times"))
				.End(Recover("tag", "NETWORK").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: ping ok")
					.Msg("msg"  , "{type}[{" + key + "}]: ping ok")),
		}
	}

def SshModule(timeout = Minutes(10), key = "ip", status = Warning):
	return {
		"sensor" : {
			"ssh" : Boolean(timeout),
		},

		"trigger" : {
			"ssh_failed" : Match("ssh", False)
		},

		"react" : {
			"notify_ssh_failed" : Reaction()
				.On("ssh_failed", 3, 0)
				.Begin(status("tag", "NETWORK").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: ssh failed three times")
					.Msg("msg"  , "{type}[{" + key + "}]: ssh failed three times"))
				.End(Recover("tag", "NETWORK").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: ssh ok")
					.Msg("msg"  , "{type}[{" + key + "}]: ssh ok")),
		}
	}

def SnmpModule(timeout = Minutes(10), key = "ip", status = Warning):
	return {
		"sensor" : {
			"snmp" : Boolean(timeout),
		},

		"trigger" : {
			"snmp_failed" : Match("snmp", False)
		},

		"react" : {
			"notify_snmp_failed" : Reaction()
				.On("snmp_failed", 3, 0)
				.Begin(status("tag", "NETWORK").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: snmp failed three times")
					.Msg("msg"  , "{type}[{" + key + "}]: snmp failed three times"))
				.End(Recover("tag", "NETWORK").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: snmp ok")
					.Msg("msg"  , "{type}[{" + key + "}]: snmp ok")),
		}
	}