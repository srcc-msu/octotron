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
			Warning("current_pending_sector > 0", "type", "current_pending_sector").PrintParent("type", "node", "ip"),

		Equals("offline_uncorrectable_ok", False) :
			Warning("offline_uncorrectable > 0", "type", "offline_uncorrectable").PrintParent("type", "node", "ip"),

		Equals("reallocated_sector_ct_ok", False) :
			Warning("reallocated_sector_ct > 0", "type", "reallocated_sector_ct").PrintParent("type", "node", "ip"),

		Equals("reported_uncorrect_ok", False) :
			Warning("reported_uncorrect > 0", "type", "reported_uncorrect").PrintParent("type", "node", "ip"),

		Equals("spin_retry_count_ok", False) :
			Warning("spin_retry_count > 0", "type", "spin_retry_count").PrintParent("type", "node", "ip"),

		Equals("udma_crc_error_count_ok", False) :
			Warning("udma_crc_error_count > 0", "type", "spin_retry_count").PrintParent("type", "node", "ip"),

		Equals("temp_ok", False) :
			(Danger("disk temperature is above threshold", "type", "temperature_celsius").PrintParent("type", "node", "ip")
				, Recover("disk temperature is back to normal", "type", "temperature_celsius").PrintParent("type", "node", "ip"))
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
			Warning("High fork rate on node for last 1000 seconds", "type", "node", "ip", "forks", "fork_rate", "_static_fork_rate_thr"),

		Equals("zombies_ok", False).Delay(1000) :
			Warning("Zombie processes present for last 1000 seconds, run for your life!", "type", "node", "ip", "zombies"),

		Equals("la_1_acceptable", False).Delay(1000) :
			(Warning("LA on on the node exceeded threshold 1 for last 1000 seconds", "type", "node", "ip", "la_1", "_static_la_thr1")
				, Recover("LA is back to normal", "type", "node", "ip", "la_1")),

		Equals("la_1_sane", False) :
			Danger("LA on on the node exceeded threshold 2 for last 1000 seconds", "type", "node", "ip", "la_1", "_static_la_thr2"),

		Equals("check_tmp_ok", False) :
			(Danger("could not access tmp on node", "type", "node", "ip"), Recover("tmp on node is accessible again", "type", "node", "ip")),
		Equals("check_home_ok", False) :
			(Danger("could not access home on node", "type", "node", "ip"), Recover("home on node is accessible again", "type", "node", "ip")),
		Equals("check_clean_ok", False) :
			(Danger("could not remove file on node", "type", "node", "ip"), Recover("remove file on node worked", "type", "node", "ip")),

		Equals("check_nmond_ok", False) :
			(Danger("hopsa agent(nmond) not found", "type", "node", "ip"), Recover("hopsa agent(nmond) found", "type", "node", "ip")),

		Equals("ntpd_drift_ok_1", False) :
			(Danger("ntpd drift is too big", "type", "node", "ip", "ntpd_drift"), Recover("ntpd drift is ok", "type", "node", "ip", "ntpd_drift")),

		Equals("ntpd_drift_ok_2", False) :
			(Danger("ntpd drift is too big", "type", "node", "ip", "ntpd_drift"), Recover("ntpd drift is ok", "type", "node", "ip", "ntpd_drift")),

		Equals("temp_ok", False) :
			(Warning("bad system temp on node", "type", "node", "ip", "temp"), Recover("system temp on node is ok", "type", "node", "ip", "temp")),

		Equals("temp_acceptable", False) :
			Critical("critical system temp on node", "type", "node", "ip", "temp")
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
			(Warning("bad cpu temp", "type", "lid", "temp").PrintParent("type", "node", "ip")
				, Recover("cpu temp is ok now", "type", "lid", "temp").PrintParent("type", "node", "ip")),

		Equals("cpu_temp_acceptable", False) :
			Critical("critical cpu temp", "type", "lid", "temp").PrintParent("type", "node", "ip")
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
			Danger("total mem reduced below check value", "mem_total", "req_mem").PrintParent("type", "node", "ip")
				, Recover("total mem is ok", "mem_total", "req_mem").PrintParent("type", "node", "ip"))
	}
}

#// ----------------------------------------- ETH --------------------------------------------

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
			Danger("speed does not match requred speed", "descr", "speed", "_static_eth_speed_req").PrintParent("type", "node", "ip"),

		Equals("duplex_ok", False) :
			Danger("duplex mode does not match requred mode", "descr", "duplex", "_static_eth_duplex_req").PrintParent("type", "node", "ip"),

		Equals("check_rx_errors", False).Delay(1000) :
			Warning("recieve errors growing fast for last 1000 seconds", "descr", "rx_errors").PrintParent("type", "node", "ip"),

		Equals("check_tx_errors", False).Delay(1000) :
			Warning("transm errors growing fast for last 1000 seconds", "descr", "tx_errors").PrintParent("type", "node", "ip"),

		Equals("check_tx_dropped", False).Delay(1000) :
			Warning("tranms dropped growing fast for last 1000 seconds", "descr", "tx_dropped").PrintParent("type", "node", "ip"),

		Equals("check_collisions", False).Delay(1000) :
			Warning("collisions growing fast for last 1000 seconds", "descr", "collisions").PrintParent("type", "node", "ip"),
	}
}