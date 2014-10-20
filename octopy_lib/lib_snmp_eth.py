from octopy import *

eth_port_snmp_module = {
	"const" : {
		"_static_eth_port_error_speed_max" : 10.0
	},

	"sensor" : {
		"out_frames" : 0,
		"in_frames" : 0,

		"admin_status" : "up",
		"oper_status" : "up",

		"duplex" : "full",
		"_static_duplex_req" : "full",

		"speed" : 0,

		"in_errors" : 0,
		"out_errors" : 0,

		"q_len" : 0
	},

	"var" : {
		"eth_out_frames_speed" : CalcSpeed("out_frames"),
		"eth_in_frames_speed" : CalcSpeed("in_frames"),

		"eth_in_errors_speed" : CalcSpeed("in_errors"),
		"eth_out_errors_speed" : CalcSpeed("out_errors"),

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
				.Msg("descr", "port went down")
				.Msg("msg"  , "{in_n:type} {in_n:ip}: port({if_id}) went down")
			, Recover("tag", "ETH").Msg("loc", "{in_n:ip}")
				.Msg("descr", "port is up")
				.Msg("msg"  , "{in_n:type} {in_n:ip}: port({if_id}) is up")),

		Equals("duplex_match", False) :
			( Danger("tag", "ETH").Msg("loc", "{in_n:ip}")
				.Msg("descr", "port has wrong duplex mode({duplex})")
				.Msg("msg"  , "{in_n:type} {in_n:ip}: port({if_id}) has wrong duplex mode({duplex})")
			, Recover("tag", "ETH").Msg("loc", "{in_n:ip}")
				.Msg("descr", "port duplex is ok")
				.Msg("msg"  , "{in_n:type} {in_n:ip}: port({if_id}) duplex is ok")),

		Equals("speed_match", False) :
			( Danger("tag", "ETH").Msg("loc", "{in_n:ip}")
				.Msg("descr", "port({if_id}) has a wrong speed({speed})")
				.Msg("msg"  , "port({if_id}) has a wrong speed({speed})")
			, Recover("tag", "ETH").Msg("loc", "{in_n:ip}")
				.Msg("descr", "port speed is good")
				.Msg("msg"  , "{in_n:type} {in_n:ip}: port({if_id}) speed is good")),

		Equals("q_len_ok", False).Delay(1000) :
			Warning("tag", "ETH").Msg("loc", "{in_n:ip}")
				.Msg("descr", "port queue length is above threshold for last 1000 seconds")
				.Msg("msg"  , "{in_n:type} {in_n:ip}: port({if_id}) queue length({q_len}) is above threshold for last 1000 seconds"),

		Equals("in_errors_ok", False).Delay(1000) :
			Warning("tag", "ETH").Msg("loc", "{in_n:ip}")
				.Msg("descr", "port in errors growing fast for last 1000 seconds: in_errors : {in_errors}, eth_in_errors_speed: {eth_in_errors_speed}")
				.Msg("msg"  , "{in_n:type} {in_n:ip}: port({if_id}) in errors growing fast for last 1000 seconds: in_errors : {in_errors}, eth_in_errors_speed: {eth_in_errors_speed}"),

		Equals("out_errors_ok", False).Delay(1000) :
			Warning("tag", "ETH").Msg("loc", "{in_n:ip}")
				.Msg("descr", "port out errors growing fast for last 1000 seconds: out_errors : {out_errors}, eth_out_errors_speed: {eth_out_errors_speed}")
				.Msg("msg"  , "{in_n:type} {in_n:ip}: port({if_id}) out errors growing fast for last 1000 seconds: out_errors : {out_errors}, eth_out_errors_speed: {eth_out_errors_speed}"),
	}
}
