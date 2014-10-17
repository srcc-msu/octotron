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
			Warning("tag", "DISK")
				.Msg("descr", "current_pending_sector growing")
				.Msg("msg", "disk in {in_n:node} current_pending_sector growing : {current_pending_sector}"),

		Equals("offline_uncorrectable_ok", False) :
			Warning("tag", "DISK")
				.Msg("descr", "offline_uncorrectable growing")
				.Msg("msg", "disk in {in_n:node} offline_uncorrectable growing : {offline_uncorrectable}"),

		Equals("reallocated_sector_ct_ok", False) :
			Warning("tag", "DISK")
				.Msg("descr", "reallocated_sector_ct growing")
				.Msg("msg", "disk in {in_n:node} reallocated_sector_ct growing : {reallocated_sector_ct}"),

		Equals("reported_uncorrect_ok", False) :
			Warning("tag", "DISK")
				.Msg("descr", "reported_uncorrect growing")
				.Msg("msg", "disk in {in_n:node} reported_uncorrect growing : {reported_uncorrect}"),

		Equals("spin_retry_count_ok", False) :
			Warning("tag", "DISK")
				.Msg("descr", "spin_retry_count growing")
				.Msg("msg", "disk in {in_n:node} spin_retry_count growing : {spin_retry_count}"),

		Equals("udma_crc_error_count_ok", False) :
			Warning("tag", "DISK")
				.Msg("descr", "udma_crc_error_count growing")
				.Msg("msg", "disk in {in_n:node} udma_crc_error_count growing : {spin_retry_count}"),

		Equals("temp_ok", False) : (
			Danger("tag", "TEMPERATURE")
				.Msg("descr", "disk temperature is above threshol")
				.Msg("msg", "disk temperature is above threshol({temperature_celsius})"),
			, Recover("tag", "TEMPERATURE")
				.Msg("descr", "disk temperature is back to normal"))
				.Msg("msg", "disk temperature is back to normal({temperature_celsius})")),
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
			Warning("tag", "NODE")
				.Msg("descr", "High fork rate on node for last 1000 seconds")
				.Msg("msg", "High fork rate on {node} for last 1000 seconds, forks: {forks}, fork_rate: {fork_rate}"),

		Equals("zombies_ok", False).Delay(1000) :
			Warning("tag", "NODE")
				.Msg("({zombies}) zombies present on {node} for last 1000 seconds, run for your life!"),

		Equals("la_1_acceptable", False).Delay(1000) :
			( Warning("tag", "NODE")
				.Msg("descr", "LA on node exceeded threshold 1 for last 1000 seconds")
				.Msg("msg", "LA({la_1}) on {node} exceeded threshold 1 for last 1000 seconds"),
			, Recover("tag", "NODE")
				.Msg("descr", "LA on node is back to normal")),
				.Msg("msg", "LA({la_1}) on {node} is back to normal")),

		Equals("la_1_sane", False) :
			Danger("tag", "NODE")
			.Msg("LA({la_1}) on {node} exceeded threshold 2 for last 1000 seconds"),

		Equals("check_tmp_ok", False) :
			( Danger("tag", "NODE")
				.Msg("descr", "could not access tmp on node")
				.Msg("msg", "could not access tmp on {node}"),
			, Recover("tag", "NODE")
				.Msg("descr", "tmp on node is accessible again")),
				.Msg("msg", "tmp on {node} is accessible again")),
		Equals("check_home_ok", False) :
			( Danger("tag", "NODE")
				.Msg("descr", "could not access home on node")
				.Msg("msg", "could not access home on {node}"),
			, Recover("tag", "NODE")
				.Msg("descr", "home on node is accessible again")),
				.Msg("msg", "home on {node} is accessible again")),
		Equals("check_clean_ok", False) :
			( Danger("tag", "NODE")
				.Msg("descr", "could not remove file on node")
				.Msg("msg", "could not remove file on {node}"),
			, Recover("tag", "NODE")
				.Msg("descr", "remove file on node worked")),
				.Msg("msg", "remove file on {node} worked")),

		Equals("check_nmond_ok", False) :
			( Danger("tag", "NODE")
				.Msg("descr", "hopsa agent(nmond) not found on node")
				.Msg("msg", "hopsa agent(nmond) not found on {node}"),
			, Recover("tag", "NODE")
				.Msg("descr", "hopsa agent(nmond) found on node")),
				.Msg("msg", "hopsa agent(nmond) found on {node}")),

		Equals("ntpd_drift_ok_1", False) :
			( Danger("tag", "NODE")
				.Msg("descr", "ntpd drift on node is too big")
				.Msg("msg", "ntpd drift({ntpd_drift}) on {node} is too big"),
			, Recover("tag", "NODE")
				.Msg("descr", "ntpd drift on node is ok")),
				.Msg("msg", "ntpd drift({ntpd_drift}) on {node} is ok")),

		Equals("ntpd_drift_ok_2", False) :
			( Danger("tag", "NODE")
				.Msg("descr", "ntpd drift on node is too big")
				.Msg("msg", "ntpd drift({ntpd_drift}) on {node} is too big"),
			, Recover("tag", "NODE")
				.Msg("descr", "ntpd drift on node is ok")),
				.Msg("msg", "ntpd drift({ntpd_drift}) on {node} is ok")),

		Equals("temp_ok", False) :
			( Warning("tag", "TEMPERATURE")
				.Msg("descr", "bad system temp on node")
				.Msg("msg", "bad system temp on {node}"),
			, Recover("tag", "NODE")
				.Msg("descr", "system temp on node is ok")),
				.Msg("msg", "system temp on {node} is ok")),

		Equals("temp_acceptable", False) :
			Critical("tag", "TEMPERATURE")
				.Msg("descr", "critical system temp on node")
				.Msg("msg", "critical system temp on {node}"),
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
			( Warning("tag", "TEMPERATURE")
				.Msg("descr", "bad cpu temp")
				.Msg("msg", "bad cpu temp({temp})  node {in_n:node}"),
			, Recover("tag", "TEMPERATURE")
				.Msg("descr", "cpu temp({temp}) is ok now ")
				.Msg("msg", "cpu temp({temp})  node {in_n:node} is ok now "),

		Equals("cpu_temp_acceptable", False) :
			( Critical("tag", "TEMPERATURE")
				.Msg("descr", "critical cpu temp")
				.Msg("msg", "critical cpu temp({temp})  node {in_n:node}")),
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
			( Danger("tag", "MEM")
				.Msg("descr", "total mem({total_mem})  node {in_n:node} reduced below check value({req_mem})")
				.Msg("msg", "total mem({total_mem})  node {in_n:node} reduced below check value({req_mem})"),
			, Recover("tag", "MEM")
				.Msg("descr", "total mem({total_mem})  node {in_n:node} is ok")
				.Msg("msg", "total mem({total_mem})  node {in_n:node} is ok")),
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
			Danger("tag", "IB")
				.Msg("descr", "IB link problem on node: state")
				.Msg("msg", "IB link problem on {in_n:node}: state"),
		NotEquals("physical_state", 0) :
			Danger("tag", "IB")
				.Msg("descr", "IB link problem on node: physical state")
				.Msg("msg", "IB link problem on {in_n:node}: physical state"),

		NotEquals("SymbolErrors", 0).Repeatable() :
			Warning("tag", "IB")
				.Msg("descr", "IB errros growing on node: SymbolErrors")
				.Msg("msg", "IB errros growing on {in_n:node}: SymbolErrors = {SymbolErrors}"),
		NotEquals("RcvErrors", 0).Repeatable() :
			Warning("tag", "IB")
				.Msg("descr", "IB errros growing on node: RcvErrors")
				.Msg("msg", "IB errros growing on {in_n:node}: RcvErrors = {RcvErrors}"),
		NotEquals("RcvRemotePhysErrors", 0).Repeatable() :
			Warning("tag", "IB")
				.Msg("descr", "IB errros growing on node: RcvRemotePhysErrors")
				.Msg("msg", "IB errros growing on {in_n:node}: RcvRemotePhysErrors = {RcvRemotePhysErrors}"),
		NotEquals("RcvSwRelayErrors", 0).Repeatable() :
			Warning("tag", "IB")
				.Msg("descr", "IB errros growing on node: RcvSwRelayErrors")
				.Msg("msg", "IB errros growing on {in_n:node}: RcvSwRelayErrors = {RcvSwRelayErrors}"),
		NotEquals("XmtDiscards", 0).Repeatable() :
			Warning("tag", "IB")
				.Msg("descr", "IB errros growing on node: XmtDiscards")
				.Msg("msg", "IB errros growing on {in_n:node}: XmtDiscards = {XmtDiscards}"),
		NotEquals("XmtConstraintErrors", 0).Repeatable() :
			Warning("tag", "IB")
				.Msg("descr", "IB errros growing on node: XmtConstraintErrors")
				.Msg("msg", "IB errros growing on {in_n:node}: XmtConstraintErrors = {XmtConstraintErrors}"),
		NotEquals("RcvConstraintErrors", 0).Repeatable() :
			Warning("tag", "IB")
				.Msg("descr", "IB errros growing on node: RcvConstraintErrors")
				.Msg("msg", "IB errros growing on {in_n:node}: RcvConstraintErrors = {RcvConstraintErrors}"),
		NotEquals("LinkIntegrityErrors", 0).Repeatable() :
			Warning("tag", "IB")
				.Msg("descr", "IB errros growing on node: LinkIntegrityErrors")
				.Msg("msg", "IB errros growing on {in_n:node}: LinkIntegrityErrors = {LinkIntegrityErrors}"),
		NotEquals("ExcBufOverrunErrors", 0).Repeatable() :
			Warning("tag", "IB")
				.Msg("descr", "IB errros growing on node: ExcBufOverrunErrors")
				.Msg("msg", "IB errros growing on {in_n:node}: ExcBufOverrunErrors = {ExcBufOverrunErrors}"),
		NotEquals("VL15Dropped", 0).Repeatable() :
			Warning("tag", "IB")
				.Msg("descr", "IB errros growing on node: VL15Dropped")
				.Msg("msg", "IB errros growing on {in_n:node}: VL15Dropped = {VL15Dropped}"),
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
			Danger("tag", "ETH")
				.Msg("descr", "speed does not match requred speed")
				.Msg("msg", "speed({speed}) does not match requred speed({_static_eth_speed_req})"),

		Equals("duplex_ok", False) :
			Danger("tag", "ETH")
				.Msg("descr", "duplex mode does not match requred mode")
				.Msg("msg", "duplex mode({duplex}) does not match requred mode({_static_eth_duplex_req})"),

		Equals("check_rx_errors", False).Delay(1000) :
			Warning("tag", "ETH")
				.Msg("descr", "recieve errors growing fast for last 1000 seconds")
				.Msg("msg", "recieve errors({rx_errors}) growing fast for last 1000 seconds"),

		Equals("check_tx_errors", False).Delay(1000) :
			Warning("tag", "ETH")
				.Msg("descr", "transm errors growing fast for last 1000 seconds")
				.Msg("msg", "transm errors({tx_errors}) growing fast for last 1000 seconds"),

		Equals("check_tx_dropped", False).Delay(1000) :
			Warning("tag", "ETH")
				.Msg("descr", "tranms dropped growing fast for last 1000 seconds")
				.Msg("msg", "tranms dropped({tx_dropped}) growing fast for last 1000 seconds"),

		Equals("check_collisions", False).Delay(1000) :
			Warning("tag", "ETH")
				.Msg("descr", "collisions growing fast for last 1000 seconds")
				.Msg("msg", "collisions({collisions}) growing fast for last 1000 seconds"),
	}
}
