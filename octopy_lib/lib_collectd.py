from octopy import *

def DiskModule(timeout = Minutes(10)):
	loc = "{in_n:node}"
	loc_s = "{in_n:type} {type}: "
	loc_l = "{in_n:node} {type}: "

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

			"temperature_ok" : UpperArgThreshold("temperature_celsius", "_static_disk_temp_max"),

			"cd_disk_total_errors" : AStrictNotMatchCount(True, EDependencyType.SELF
				, "current_pending_sector_ok"
				, "offline_uncorrectable_ok"
				, "reallocated_sector_ct_ok"
				, "reported_uncorrect_ok"
				, "spin_retry_count_ok"
				, "udma_crc_error_count_ok"),
		},

		"trigger" : {
			"disk_error" : NotEquals("cd_disk_total_errors", 0)
			"bad_temperature" : Equals("temperature_ok", false)
		}

		"react" : [
			Reaction("notify_disk_error")
				.On("disk_error")
				.Begin(Warning("tag", "DISK").Msg("loc", loc)
					.Msg("descr", loc_s + "udma_crc_error_count growing")
					.Msg("msg"  , loc_l + "udma_crc_error_count growing : {spin_retry_count}")),

			Reaction("notify_bad_temperature")
				.On("bad_temperature")
				.Begin(Danger("tag", "TEMPERATURE").Msg("loc", loc)
					.Msg("descr", loc_s + "disk temperature is above threshol")
					.Msg("msg"  , loc_l + "disk temperature is above threshol({temperature_celsius}"))
				.End(Recover("tag", "TEMPERATURE").Msg("loc", loc)
					.Msg("descr", loc_s + "disk temperature is back to normal")
					.Msg("msg"  , loc_l + "disk temperature is back to normal({temperature_celsius})")),
		]
	}

#// ----------------------------------------- NODE --------------------------------------------

def ExperimentalNodeModule(timeout = Minutes(10)):
	loc = "{node}"
	loc_s = "{type}: "
	loc_l = "{node}: "

	return {
		"var" : {
			"la_state" : Interval("la_1", 3.0, 33.0),

			"node_free_fail" : StrictLogicalAnd("task_not_present", "la_free_fail"),
			"node_busy_fail" : StrictLogicalAnd("task_present", "la_busy_fail"),
		},

		"trigger" : {
			"task_present" : Manual()

			"high_la_free" : Equals("la_free_state", 1),
			"high_la_busy" : Equals("la_busy_state", 2),
		},

		"react" : [
			Reaction("notify_high_la_free")
				.Off("task_present")
				.On("high_la_free", 0, 1000)
				.Begin(Warning("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "LA exceeded 3.0 for last 1000 seconds, no running task")
					.Msg("msg"  , loc_l + "LA({la_1}) exceeded 3.0 for last 1000 seconds, no running task")),

			Reaction("notify_high_la_busy")
				.On(task_present)
				.On("high_la_busy", 0, 1000)
				.Begin(Warning("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "LA exceeded 33.0 for last 1000 seconds, user task presents")
					.Msg("msg"  , loc_l + "LA({la_1}) exceeded 33.0 for last 1000 seconds, user task presents")),

		]
	}

def NodeModule(timeout = Minutes(10)):
	loc = "{node}"
	loc_s = "{type}: "
	loc_l = "{node}: "

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
		},

		"var" : {
			"ntpd_drift_state" : Interval("ntpd_drift", -2.0, 2.0),
			"temp_state" : Interval("temp", 40, 50),
			"temp_ok" : NotMatch("temp_state", 2),

			"fork_rate" : Speed("forks"),
			"fork_rate_ok" : UpperArgThreshold("fork_rate", "_static_fork_rate_thr"),

			"zombies_ok" : Match("zombies", 0),

			"check_tmp_ok"   : Match("check_tmp", 0),
			"check_home_ok"  : Match("check_home", 0),
			"check_clean_ok" : Match("check_clean", 0),

			"check_nmond_ok" : Match("check_nmond", 0),

			"cd_node_total_errors" : AStrictNotMatchCount(True, EDependencyType.SELF
				, "temp_ok"
				, "fork_rate_ok"
				, "zombies_ok"
				, "check_tmp_ok"
				, "check_home_ok"
				, "check_clean_ok"
				, "check_nmond_ok")

		},

		"react" : {
			Equals("fork_rate_ok", False).Delay(1000) :
				Warning("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "high fork rate on for last 1000 seconds")
					.Msg("msg"  , loc_l + "high fork rate on for last 1000 seconds, forks: {forks}, fork_rate: {fork_rate}"),

			Equals("zombies_ok", False).Delay(1000) :
				Warning("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "zombies present for last 1000 seconds")
					.Msg("msg"  , loc_l + "({zombies}) zombies present for last 1000 seconds, run for your life!"),

			Equals("check_tmp_ok", False) :
				( Danger("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "could not access tmp")
					.Msg("msg"  , loc_l + "could not access tmp")
				, Recover("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "tmp is accessible again")
					.Msg("msg"  , loc_l + "tmp is accessible again")),
			Equals("check_home_ok", False) :
				( Danger("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "could not access home")
					.Msg("msg"  , loc_l + "could not access home")
				, Recover("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "home is accessible again")
					.Msg("msg"  , loc_l + "home is accessible again")),
			Equals("check_clean_ok", False) :
				( Danger("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "could not remove file")
					.Msg("msg"  , loc_l + "could not remove file")
				, Recover("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "remove file worked")
					.Msg("msg"  , loc_l + "remove file worked")),

			Equals("check_nmond_ok", False) :
				( Danger("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "hopsa agent(nmond) not found")
					.Msg("msg"  , loc_l + "hopsa agent(nmond) not found")
				, Recover("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "hopsa agent(nmond) found")
					.Msg("msg"  , loc_l + "hopsa agent(nmond) found")),

			NotEquals("ntpd_drift_state", 1) :
				( Danger("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "ntpd drift is too big")
					.Msg("msg"  , loc_l + "ntpd drift({ntpd_drift}) is too big")
				, Recover("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "ntpd drift is ok")
					.Msg("msg"  , loc_l + "ntpd drift({ntpd_drift}) is ok")),

			NotEquals("temp_state", 0) :
				( Warning("tag", "TEMPERATURE").Msg("loc", loc)
					.Msg("descr", loc_s + "bad system temp")
					.Msg("msg"  , loc_l + "bad system temp")
				, Recover("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "system temp is ok")
					.Msg("msg"  , loc_l + "system temp is ok")),

			Equals("temp_state", 2) :
				Critical("tag", "TEMPERATURE").Msg("loc", loc)
					.Msg("descr", loc_s + "critical system temp")
					.Msg("msg"  , loc_l + "critical system temp"),
		}
	}

#// ----------------------------------------- CPU --------------------------------------------

def CpuModule(timeout = Minutes(10)):
	loc = "{in_n:node}"
	loc_s = "{in_n:type} {type}: "
	loc_l = "{in_n:node} {type}: "

	return {
		"sensor" : {
			"temp" : Long(timeout),
		},

		"var" : {
			"temp_state" : Interval("temp", 75, 80),
		},

		"react" : {
			NotEquals("temp_state", 0) :
				( Warning("tag", "TEMPERATURE").Msg("loc", loc)
					.Msg("descr", loc_s + "bad temp")
					.Msg("msg"  , loc_l + "bad temp({temp})")
				, Recover("tag", "TEMPERATURE").Msg("loc", loc)
					.Msg("descr", loc_s + "temp is ok now ")
					.Msg("msg"  , loc_l + "temp({temp}) is ok now ")),

			Equals("temp_state", 2) :
				Critical("tag", "TEMPERATURE").Msg("loc", loc)
					.Msg("descr", loc_s + "critical temp")
					.Msg("msg"  , loc_l + "critical temp({temp})"),
		}
	}

#// ----------------------------------------- MEMORY --------------------------------------------

def MemoryModule(timeout = Minutes(10)):
	loc = "{in_n:node}"
	loc_s = "{in_n:type} {type}: "
	loc_l = "{in_n:node} {type}: "

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

		"cd_mem_total_errors" : AStrictNotMatchCount(True, EDependencyType.SELF
			, "total_memory_ok")
	},

	"react" : {
		Equals("total_memory_ok", False) :
			( Danger("tag", "MEM").Msg("loc", loc)
				.Msg("descr", loc_s + "total mem reduced below check value")
				.Msg("msg"  , loc_l + "total mem({total}) reduced below check value({req_mem})")
			, Recover("tag", "MEM").Msg("loc", loc)
				.Msg("descr", loc_s + "total mem is ok")
				.Msg("msg"  , loc_l + "total mem({total}) is ok")),
	}
}

#// ----------------------------------------- ETH --------------------------------------------

def IBModule(timeout = Minutes(10)):
	loc = "{in_n:node}"
	loc_s = "{in_n:type} {type}: "
	loc_l = "{in_n:node} {type}: "

	return {
		"const" : {
			"_static_ib_err_speed_thr" : 10.0,
		},

		"sensor" : {
			"state" : String(timeout),
			"physical_state" : String(timeout),

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

		"var" : {
			"SymbolErrors_speed" : Speed("SymbolErrors"),
			"RcvErrors_speed" : Speed("RcvErrors"),
			"RcvRemotePhysErrors_speed" : Speed("RcvRemotePhysErrors"),
			"RcvSwRelayErrors_speed" : Speed("RcvSwRelayErrors"),
			"XmtDiscards_speed" : Speed("XmtDiscards"),
			"XmtConstraintErrors_speed" : Speed("XmtConstraintErrors"),
			"RcvConstraintErrors_speed" : Speed("RcvConstraintErrors"),
			"LinkIntegrityErrors_speed" : Speed("LinkIntegrityErrors"),
			"ExcBufOverrunErrors_speed" : Speed("ExcBufOverrunErrors"),
			"VL15Dropped_speed" : Speed("VL15Dropped"),

			"state_ok" : Match("state", "Active"),
			"physical_state_ok" : Match("physical_state", "LinkUp"),

			"SymbolErrors_check" : UpperArgThreshold("SymbolErrors_speed", "_static_ib_err_speed_thr"),
			"RcvErrors_check" : UpperArgThreshold("RcvErrors_speed", "_static_ib_err_speed_thr"),
			"RcvRemotePhysErrors_check" : UpperArgThreshold("RcvRemotePhysErrors_speed", "_static_ib_err_speed_thr"),
			"RcvSwRelayErrors_check" : UpperArgThreshold("RcvSwRelayErrors_speed", "_static_ib_err_speed_thr"),
			"XmtDiscards_check" : UpperArgThreshold("XmtDiscards_speed", "_static_ib_err_speed_thr"),
			"XmtConstraintErrors_check" : UpperArgThreshold("XmtConstraintErrors_speed", "_static_ib_err_speed_thr"),
			"RcvConstraintErrors_check" : UpperArgThreshold("RcvConstraintErrors_speed", "_static_ib_err_speed_thr"),
			"LinkIntegrityErrors_check" : UpperArgThreshold("LinkIntegrityErrors_speed", "_static_ib_err_speed_thr"),
			"ExcBufOverrunErrors_check" : UpperArgThreshold("ExcBufOverrunErrors_speed", "_static_ib_err_speed_thr"),
			"VL15Dropped_check" : UpperArgThreshold("VL15Dropped_speed", "_static_ib_err_speed_thr"),

			"cd_ib_total_errors" : AStrictNotMatchCount(True, EDependencyType.SELF
				, "state_ok"
				, "physical_state_ok"
				, "SymbolErrors_check"
				, "RcvErrors_check"
				, "RcvRemotePhysErrors_check"
				, "RcvSwRelayErrors_check"
				, "XmtDiscards_check"
				, "XmtConstraintErrors_check"
				, "RcvConstraintErrors_check"
				, "LinkIntegrityErrors_check"
				, "ExcBufOverrunErrors_check"
				, "VL15Dropped_check"),
		},

		"react" : {
			Equals("state_ok", False) :
				Danger("tag", "IB").Msg("loc", loc)
					.Msg("descr", loc_s + "IB link problem: state")
					.Msg("msg"  , loc_l + "IB link problem: {state}"),
			Equals("physical_state", False) :
				Danger("tag", "IB").Msg("loc", loc)
					.Msg("descr", loc_s + "IB link problem: physical state")
					.Msg("msg"  , loc_l + "IB link problem: {physical_state}"),

			NotEquals("SymbolErrors_check", False).Delay(1000) :
				Warning("tag", "IB").Msg("loc", loc)
					.Msg("descr", loc_s + "IB errros growing: SymbolErrors")
					.Msg("msg"  , loc_l + "IB errros growing: SymbolErrors({SymbolErrors})"),
			NotEquals("RcvErrors_check", False).Delay(1000) :
				Warning("tag", "IB").Msg("loc", loc)
					.Msg("descr", loc_s + "IB errros growing: RcvErrors")
					.Msg("msg"  , loc_l + "IB errros growing: RcvErrors({RcvErrors})"),
			NotEquals("RcvRemotePhysErrors_check", False).Delay(1000) :
				Warning("tag", "IB").Msg("loc", loc)
					.Msg("descr", loc_s + "IB errros growing: RcvRemotePhysErrors")
					.Msg("msg"  , loc_l + "IB errros growing: RcvRemotePhysErrors({RcvRemotePhysErrors})"),
			NotEquals("RcvSwRelayErrors_check", False).Delay(1000) :
				Warning("tag", "IB").Msg("loc", loc)
					.Msg("descr", loc_s + "IB errros growing: RcvSwRelayErrors")
					.Msg("msg"  , loc_l + "IB errros growing: RcvSwRelayErrors({RcvSwRelayErrors})"),
			NotEquals("XmtDiscards_check", False).Delay(1000) :
				Warning("tag", "IB").Msg("loc", loc)
					.Msg("descr", loc_s + "IB errros growing: XmtDiscards")
					.Msg("msg"  , loc_l + "IB errros growing: XmtDiscards({XmtDiscards})"),
			NotEquals("XmtConstraintErrors_check", False).Delay(1000) :
				Warning("tag", "IB").Msg("loc", loc)
					.Msg("descr", loc_s + "IB errros growing: XmtConstraintErrors")
					.Msg("msg"  , loc_l + "IB errros growing: XmtConstraintErrors({XmtConstraintErrors})"),
			NotEquals("RcvConstraintErrors_check", False).Delay(1000) :
				Warning("tag", "IB").Msg("loc", loc)
					.Msg("descr", loc_s + "IB errros growing: RcvConstraintErrors")
					.Msg("msg"  , loc_l + "IB errros growing: RcvConstraintErrors({RcvConstraintErrors})"),
			NotEquals("LinkIntegrityErrors_check", False).Delay(1000) :
				Warning("tag", "IB").Msg("loc", loc)
					.Msg("descr", loc_s + "IB errros growing: LinkIntegrityErrors")
					.Msg("msg"  , loc_l + "IB errros growing: LinkIntegrityErrors({LinkIntegrityErrors})"),
			NotEquals("ExcBufOverrunErrors_check", False).Delay(1000) :
				Warning("tag", "IB").Msg("loc", loc)
					.Msg("descr", loc_s + "IB errros growing: ExcBufOverrunErrors")
					.Msg("msg"  , loc_l + "IB errros growing: ExcBufOverrunErrors({ExcBufOverrunErrors})"),
			NotEquals("VL15Dropped_check", False).Delay(1000) :
				Warning("tag", "IB").Msg("loc", loc)
					.Msg("descr", loc_s + "IB errros growing: VL15Dropped")
					.Msg("msg"  , loc_l + "IB errros growing: VL15Dropped({VL15Dropped})"),
		}
	}

def EthModule(timeout = Minutes(10)):
	loc = "{in_n:node}"
	loc_s = "{in_n:type} {type}: "
	loc_l = "{in_n:node} {type}: "

	return {
		"static" : {
			"_static_eth_err_speed_thr" : 10.0
		},

		"sensor" : {
			"rx_errors" : Long(timeout),
			"tx_errors" : Long(timeout),

			"tx_dropped" : Long(timeout),
			"collisions" : Long(timeout),
		},

		"var" : {
			"rx_errors_speed" : Speed("rx_errors"),
			"tx_errors_speed" : Speed("tx_errors"),

			"tx_dropped_speed" : Speed("tx_dropped"),
			"collisions_speed" : Speed("collisions"),

			"check_rx_errors" : UpperArgThreshold("rx_errors_speed", "_static_eth_err_speed_thr"),
			"check_tx_errors" : UpperArgThreshold("tx_errors_speed", "_static_eth_err_speed_thr"),

			"check_tx_dropped" : UpperArgThreshold("tx_dropped_speed", "_static_eth_err_speed_thr"),
			"check_collisions" : UpperArgThreshold("collisions_speed", "_static_eth_err_speed_thr"),

			"cd_eth_total_errors" : AStrictNotMatchCount(True, EDependencyType.SELF
				, "check_rx_errors"
				, "check_tx_errors"
				, "check_tx_dropped"
				, "check_collisions")
		},

		"react" : {
			Equals("check_rx_errors", False).Delay(1000) :
				Warning("tag", "ETH").Msg("loc", loc)
					.Msg("descr", loc_s + "recieve errors growing fast for last 1000 seconds")
					.Msg("msg"  , loc_l + "recieve errors({rx_errors}) growing fast for last 1000 seconds"),

			Equals("check_tx_errors", False).Delay(1000) :
				Warning("tag", "ETH").Msg("loc", loc)
					.Msg("descr", loc_s + "transm errors growing fast for last 1000 seconds")
					.Msg("msg"  , loc_l + "transm errors({tx_errors}) growing fast for last 1000 seconds"),

			Equals("check_tx_dropped", False).Delay(1000) :
				Warning("tag", "ETH").Msg("loc", loc)
					.Msg("descr", loc_s + "tranms dropped growing fast for last 1000 seconds")
					.Msg("msg"  , loc_l + "tranms dropped({tx_dropped}) growing fast for last 1000 seconds"),

			Equals("check_collisions", False).Delay(1000) :
				Warning("tag", "ETH").Msg("loc", loc)
					.Msg("descr", loc_s + "collisions growing fast for last 1000 seconds")
					.Msg("msg"  , loc_l + "collisions({collisions}) growing fast for last 1000 seconds"),
		}
	}
