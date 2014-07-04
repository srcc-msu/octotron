from octopy import *

eth_port_snmp_a = {
	"type" : "port",

	"out_frames" : 0,
	"in_frames" : 0,

	"admin_status" : "up",
	"oper_status" : "up",

	"duplex" : "full",
	"_static_duplex_req" : "full",

	"speed" : 0,

	"in_errors" : 0,
	"out_errors" : 0,

	"q_len" : 0,

	"_static_eth_port_error_speed_max" : 10.0,
}

eth_port_snmp_r = {
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
}

eth_port_snmp_react = {
	("q_len_ok", False) :
		Reaction(Warning("eth port queue length is growing for last 1000 seconds", "type", "if_id", "q_len").PrintParent("type", "ip"), delay = 1000),

	("status_match", False) :
		Reaction(Danger("port went down", "type", "if_id", "admin_status", "oper_status").PrintParent("type", "ip")
			, Recover("port is up", "if_id", "admin_status", "oper_status").PrintParent("type", "ip")),

	("duplex_match", False) :
		Reaction(Danger("wrong duplex mode", "type", "if_id", "duplex", "_static_duplex_req").PrintParent("type", "ip")
			, Recover("duplex is ok", "type", "if_id", "duplex", "_static_duplex_req").PrintParent("type", "ip")),

	("speed_match", False) :
		Reaction(Danger("port has a wrong speed", "type", "if_id", "speed", "speed_req").PrintParent("type", "ip")
			, Recover("port speed is good", "if_id", "speed", "speed_req").PrintParent("type", "ip")),

	("in_errors_ok", False) :
		Reaction(Warning("in errors growing fast for last 1000 seconds", "type", "if_id", "eth_in_errors", "eth_in_errors_speed", "_static_eth_port_error_speed_max").PrintParent("type", "ip"), delay = 1000),

	("out_errors_ok", False) :
		Reaction(Warning("out errors growing fast for last 1000 seconds", "type", "if_id", "eth_out_errors", "eth_out_errors_speed", "_static_eth_port_error_speed_max").PrintParent("type", "ip"), delay = 1000)
}
