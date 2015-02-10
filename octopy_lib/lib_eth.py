from octopy import *

def LinkModule():
	return {
	"var" : {
		"duplex_match" : LinkedVarArgMatch("duplex"),
		"speed_match" : LinkedVarArgMatch("speed"),
	},

	"react" : {
		Equals("duplex_match", False) :
			( Danger("tag", "ETH").Msg("loc", "{source.in_n:ip}")
				.Msg("descr", "mismatch duplex mode on two sides of the link")
				.Msg("msg"  , "mismatch duplex mode on two sides of the link from {target:ip} to {source:ip}")
			, Recover("tag", "ETH").Msg("loc", "{source.in_n:ip}")
				.Msg("descr", "duplex on the link is ok")
				.Msg("msg"  , "duplex on the link is ok from {target:ip} to {source:ip}")),

		Equals("speed_match", False) :
			( Danger("tag", "ETH").Msg("loc", "{source.in_n:ip}")
				.Msg("descr", "mismatch speed on two sides of the link")
				.Msg("msg"  , "mismatch speed on two sides of the link  from {target:ip} to {source:ip}")
			, Recover("tag", "ETH").Msg("loc", "{source.in_n:ip}")
				.Msg("descr", "speed on the link is ok")
				.Msg("msg"  , "speed on the link is ok from {target:ip} to {source:ip}")),
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

		"var" : {
			"status_match" : ArgMatch("oper_status", "admin_status"),
		},

		"react" : {
			Equals("status_match", False) :
				( Danger("tag", "ETH").Msg("loc", loc)
					.Msg("descr", loc_s + "is down")
					.Msg("msg"  , loc_l + "is down")
				, Recover("tag", "ETH").Msg("loc", loc)
					.Msg("descr", loc_s + "is up")
					.Msg("msg"  , loc_l + "is up")),
		}
	}

def PortDuplexModule(loc = None, loc_s = None, loc_l = None):
	"""depends on PortModule"""

	loc, loc_s, loc_l = __PortsDefaultMessages(loc, loc_s, loc_l)

	return {
		"sensor" : {
			"duplex_req" : String(UPDATE_TIME_NOT_SPECIFIED, "full"),
		},

		"var" : {
			"duplex_match" : ArgMatch("duplex", "duplex_req"),
		},

		"react" : {
			Equals("duplex_match", False) :
				( Danger("tag", "ETH").Msg("loc", loc)
					.Msg("descr", loc_s + "wrong duplex mode")
					.Msg("msg"  , loc_l + "wrong duplex mode({duplex})")
				, Recover("tag", "ETH").Msg("loc", loc)
					.Msg("descr", loc_s + "duplex is ok")
					.Msg("msg"  , loc_l + "duplex is ok")),
		}
	}

def PortSpeedModule(loc = None, loc_s = None, loc_l = None):
	"""depends on PortModule, requires user to define 'speed_req'"""

	loc, loc_s, loc_l = __PortsDefaultMessages(loc, loc_s, loc_l)

	return {
		"var" : {
			"speed_match" : ArgMatch("speed", "speed_req"),
		},

		"react" : {
			Equals("speed_match", False) :
				( Danger("tag", "ETH").Msg("loc", loc)
					.Msg("descr", loc_s + "wrong speed")
					.Msg("msg"  , loc_l + "wrong speed({speed}), required: {speed_req}")
				, Recover("tag", "ETH").Msg("loc", loc)
					.Msg("descr", loc_s + "speed is ok")
					.Msg("msg"  , loc_l + "speed is ok")),
		}
	}
