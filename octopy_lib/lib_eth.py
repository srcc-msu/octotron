from octopy import *

def LinkModule():
	return {
		"trigger" : {
			"duplex_mismatch" : LinkedNotMatch("duplex"),
			"speed_mismatch" : LinkedNotMatch("speed"),
		},

		"react" : {
			"notify_duplex_mismatch" : Reaction()
				.On("duplex_mismatch")
				.Begin(Warning("tag", "ETH").Msg("loc", "{left.in_n:ip} {right.in_n:ip}")
					.Msg("descr", "mismatch duplex mode on two sides of the link")
					.Msg("msg"  , "mismatch duplex mode on two sides of the link from {left:ip} to {right:ip}")),

			"notify_speed_mismatch" : Reaction()
				.On("speed_mismatch")
				.Begin(Warning("tag", "ETH").Msg("loc", "{left.in_n:ip} {right.in_n:ip}")
					.Msg("descr", "mismatch speed on two sides of the link")
					.Msg("msg"  , "mismatch speed on two sides of the link  from {left:ip} to {right:ip}"))
		}
	}

def __PortsDefaultMessages(loc, loc_s, loc_l):
	if loc is None:
		loc = "{in_n:ip}"

	if loc_s is None:
		loc_s = "{in_n:type} {type}: "

	if loc_l is None:
		loc_l = "{in_n:type}[{in_n:ip}] {type}[{id}][{name}][{descr}]: "

	return (loc, loc_s, loc_l)

def PortModule(timeout = UPDATE_TIME_NOT_SPECIFIED, loc = None, loc_s = None, loc_l = None):
	"""requires user to define 'speed_req'"""

	loc, loc_s, loc_l = __PortsDefaultMessages(loc, loc_s, loc_l)

	return {
		"sensor" : {
			"name" : String(UPDATE_TIME_NOT_SPECIFIED, ""),
			"descr" : String(UPDATE_TIME_NOT_SPECIFIED, ""),

			"admin_status" : String(UPDATE_TIME_NOT_SPECIFIED, "up"),
			"oper_status" : String(timeout),

			"speed" : Long(timeout),
			"duplex" : String(timeout),
		},

		"trigger" : {
			"status_mismatch" : NotMatchArg("oper_status", "admin_status"),
		},

		"react" : {
			"notify_status_mismatch" : Reaction()
				.On("status_mismatch")
				.Begin(Warning("tag", "ETH").Msg("loc", loc)
					.Msg("descr", loc_s + "is down")
					.Msg("msg"  , loc_l + "is down")),
		}
	}

def PortDuplexModule(loc = None, loc_s = None, loc_l = None):
	"""depends on PortModule"""

	loc, loc_s, loc_l = __PortsDefaultMessages(loc, loc_s, loc_l)

	return {
		"sensor" : {
			"duplex_req" : String(UPDATE_TIME_NOT_SPECIFIED, "full"),
		},

		"trigger" : {
			"duplex_mismatch" : NotMatchArg("duplex", "duplex_req"),
		},

		"react" : {
			"notify_duplex_mismatch" : Reaction()
				.On("duplex_mismatch")
				.Begin(Warning("tag", "ETH").Msg("loc", loc)
					.Msg("descr", loc_s + "wrong duplex mode")
					.Msg("msg"  , loc_l + "wrong duplex mode: {duplex}")),
		}
	}

def PortSpeedModule(loc = None, loc_s = None, loc_l = None):
	"""depends on PortModule, requires user to define 'speed_req'"""

	loc, loc_s, loc_l = __PortsDefaultMessages(loc, loc_s, loc_l)

	return {
		"trigger" : {
			"speed_mismatch" : NotMatchArg("speed", "speed_req"),
		},

		"react" : {
			"notify_speed_mismatch" : Reaction()
				.On("speed_mismatch")
				.Begin(Warning("tag", "ETH").Msg("loc", loc)
					.Msg("descr", loc_s + "wrong speed")
					.Msg("msg"  , loc_l + "wrong speed: {speed} != {speed_req}")),
		}
	}
