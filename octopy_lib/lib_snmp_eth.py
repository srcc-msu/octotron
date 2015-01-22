from octopy import *

def EthPortSnmpModule(timeout = Minutes(10)):
	return {
		"const" : {
			"_static_eth_port_error_speed_max" : 10.0,
			"_static_duplex_req" : "full",
		},

		"sensor" : {
			"out_frames" : Long(timeout),
			"in_frames" : Long(timeout),

			"admin_status" : String(timeout),
			"oper_status" : String(timeout),

			"duplex" : String(timeout),

			"speed" : Long(timeout),

			"in_errors" : Long(timeout),
			"out_errors" : Long(timeout),

			"q_len" : Long(timeout),
		},

		"var" : {
			"eth_out_frames_speed" : Speed("out_frames"),
			"eth_in_frames_speed" : Speed("in_frames"),

			"eth_in_errors_speed" : Speed("in_errors"),
			"eth_out_errors_speed" : Speed("out_errors"),

			"status_match" : ArgMatch("oper_status", "admin_status"),
			"duplex_match" : ArgMatch("duplex", "_static_duplex_req"),

			"speed_match" : ArgMatch("speed", "speed_req"),

			"in_errors_ok" : UpperArgThreshold("eth_in_errors_speed", "_static_eth_port_error_speed_max"),
			"out_errors_ok" : UpperArgThreshold("eth_out_errors_speed", "_static_eth_port_error_speed_max"),

			"q_len_ok" : Match("q_len", 0)
		},

		"react" : {
			Equals("status_match", False) :
				( Danger("tag", "ETH").Msg("loc", "{in_n:ip}")
					.Msg("descr", "{type}: is down")
					.Msg("msg"  , "{type}({in_n:ip})[{if_id}] is down")
				, Recover("tag", "ETH").Msg("loc", "{in_n:ip}")
					.Msg("descr", "{type}: is up")
					.Msg("msg"  , "{type}({in_n:ip})[{if_id}] is up")),

			Equals("duplex_match", False) :
				( Danger("tag", "ETH").Msg("loc", "{in_n:ip}")
					.Msg("descr", "{type}: wrong duplex mode")
					.Msg("msg"  , "{type}({in_n:ip})[{if_id}] wrong duplex mode({duplex})")
				, Recover("tag", "ETH").Msg("loc", "{in_n:ip}")
					.Msg("descr", "{type}: duplex is ok")
					.Msg("msg"  , "{type}({in_n:ip})[{if_id}] duplex is ok")),

			Equals("speed_match", False) :
				( Danger("tag", "ETH").Msg("loc", "{in_n:ip}")
					.Msg("descr", "{type}: wrong speed")
					.Msg("msg"  , "{type}({in_n:ip})[{if_id}] wrong speed({speed})")
				, Recover("tag", "ETH").Msg("loc", "{in_n:ip}")
					.Msg("descr", "{type}: speed is ok")
					.Msg("msg"  , "{type}({in_n:ip})[{if_id}] speed is ok")),

			Equals("q_len_ok", False).Delay(1000) :
				Warning("tag", "ETH").Msg("loc", "{in_n:ip}")
					.Msg("descr", "{type}: queue length is above threshold for last 1000 seconds")
					.Msg("msg"  , "{type}({in_n:ip})[{if_id}] queue length({q_len}) is above threshold for last 1000 seconds"),

			Equals("in_errors_ok", False).Delay(1000) :
				Warning("tag", "ETH").Msg("loc", "{in_n:ip}")
					.Msg("descr", "{type}: in errors growing fast for last 1000 seconds")
					.Msg("msg"  , "{type}({in_n:ip})[{if_id}] in errors growing fast for last 1000 seconds: in_errors : {in_errors}, eth_in_errors_speed: {eth_in_errors_speed}"),

			Equals("out_errors_ok", False).Delay(1000) :
				Warning("tag", "ETH").Msg("loc", "{in_n:ip}")
					.Msg("descr", "{type}: out errors growing fast for last 1000 seconds")
					.Msg("msg"  , "{type}({in_n:ip})[{if_id}] out errors growing fast for last 1000 seconds: out_errors : {out_errors}, eth_out_errors_speed: {eth_out_errors_speed}"),
		}
	}
