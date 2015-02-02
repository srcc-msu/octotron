from octopy import *

def PingModule(timeout = Minutes(10)):
	return {
		"sensor" : {
			"ping" : Boolean(timeout),
		},

		"react" : {
			Equals("ping", False).Repeat(2) :
				( Danger("tag", "NETWORK").Msg("loc", "{ip}")
					.Msg("descr", "{type}: ping failed twice")
					.Msg("msg"  , "{type}[{ip}]: ping failed twice")
				, Recover("tag", "NETWORK").Msg("loc", "{ip}")
					.Msg("descr", "{type}: ping ok")
					.Msg("msg"  , "{type}[{ip}]: ping ok")),
		}
	}

def SshModule(timeout = Minutes(10)):
	return {
		"sensor" : {
			"ssh" : Boolean(timeout),
		},

		"react" : {
			Equals("ssh", False).Repeat(2) :
				( Danger("tag", "NETWORK").Msg("loc", "{ip}")
					.Msg("descr", "{type}: ssh failed twice")
					.Msg("msg"  , "{type}[{ip}]: ssh failed twice")
				, Recover("tag", "NETWORK").Msg("loc", "{ip}")
					.Msg("descr", "{type}: ssh ok")
					.Msg("msg"  , "{type}[{ip}]: ssh ok")),
		}
	}

def SnmpModule(timeout = Minutes(10)):
	return {
		"sensor" : {
			"snmp" : Boolean(timeout),
		},

		"react" : {
			Equals("snmp", False).Repeat(2) :
				( Danger("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: snmp check failed twice")
					.Msg("msg"  , "{type}[{ip}]: snmp check failed twice")
				, Recover("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: snmp check ok")
					.Msg("msg"  , "{type}[{ip}]: snmp check ok")),
		}
	}