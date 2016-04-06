from octopy import *

def PingModule(timeout = Minutes(10), key = "ip", status = Warning, rstatus = RWarning):
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
				.End(rstatus("tag", "NETWORK").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: ping ok")
					.Msg("msg"  , "{type}[{" + key + "}]: ping ok")),
		}
	}

def SshModule(timeout = Minutes(10), key = "ip", status = Warning, rstatus = RWarning):
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
				.End(rstatus("tag", "NETWORK").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: ssh ok")
					.Msg("msg"  , "{type}[{" + key + "}]: ssh ok")),
		}
	}

def SnmpModule(timeout = Minutes(10), key = "ip", status = Warning, rstatus = RWarning):
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
				.End(rstatus("tag", "NETWORK").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: snmp ok")
					.Msg("msg"  , "{type}[{" + key + "}]: snmp ok")),
		}
	}

def GroupPingModule(group_name, total_count, threshold = 20, status = Danger, rstatus = RDanger):
	# TODO: update after adding entity_count rule
	return {
		"const" : {
			"group_name" : group_name,
			"failed_threshold" : threshold,
		},

		"var" : {
			"failed_ping" : ASoftMatchCount(False, "out_n", "ping"),
			"failed_pct_ping" : ToPct("failed_ping", total_count),
		},

		"trigger" : {
			"many_failed_ping" : GTArg("failed_pct_ping", "failed_threshold"),
		},

		"react" : {
			"notify_many_failed_ping" : Reaction()
				.On("many_failed_ping")
				.Begin(status("tag", "SYSTEM").Msg("loc", "{id}")
					.Msg("descr", "too many unavailable hosts")
					.Msg("msg"  , "{group_name}: too many unavailable hosts: {failed_ping} = {failed_pct_ping}%"))
				.End(rstatus("tag", "SYSTEM").Msg("loc", "{id}")
					.Msg("descr", "enough hosts are available again")
					.Msg("msg"  , "{group_name}: enough hosts are available again: {failed_ping} = {failed_pct_ping}%"))
		}
	}