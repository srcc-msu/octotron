from octopy import *

def EthPortSnmpModule(timeout = Minutes(10)):
	return {
		"const" : {
			"static_eth_port_error_speed_max" : 10.0,
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
		},


		"trigger" : {
			"high_in_errors" : GTArg("eth_in_errors_speed", "static_eth_port_error_speed_max"),
			"high_out_errors" : GTArg("eth_out_errors_speed", "static_eth_port_error_speed_max"),

			"bad_q_len" : Match("q_len", 0)
		},

		"react" : {
			"notify_bad_q_len" : Reaction()
				.On("bad_q_len", 0, 1000)
				.Begin(Warning("tag", "ETH").Msg("loc", "{in_n:ip}")
					.Msg("descr", "{type}: queue length is above threshold for last 1000 seconds")
					.Msg("msg"  , "{type}({in_n:ip})[{if_id}] queue length({q_len}) is above threshold for last 1000 seconds"))
				.End(RWarning("tag", "ETH").Msg("loc", "{in_n:ip}")
					.Msg("descr", "{type}: queue length is ok")
					.Msg("msg"  , "{type}({in_n:ip})[{if_id}] queue length({q_len}) is ok")),

			"notify_high_in_errors" : Reaction()
				.On("high_in_errors", 0, 1000)
				.Begin(Warning("tag", "ETH").Msg("loc", "{in_n:ip}")
					.Msg("descr", "{type}: in errors growing fast for last 1000 seconds")
					.Msg("msg"  , "{type}({in_n:ip})[{if_id}] in errors growing fast for last 1000 seconds: in_errors : {in_errors}, eth_in_errors_speed: {eth_in_errors_speed}"))
				.End(RWarning("tag", "ETH").Msg("loc", "{in_n:ip}")
					.Msg("descr", "{type}: in errors are ok")
					.Msg("msg"  , "{type}({in_n:ip})[{if_id}] in errors are ok: in_errors : {in_errors}, eth_in_errors_speed: {eth_in_errors_speed}")),

			"notify_high_out_errors" : Reaction()
				.On("high_out_errors", 0, 1000)
				.Begin(Warning("tag", "ETH").Msg("loc", "{in_n:ip}")
					.Msg("descr", "{type}: out errors growing fast for last 1000 seconds")
					.Msg("msg"  , "{type}({in_n:ip})[{if_id}] out errors growing fast for last 1000 seconds: out_errors : {out_errors}, eth_out_errors_speed: {eth_out_errors_speed}"))
				.End(RWarning("tag", "ETH").Msg("loc", "{in_n:ip}")
					.Msg("descr", "{type}: out errors are ok")
					.Msg("msg"  , "{type}({in_n:ip})[{if_id}] out errors are ok: out_errors : {out_errors}, eth_out_errors_speed: {eth_out_errors_speed}")),
		}
	}
