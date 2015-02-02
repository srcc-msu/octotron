from octopy import *

def EthPortSnmpModule(timeout = Minutes(10)):
	return {
		"const" : {
			"_static_eth_port_error_speed_max" : 10.0,
		},

		"sensor" : {
			"out_frames" : Long(timeout),
			"in_frames" : Long(timeout),

			"in_errors" : Long(timeout),
			"out_errors" : Long(timeout),

			"q_len" : Long(timeout),
		},

		"var" : {
			"eth_out_frames_speed" : Speed("out_frames"),
			"eth_in_frames_speed" : Speed("in_frames"),

			"eth_in_errors_speed" : Speed("in_errors"),
			"eth_out_errors_speed" : Speed("out_errors"),

			"in_errors_ok" : UpperArgThreshold("eth_in_errors_speed", "_static_eth_port_error_speed_max"),
			"out_errors_ok" : UpperArgThreshold("eth_out_errors_speed", "_static_eth_port_error_speed_max"),

			"q_len_ok" : Match("q_len", 0)
		},

		"react" : {
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
