from octopy import *

disk_module = {
	"static" : {
		"_static_disk_temp_max" :  40,
	},

	"sensor" : {
		"current_pending_sector" : 0,
		"hardware_ecc_recovered" : 0,
		"offline_uncorrectable"  : 0,
		"reallocated_sector_ct"  : 0,
		"reported_uncorrect"     : 0,
		"seek_error_rate"        : 0,
		"spin_retry_count"       : 0,
		"udma_crc_error_count"   : 0,

		"temperature_celsius"    : 0,
	},

	"var" : {
		"current_pending_sector_ok" : Match("current_pending_sector", 0),
		"offline_uncorrectable_ok"  : Match("offline_uncorrectable", 0),
		"reallocated_sector_ct_ok"  : Match("reallocated_sector_ct", 0),
		"reported_uncorrect_ok"     : Match("reported_uncorrect", 0),
		"spin_retry_count_ok"       : Match("spin_retry_count", 0),
		"udma_crc_error_count_ok"   : Match("udma_crc_error_count", 0),

		"temp_ok" : UpperArgThreshold("temperature_celsius", "_static_disk_temp_max"),
	},

	"react" : {
		Equals("current_pending_sector_ok", False) :
			Warning("DISK", "current_pending_sector growing : {current_pending_sector}").PrintParent("type", "node", "ip"),

		Equals("offline_uncorrectable_ok", False) :
			Warning("DISK", "offline_uncorrectable growing : {offline_uncorrectable}").PrintParent("type", "node", "ip"),

		Equals("reallocated_sector_ct_ok", False) :
			Warning("DISK", "reallocated_sector_ct growing : {reallocated_sector_ct}").PrintParent("type", "node", "ip"),

		Equals("reported_uncorrect_ok", False) :
			Warning("DISK", "reported_uncorrect growing : {reported_uncorrect}").PrintParent("type", "node", "ip"),

		Equals("spin_retry_count_ok", False) :
			Warning("DISK", "spin_retry_count growing : {spin_retry_count}").PrintParent("type", "node", "ip"),

		Equals("udma_crc_error_count_ok", False) :
			Warning("DISK", "udma_crc_error_count growing : {spin_retry_count}").PrintParent("type", "node", "ip"),

		Equals("temp_ok", False) :
			(Danger("TEMPERATURE", "disk temperature is above threshol({temperature_celsius})").PrintParent("type", "node", "ip")
				, Recover("disk temperature is back to normal({temperature_celsius})").PrintParent("type", "node", "ip"))
	}
}

#// ----------------------------------------- NODE --------------------------------------------

node_module = {
	"static" :
	{
		"_static_fork_rate_thr" : 50.0,
		"_static_la_thr1" : 9.0,
		"_static_la_thr2" : 17.0,
		"_static_system_ntpd_thr_neg" :  -2.0,
		"_static_system_ntpd_thr_pos" :  2.0,

		"_static_system_thr1" :  40,
		"_static_system_thr2" :  50,
	},

	"sensor" : {
		"temp" : 0,
		"la_1" : 0.0,
		"forks" : 0,
		"zombies" : 0,


		"check_tmp"   : 0,
		"check_home"  : 0,
		"check_clean" : 0,

		"check_nmond" : 0,

		"ntpd_drift" : 0.0,
	},

	"var" : {
		"la_1_acceptable" : UpperArgThreshold("la_1", "_static_la_thr1"),
		"la_1_sane"       : UpperArgThreshold("la_1", "_static_la_thr2"),

		"fork_rate" : CalcSpeed("forks"),
		"fork_rate_ok" : UpperArgThreshold("fork_rate", "_static_fork_rate_thr"),

		"zombies_ok" : Match("zombies", 0),

		"check_tmp_ok"   : Match("check_tmp", 0),
		"check_home_ok"  : Match("check_home", 0),
		"check_clean_ok" : Match("check_clean", 0),

		"check_nmond_ok" : Match("check_nmond", 0),

		"ntpd_drift_ok_1" : UpperArgThreshold("ntpd_drift", "_static_system_ntpd_thr_pos"),
		"ntpd_drift_ok_2" : LowerArgThreshold("ntpd_drift", "_static_system_ntpd_thr_neg"),

		"temp_ok" : UpperArgThreshold("temp", "_static_system_thr1"),
		"temp_acceptable" : UpperArgThreshold("temp", "_static_system_thr2"),
	},

	"react" : {
		Equals("fork_rate_ok", False).Delay(1000) :
			Warning("NODE", "High fork rate on {node} for last 1000 seconds, forks: {forks}, fork_rate: {fork_rate}"),

		Equals("zombies_ok", False).Delay(1000) :
			Warning("NODE", "({zombies}) zombies present on {node} for last 1000 seconds, run for your life!"),

		Equals("la_1_acceptable", False).Delay(1000) :
			(Warning("NODE", "LA({la_1}) on {node} exceeded threshold 1 for last 1000 seconds")
				, Recover("LA({la_1}) on {node} is back to normal")),

		Equals("la_1_sane", False) :
			Danger("NODE", "LA({la_1}) on {node} exceeded threshold 2 for last 1000 seconds"),

		Equals("check_tmp_ok", False) :
			(Danger("NODE", "could not access tmp on {node}")
				, Recover("tmp on {node} is accessible again")),
		Equals("check_home_ok", False) :
			(Danger("NODE", "could not access home on {node}")
				, Recover("home on {node} is accessible again")),
		Equals("check_clean_ok", False) :
			(Danger("NODE", "could not remove file on {node}")
				, Recover("remove file on {node} worked")),

		Equals("check_nmond_ok", False) :
			(Danger("NODE", "hopsa agent(nmond) not found on {node}")
				, Recover("hopsa agent(nmond) found on {node}")),

		Equals("ntpd_drift_ok_1", False) :
			(Danger("NODE", "ntpd drift({ntpd_drift}) on {node} is too big", "ntpd_drift")
				, Recover("ntpd drift({ntpd_drift}) on {node} is ok")),

		Equals("ntpd_drift_ok_2", False) :
			(Danger("NODE", "ntpd drift({ntpd_drift}) on {node} is too big", "ntpd_drift")
				, Recover("ntpd drift({ntpd_drift}) on {node} is ok")),

		Equals("temp_ok", False) :
			(Warning("TEMPERATURE", "bad system temp on {node}")
				, Recover("system temp on {node} is ok")),

		Equals("temp_acceptable", False) :
			Critical("TEMPERATURE", "critical system temp on {node}")
	}
}

#// ----------------------------------------- CPU --------------------------------------------

cpu_module = {

	"static" : {
		"_static_temp_thr1" : 75,
		"_static_temp_thr2" : 80
	},

	"sensor" : {
		"temp" : 0,
	},

	"var" : {
		"cpu_temp_ok"         : UpperArgThreshold("temp", "_static_temp_thr1"),
		"cpu_temp_acceptable" : UpperArgThreshold("temp", "_static_temp_thr2"),
	},

	"react" : {
		Equals("cpu_temp_ok", False) :
			(Warning("TEMPERATURE", "bad cpu temp({temp})").PrintParent("type", "node", "ip")
				, Recover("cpu temp({temp}) is ok now ").PrintParent("type", "node", "ip")),

		Equals("cpu_temp_acceptable", False) :
			Critical("TEMPERATURE", "critical cpu temp({temp})").PrintParent("type", "node", "ip")
	}
}

#// ----------------------------------------- MEMORY --------------------------------------------

memory_module = {
	"sensor" : {
		"buffered" : 0,
		"cached" : 0,
		"free" : 0,
		"used" : 0
	},

	"var" : {
		"total_mem" : AggregateLongSum(EDependencyType.SELF
			, "buffered", "cached", "free", "used"),
		"total_mem_ok" : LowerArgThreshold("total_mem", "req_mem"),

	},

	"react" : {
		Equals("total_mem_ok", False) :
			(Danger("MEM", "total mem({total_mem}) reduced below check value({req_mem})").PrintParent("type", "node", "ip")
				, Recover("total mem({total_mem}) is ok").PrintParent("type", "node", "ip"))
	}
}

#// ----------------------------------------- ETH --------------------------------------------

ib_module = {
	"sensor" : {
		"state" : 0,
		"physical_state" : 0,

		"LinkRecovers" : 0,
		"LinkDowned" : 0,

		"SymbolErrors" : 0,
		"RcvErrors" : 0,
		"RcvRemotePhysErrors" : 0,
		"RcvSwRelayErrors" : 0,
		"XmtDiscards" : 0,
		"XmtConstraintErrors" : 0,
		"RcvConstraintErrors" : 0,
		"LinkIntegrityErrors" : 0,
		"ExcBufOverrunErrors" : 0,
		"VL15Dropped" : 0,
		"PortXmitData" : 0,
		"PortRcvData" : 0,
		"PortXmitPkts" : 0,
		"PortRcvPkts" : 0,
	},

	"react" : {
		NotEquals("state", 0) :
			Danger("IB", "IB link problem: state").PrintParent("type", "node", "ip"),
		NotEquals("physical_state", 0) :
			Danger("IB", "IB link problem: physical state").PrintParent("type", "node", "ip"),

		NotEquals("SymbolErrors", 0).Repeatable() :
			Warning("IB", "IB errros growing: SymbolErrors = {SymbolErrors}").PrintParent("type", "node", "ip"),
		NotEquals("RcvErrors", 0).Repeatable() :
			Warning("IB", "IB errros growing: RcvErrors = {RcvErrors}").PrintParent("type", "node", "ip"),
		NotEquals("RcvRemotePhysErrors", 0).Repeatable() :
			Warning("IB", "IB errros growing: RcvRemotePhysErrors = {RcvRemotePhysErrors}").PrintParent("type", "node", "ip"),
		NotEquals("RcvSwRelayErrors", 0).Repeatable() :
			Warning("IB", "IB errros growing: RcvSwRelayErrors = {RcvSwRelayErrors}").PrintParent("type", "node", "ip"),
		NotEquals("XmtDiscards", 0).Repeatable() :
			Warning("IB", "IB errros growing: XmtDiscards = {XmtDiscards}").PrintParent("type", "node", "ip"),
		NotEquals("XmtConstraintErrors", 0).Repeatable() :
			Warning("IB", "IB errros growing: XmtConstraintErrors = {XmtConstraintErrors}").PrintParent("type", "node", "ip"),
		NotEquals("RcvConstraintErrors", 0).Repeatable() :
			Warning("IB", "IB errros growing: RcvConstraintErrors = {RcvConstraintErrors}").PrintParent("type", "node", "ip"),
		NotEquals("LinkIntegrityErrors", 0).Repeatable() :
			Warning("IB", "IB errros growing: LinkIntegrityErrors = {LinkIntegrityErrors}").PrintParent("type", "node", "ip"),
		NotEquals("ExcBufOverrunErrors", 0).Repeatable() :
			Warning("IB", "IB errros growing: ExcBufOverrunErrors = {ExcBufOverrunErrors}").PrintParent("type", "node", "ip"),
		NotEquals("VL15Dropped", 0).Repeatable() :
			Warning("IB", "IB errros growing: VL15Dropped = {VL15Dropped}").PrintParent("type", "node", "ip"),
	}
}

eth_module = {
	"static" : {
		"_static_eth_err_speed_thr" : 10.0,

		"_static_eth_speed_req" : 1000,
		"_static_eth_duplex_req" : "full",
	},

	"sensor" : {
		"speed" : 0,
		"duplex" : "",

		"rx_errors" : 0,
		"tx_errors" : 0,

		"tx_dropped" : 0,
		"collisions" : 0,
	},

	"var" : {
		"speed_ok" : ArgMatch("speed", "_static_eth_speed_req"),
		"duplex_ok" : ArgMatch("duplex", "_static_eth_duplex_req"),

		"rx_errors_speed" : CalcSpeed("rx_errors"),
		"tx_errors_speed" : CalcSpeed("tx_errors"),

		"tx_dropped_speed" : CalcSpeed("tx_dropped"),
		"collisions_speed" : CalcSpeed("collisions"),

		"check_rx_errors" : UpperArgThreshold("rx_errors_speed", "_static_eth_err_speed_thr"),
		"check_tx_errors" : UpperArgThreshold("tx_errors_speed", "_static_eth_err_speed_thr"),

		"check_tx_dropped" : UpperArgThreshold("tx_dropped_speed", "_static_eth_err_speed_thr"),
		"check_collisions" : UpperArgThreshold("collisions_speed", "_static_eth_err_speed_thr"),
	},

	"react" : {
		Equals("speed_ok", False) :
			Danger("ETH", "speed({speed}) does not match requred speed({_static_eth_speed_req})").PrintParent("type", "node", "ip"),

		Equals("duplex_ok", False) :
			Danger("ETH", "duplex mode({duplex}) does not match requred mode({_static_eth_duplex_req})").PrintParent("type", "node", "ip"),

		Equals("check_rx_errors", False).Delay(1000) :
			Warning("ETH", "recieve errors({rx_errors}) growing fast for last 1000 seconds").PrintParent("type", "node", "ip"),

		Equals("check_tx_errors", False).Delay(1000) :
			Warning("ETH", "transm errors({tx_errors}) growing fast for last 1000 seconds").PrintParent("type", "node", "ip"),

		Equals("check_tx_dropped", False).Delay(1000) :
			Warning("ETH", "tranms dropped({tx_dropped}) growing fast for last 1000 seconds").PrintParent("type", "node", "ip"),

		Equals("check_collisions", False).Delay(1000) :
			Warning("ETH", "collisions({collisions}) growing fast for last 1000 seconds").PrintParent("type", "node", "ip"),
	}
}
