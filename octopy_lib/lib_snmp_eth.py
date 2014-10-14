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
		Equals("q_len_ok", False).Delay(1000) :
			Warning("ETH", "eth port({if_id}) queue length(q_len) is growing for last 1000 seconds").PrintParent("type", "ip"),

		Equals("status_match", False) :
			(Danger("ETH", "port({if_id}) went down", "type").PrintParent("type", "ip")
				, Recover("port({if_id}) is up").PrintParent("type", "ip")),

		Equals("duplex_match", False) :
			(Danger("ETH", "port({if_id}) has wrong duplex mode({duplex})").PrintParent("type", "ip")
				, Recover("port({if_id}) duplex is ok").PrintParent("type", "ip")),

		Equals("speed_match", False) :
			(Danger("ETH", "port({if_id}) has a wrong speed({speed})").PrintParent("type", "ip")
				, Recover("port({if_id}) speed is good").PrintParent("type", "ip")),

		Equals("in_errors_ok", False).Delay(1000) :
			Warning("ETH", "port({if_id}) in errors growing fast for last 1000 seconds: in_errors : {in_errors}, eth_in_errors_speed: {eth_in_errors_speed}").PrintParent("type", "ip"),

		Equals("out_errors_ok", False).Delay(1000) :
			Warning("ETH", "port({if_id}) out errors growing fast for last 1000 seconds: out_errors : {out_errors}, eth_out_errors_speed: {eth_out_errors_speed}").PrintParent("type", "ip")
	}
}
