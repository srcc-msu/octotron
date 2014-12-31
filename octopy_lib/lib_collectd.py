from octopy import *

def DiskModule(timeout = Minutes(10)):
	return {
	"static" : {
		"_static_disk_temp_max" :  40,
	},

	"sensor" : {
		"current_pending_sector" : Long(timeout),
		"hardware_ecc_recovered" : Long(timeout),
		"offline_uncorrectable"  : Long(timeout),
		"reallocated_sector_ct"  : Long(timeout),
		"reported_uncorrect"     : Long(timeout),
		"seek_error_rate"        : Long(timeout),
		"spin_retry_count"       : Long(timeout),
		"udma_crc_error_count"   : Long(timeout),

		"temperature_celsius"    : Long(timeout),
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
			Warning("tag", "DISK").Msg("loc", "{in_n:node}")
				.Msg("descr", "current_pending_sector growing")
				.Msg("msg"  , "disk on {in_n:node} current_pending_sector growing : {current_pending_sector}"),

		Equals("offline_uncorrectable_ok", False) :
			Warning("tag", "DISK").Msg("loc", "{in_n:node}")
				.Msg("descr", "offline_uncorrectable growing")
				.Msg("msg"  , "disk on {in_n:node} offline_uncorrectable growing : {offline_uncorrectable}"),

		Equals("reallocated_sector_ct_ok", False) :
			Warning("tag", "DISK").Msg("loc", "{in_n:node}")
				.Msg("descr", "reallocated_sector_ct growing")
				.Msg("msg"  , "disk on {in_n:node} reallocated_sector_ct growing : {reallocated_sector_ct}"),

		Equals("reported_uncorrect_ok", False) :
			Warning("tag", "DISK").Msg("loc", "{in_n:node}")
				.Msg("descr", "reported_uncorrect growing")
				.Msg("msg"  , "disk on {in_n:node} reported_uncorrect growing : {reported_uncorrect}"),

		Equals("spin_retry_count_ok", False) :
			Warning("tag", "DISK").Msg("loc", "{in_n:node}")
				.Msg("descr", "spin_retry_count growing")
				.Msg("msg"  , "disk on {in_n:node} spin_retry_count growing : {spin_retry_count}"),

		Equals("udma_crc_error_count_ok", False) :
			Warning("tag", "DISK").Msg("loc", "{in_n:node}")
				.Msg("descr", "udma_crc_error_count growing")
				.Msg("msg"  , "disk on {in_n:node} udma_crc_error_count growing : {spin_retry_count}"),

		Equals("temp_ok", False) :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{in_n:node}")
				.Msg("descr", "disk temperature is above threshol")
				.Msg("msg"  , "disk temperature on {in_n:node} is above threshol({temperature_celsius}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{in_n:node}")
				.Msg("descr", "disk temperature is back to normal")
				.Msg("msg"  , "disk temperature on {in_n:node} is back to normal({temperature_celsius})")),
	}
}

#// ----------------------------------------- NODE --------------------------------------------

def NodeModule(timeout = Minutes(10)):
	return {
		"static" :
		{
			"_static_fork_rate_thr" : 50.0,
		},

		"sensor" : {
			"temp" : Long(timeout),
			"forks" : Long(timeout),
			"zombies" : Long(timeout),

			"check_tmp"   : Long(timeout),
			"check_home"  : Long(timeout),
			"check_clean" : Long(timeout),
			"check_nmond" : Long(timeout),

			"ntpd_drift" : Double(timeout),
			"la_1" : Double(timeout),

			"task_id" : Long(timeout),
		},

		"var" : {
			"task_not_present" : Match("task_id", -1),
			"task_present" : NotMatch("task_id", -1),

			"la_1_free_state" : Interval("la_1", 3.0), "la_1_free_ok" : Match("la_1_free_state", 0),
			"la_1_busy_state" : Interval("la_1", 33.0), "la_1_busy_ok" : Match("la_1_busy_state", 0),

			"node_free_ok" : StrictLogicalAnd("task_not_present", "la_1_free_ok"),
			"node_busy_ok" : StrictLogicalAnd("task_present", "la_1_busy_ok"),

			"ntpd_drift_state" : Interval("ntpd_drift", -2.0, 2.0),
			"temp_state" : Interval("temp", 40, 50),

			"fork_rate" : Speed("forks"),
			"fork_rate_ok" : UpperArgThreshold("fork_rate", "_static_fork_rate_thr"),

			"zombies_ok" : Match("zombies", 0),

			"check_tmp_ok"   : Match("check_tmp", 0),
			"check_home_ok"  : Match("check_home", 0),
			"check_clean_ok" : Match("check_clean", 0),

			"check_nmond_ok" : Match("check_nmond", 0),
		},

		"react" : {
			Equals("fork_rate_ok", False).Delay(1000) :
				Warning("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "High fork rate on node for last 1000 seconds")
					.Msg("msg"  , "High fork rate on {node} for last 1000 seconds, forks: {forks}, fork_rate: {fork_rate}"),

			Equals("zombies_ok", False).Delay(1000) :
				Warning("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "zombies present on node for last 1000 seconds")
					.Msg("msg"  , "({zombies}) zombies present on {node} for last 1000 seconds, run for your life!"),

			Equals("node_free_ok", False).Delay(1000) :
				Warning("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "LA on *free* node exceeded 3.0 for last 1000 seconds")
					.Msg("msg"  , "LA({la_1}) on *free* {node} exceeded 3.0 for last 1000 seconds"),

			Equals("node_busy_ok", False).Delay(1000) :
				Warning("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "LA on node with task exceeded 33.0 for last 1000 seconds")
					.Msg("msg"  , "LA({la_1}) on {node} with task(id: {task_id}) exceeded 33.0 for last 1000 seconds"),

			Equals("check_tmp_ok", False) :
				( Danger("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "could not access tmp on node")
					.Msg("msg"  , "could not access tmp on {node}")
				, Recover("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "tmp on node is accessible again")
					.Msg("msg"  , "tmp on {node} is accessible again")),
			Equals("check_home_ok", False) :
				( Danger("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "could not access home on node")
					.Msg("msg"  , "could not access home on {node}")
				, Recover("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "home on node is accessible again")
					.Msg("msg"  , "home on {node} is accessible again")),
			Equals("check_clean_ok", False) :
				( Danger("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "could not remove file on node")
					.Msg("msg"  , "could not remove file on {node}")
				, Recover("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "remove file on node worked")
					.Msg("msg"  , "remove file on {node} worked")),

			Equals("check_nmond_ok", False) :
				( Danger("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "hopsa agent(nmond) not found on node")
					.Msg("msg"  , "hopsa agent(nmond) not found on {node}")
				, Recover("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "hopsa agent(nmond) found on node")
					.Msg("msg"  , "hopsa agent(nmond) found on {node}")),

			NotEquals("ntpd_drift_state", 1) :
				( Danger("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "ntpd drift on node is too big")
					.Msg("msg"  , "ntpd drift({ntpd_drift}) on {node} is too big")
				, Recover("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "ntpd drift on node is ok")
					.Msg("msg"  , "ntpd drift({ntpd_drift}) on {node} is ok")),

			NotEquals("temp_state", 0) :
				( Warning("tag", "TEMPERATURE").Msg("loc", "{node}")
					.Msg("descr", "bad system temp on node")
					.Msg("msg"  , "bad system temp on {node}")
				, Recover("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "system temp on node is ok")
					.Msg("msg"  , "system temp on {node} is ok")),

			Equals("temp_state", 2) :
				Critical("tag", "TEMPERATURE").Msg("loc", "{node}")
					.Msg("descr", "critical system temp on node")
					.Msg("msg"  , "critical system temp on {node}"),
		}
	}

#// ----------------------------------------- CPU --------------------------------------------



def CpuModule(timeout = Minutes(10)):
	return {
		"sensor" : {
			"temp" : Long(timeout),
		},

		"var" : {
			"temp_state" : Interval("temp", 75, 80),
		},

		"react" : {
			NotEquals("temp_state", 0) :
				( Warning("tag", "TEMPERATURE").Msg("loc", "{in_n:node}")
					.Msg("descr", "bad cpu temp")
					.Msg("msg"  , "bad cpu temp({temp})  node {in_n:node}")
				, Recover("tag", "TEMPERATURE").Msg("loc", "{in_n:node}")
					.Msg("descr", "cpu temp is ok now ")
					.Msg("msg"  , "cpu temp({temp})  node {in_n:node} is ok now ")),

			Equals("temp_state", 2) :
				Critical("tag", "TEMPERATURE").Msg("loc", "{in_n:node}")
					.Msg("descr", "critical cpu temp")
					.Msg("msg"  , "critical cpu temp({temp})  node {in_n:node}"),
		}
	}

#// ----------------------------------------- MEMORY --------------------------------------------

def MemoryModule(timeout = Minutes(10)):
	return {
	"sensor" : {
		"buffered" : Long(timeout),
		"cached" : Long(timeout),
		"free" : Long(timeout),
		"used" : Long(timeout),
		"total" : Long(timeout),
	},

	"var" : {
		"total_memory_ok" : LowerArgThreshold("total", "req_mem"),
	},

	"react" : {
		Equals("total_memory_ok", False) :
			( Danger("tag", "MEM").Msg("loc", "{in_n:node}")
				.Msg("descr", "total mem on node reduced below check value")
				.Msg("msg"  , "total mem({total}) on node {in_n:node} reduced below check value({req_mem})")
			, Recover("tag", "MEM").Msg("loc", "{in_n:node}")
				.Msg("descr", "total mem on node is ok")
				.Msg("msg"  , "total mem({total}) on node {in_n:node} is ok")),
	}
}

#// ----------------------------------------- ETH --------------------------------------------

def IBModule(timeout = Minutes(10)):
	return {
		"sensor" : {
			"state" : Long(timeout),
			"physical_state" : Long(timeout),

			"LinkRecovers" : Long(timeout),
			"LinkDowned" : Long(timeout),

			"SymbolErrors" : Long(timeout),
			"RcvErrors" : Long(timeout),
			"RcvRemotePhysErrors" : Long(timeout),
			"RcvSwRelayErrors" : Long(timeout),
			"XmtDiscards" : Long(timeout),
			"XmtConstraintErrors" : Long(timeout),
			"RcvConstraintErrors" : Long(timeout),
			"LinkIntegrityErrors" : Long(timeout),
			"ExcBufOverrunErrors" : Long(timeout),
			"VL15Dropped" : Long(timeout),
			"PortXmitData" : Long(timeout),
			"PortRcvData" : Long(timeout),
			"PortXmitPkts" : Long(timeout),
			"PortRcvPkts" : Long(timeout),
		},

		"react" : {
			NotEquals("state", 0) :
				Danger("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "IB link problem on node: state")
					.Msg("msg"  , "IB link problem on {in_n:node}: state"),
			NotEquals("physical_state", 0) :
				Danger("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "IB link problem on node: physical state")
					.Msg("msg"  , "IB link problem on {in_n:node}: physical state"),

			NotEquals("SymbolErrors", 0).Repeatable() :
				Warning("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "IB errros growing on node: SymbolErrors")
					.Msg("msg"  , "IB errros growing on {in_n:node}: SymbolErrors = {SymbolErrors}"),
			NotEquals("RcvErrors", 0).Repeatable() :
				Warning("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "IB errros growing on node: RcvErrors")
					.Msg("msg"  , "IB errros growing on {in_n:node}: RcvErrors = {RcvErrors}"),
			NotEquals("RcvRemotePhysErrors", 0).Repeatable() :
				Warning("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "IB errros growing on node: RcvRemotePhysErrors")
					.Msg("msg"  , "IB errros growing on {in_n:node}: RcvRemotePhysErrors = {RcvRemotePhysErrors}"),
			NotEquals("RcvSwRelayErrors", 0).Repeatable() :
				Warning("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "IB errros growing on node: RcvSwRelayErrors")
					.Msg("msg"  , "IB errros growing on {in_n:node}: RcvSwRelayErrors = {RcvSwRelayErrors}"),
			NotEquals("XmtDiscards", 0).Repeatable() :
				Warning("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "IB errros growing on node: XmtDiscards")
					.Msg("msg"  , "IB errros growing on {in_n:node}: XmtDiscards = {XmtDiscards}"),
			NotEquals("XmtConstraintErrors", 0).Repeatable() :
				Warning("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "IB errros growing on node: XmtConstraintErrors")
					.Msg("msg"  , "IB errros growing on {in_n:node}: XmtConstraintErrors = {XmtConstraintErrors}"),
			NotEquals("RcvConstraintErrors", 0).Repeatable() :
				Warning("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "IB errros growing on node: RcvConstraintErrors")
					.Msg("msg"  , "IB errros growing on {in_n:node}: RcvConstraintErrors = {RcvConstraintErrors}"),
			NotEquals("LinkIntegrityErrors", 0).Repeatable() :
				Warning("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "IB errros growing on node: LinkIntegrityErrors")
					.Msg("msg"  , "IB errros growing on {in_n:node}: LinkIntegrityErrors = {LinkIntegrityErrors}"),
			NotEquals("ExcBufOverrunErrors", 0).Repeatable() :
				Warning("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "IB errros growing on node: ExcBufOverrunErrors")
					.Msg("msg"  , "IB errros growing on {in_n:node}: ExcBufOverrunErrors = {ExcBufOverrunErrors}"),
			NotEquals("VL15Dropped", 0).Repeatable() :
				Warning("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "IB errros growing on node: VL15Dropped")
					.Msg("msg"  , "IB errros growing on {in_n:node}: VL15Dropped = {VL15Dropped}"),
		}
	}

def EthModule(timeout = Minutes(10)):
	return {
		"static" : {
			"_static_eth_err_speed_thr" : 10.0,

			"_static_eth_speed_req" : 1000,
			"_static_eth_duplex_req" : "full",
		},

		"sensor" : {
			"speed" : Long(timeout),

			"rx_errors" : Long(timeout),
			"tx_errors" : Long(timeout),

			"tx_dropped" : Long(timeout),
			"collisions" : Long(timeout),

			"duplex" : String(timeout),
		},

		"var" : {
			"speed_ok" : ArgMatch("speed", "_static_eth_speed_req"),
			"duplex_ok" : ArgMatch("duplex", "_static_eth_duplex_req"),

			"rx_errors_speed" : Speed("rx_errors"),
			"tx_errors_speed" : Speed("tx_errors"),

			"tx_dropped_speed" : Speed("tx_dropped"),
			"collisions_speed" : Speed("collisions"),

			"check_rx_errors" : UpperArgThreshold("rx_errors_speed", "_static_eth_err_speed_thr"),
			"check_tx_errors" : UpperArgThreshold("tx_errors_speed", "_static_eth_err_speed_thr"),

			"check_tx_dropped" : UpperArgThreshold("tx_dropped_speed", "_static_eth_err_speed_thr"),
			"check_collisions" : UpperArgThreshold("collisions_speed", "_static_eth_err_speed_thr"),
		},

		"react" : {
			Equals("speed_ok", False) :
				Danger("tag", "ETH").Msg("loc", "{in_n:node}")
					.Msg("descr", "speed does not match requred speed")
					.Msg("msg"  , "speed({speed}) does not match requred speed({_static_eth_speed_req}) on {in_n:node}"),

			Equals("duplex_ok", False) :
				Danger("tag", "ETH").Msg("loc", "{in_n:node}")
					.Msg("descr", "duplex mode does not match requred mode")
					.Msg("msg"  , "duplex mode({duplex}) does not match requred mode({_static_eth_duplex_req}) on {in_n:node}"),

			Equals("check_rx_errors", False).Delay(1000) :
				Warning("tag", "ETH").Msg("loc", "{in_n:node}")
					.Msg("descr", "recieve errors growing fast for last 1000 seconds")
					.Msg("msg"  , "recieve errors({rx_errors}) growing fast for last 1000 seconds on {in_n:node}"),

			Equals("check_tx_errors", False).Delay(1000) :
				Warning("tag", "ETH").Msg("loc", "{in_n:node}")
					.Msg("descr", "transm errors growing fast for last 1000 seconds")
					.Msg("msg"  , "transm errors({tx_errors}) growing fast for last 1000 seconds on {in_n:node}"),

			Equals("check_tx_dropped", False).Delay(1000) :
				Warning("tag", "ETH").Msg("loc", "{in_n:node}")
					.Msg("descr", "tranms dropped growing fast for last 1000 seconds")
					.Msg("msg"  , "tranms dropped({tx_dropped}) growing fast for last 1000 seconds on {in_n:node}"),

			Equals("check_collisions", False).Delay(1000) :
				Warning("tag", "ETH").Msg("loc", "{in_n:node}")
					.Msg("descr", "collisions growing fast for last 1000 seconds")
					.Msg("msg"  , "collisions({collisions}) growing fast for last 1000 seconds on {in_n:node}"),
		}
	}
