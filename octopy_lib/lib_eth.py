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

def PortModule(timeout = UPDATE_TIME_NOT_SPECIFIED):
	"""requires user to define and 'speed_req'"""

	loc = "{in_n:id}"
	loc_s = "{in_n:type} {type}: "
	loc_l = "{in_n:type}[{in_n:ip},{in_n:descr}] {type}[{id}]: "

	return {
		"sensor" : {
			"admin_status" : String(UPDATE_TIME_NOT_SPECIFIED, "up"),
			"duplex_req" : String(UPDATE_TIME_NOT_SPECIFIED, "full"),
			"oper_status" : String(timeout),
			"duplex" : String(timeout),
			"speed" : Long(timeout),
		},

		"var" : {
			"status_match" : ArgMatch("oper_status", "admin_status"),
			"duplex_match" : ArgMatch("duplex", "duplex_req"),
			"speed_match" : ArgMatch("speed", "speed_req"),
		},

		"react" : {
			Equals("status_match", False) :
				( Danger("tag", "ETH").Msg("loc", loc)
					.Msg("descr", loc_s + "is down")
					.Msg("msg"  , loc_l + "is down")
				, Recover("tag", "ETH").Msg("loc", loc)
					.Msg("descr", loc_s + "is up")
					.Msg("msg"  , loc_l + "is up")),

			Equals("duplex_match", False) :
				( Danger("tag", "ETH").Msg("loc", loc)
					.Msg("descr", loc_s + "wrong duplex mode")
					.Msg("msg"  , loc_l + "wrong duplex mode({duplex})")
				, Recover("tag", "ETH").Msg("loc", loc)
					.Msg("descr", loc_s + "duplex is ok")
					.Msg("msg"  , loc_l + "duplex is ok")),

			Equals("speed_match", False) :
				( Danger("tag", "ETH").Msg("loc", loc)
					.Msg("descr", loc_s + "wrong speed")
					.Msg("msg"  , loc_l + "wrong speed({speed}), required: {duplex_req}")
				, Recover("tag", "ETH").Msg("loc", loc)
					.Msg("descr", loc_s + "speed is ok")
					.Msg("msg"  , loc_l + "speed is ok")),
		}
	}