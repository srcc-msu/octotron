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
				.Msg("descr", "{type}: current_pending_sector growing")
				.Msg("msg"  , "{type}({in_n:node}): current_pending_sector growing : {current_pending_sector}"),

		Equals("offline_uncorrectable_ok", False) :
			Warning("tag", "DISK").Msg("loc", "{in_n:node}")
				.Msg("descr", "{type}: offline_uncorrectable growing")
				.Msg("msg"  , "{type}({in_n:node}): offline_uncorrectable growing : {offline_uncorrectable}"),

		Equals("reallocated_sector_ct_ok", False) :
			Warning("tag", "DISK").Msg("loc", "{in_n:node}")
				.Msg("descr", "{type}: reallocated_sector_ct growing")
				.Msg("msg"  , "{type}({in_n:node}): reallocated_sector_ct growing : {reallocated_sector_ct}"),

		Equals("reported_uncorrect_ok", False) :
			Warning("tag", "DISK").Msg("loc", "{in_n:node}")
				.Msg("descr", "{type}: reported_uncorrect growing")
				.Msg("msg"  , "{type}({in_n:node}): reported_uncorrect growing : {reported_uncorrect}"),

		Equals("spin_retry_count_ok", False) :
			Warning("tag", "DISK").Msg("loc", "{in_n:node}")
				.Msg("descr", "{type}: spin_retry_count growing")
				.Msg("msg"  , "{type}({in_n:node}): spin_retry_count growing : {spin_retry_count}"),

		Equals("udma_crc_error_count_ok", False) :
			Warning("tag", "DISK").Msg("loc", "{in_n:node}")
				.Msg("descr", "{type}: udma_crc_error_count growing")
				.Msg("msg"  , "{type}({in_n:node}): udma_crc_error_count growing : {spin_retry_count}"),

		Equals("temp_ok", False) :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{in_n:node}")
				.Msg("descr", "{type}: disk temperature is above threshol")
				.Msg("msg"  , "{type}({in_n:node}): disk temperature is above threshol({temperature_celsius}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{in_n:node}")
				.Msg("descr", "{type}: disk temperature is back to normal")
				.Msg("msg"  , "{type}({in_n:node}): disk temperature is back to normal({temperature_celsius})")),
	}
}

#// ----------------------------------------- NODE --------------------------------------------

def ExperimentalNodeModule(timeout = Minutes(10)):
	return {
		"var" : {
			"task_not_present" : Match("task_present", False),

			"la_1_free_state" : Interval("la_1", 3.0), "la_1_free_fail" : Match("la_1_free_state", 1),
			"la_1_busy_state" : Interval("la_1", 33.0), "la_1_busy_fail" : Match("la_1_busy_state", 1),

			"node_free_fail" : StrictLogicalAnd("task_not_present", "la_1_free_fail"),
			"node_busy_fail" : StrictLogicalAnd("task_present", "la_1_busy_fail"),
		},

		"react" : {
			Equals("node_free_fail", True).Delay(1000) :
				Warning("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: LA exceeded 3.0 for last 1000 seconds, no running task")
					.Msg("msg"  , "{type}({node}): LA({la_1}) exceeded 3.0 for last 1000 seconds, no running task"),

			Equals("node_busy_fail", True).Delay(1000) :
				Warning("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: LA exceeded 33.0 for last 1000 seconds, user task presents")
					.Msg("msg"  , "{type}({node}): LA({la_1}) exceeded 33.0 for last 1000 seconds, user task presents"),

		}
	}

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

			"task_present" : Long(UPDATE_TIME_NOT_SPECIFIED, False),
		},

		"var" : {
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
					.Msg("descr", "{type}: high fork rate on for last 1000 seconds")
					.Msg("msg"  , "{type}({node}): high fork rate on for last 1000 seconds, forks: {forks}, fork_rate: {fork_rate}"),

			Equals("zombies_ok", False).Delay(1000) :
				Warning("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: zombies present for last 1000 seconds")
					.Msg("msg"  , "{type}({node}): ({zombies}) zombies present for last 1000 seconds, run for your life!"),

			Equals("check_tmp_ok", False) :
				( Danger("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: could not access tmp")
					.Msg("msg"  , "{type}({node}): could not access tmp")
				, Recover("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: tmp is accessible again")
					.Msg("msg"  , "{type}({node}): tmp is accessible again")),
			Equals("check_home_ok", False) :
				( Danger("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: could not access home")
					.Msg("msg"  , "{type}({node}): could not access home")
				, Recover("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: home is accessible again")
					.Msg("msg"  , "{type}({node}): home is accessible again")),
			Equals("check_clean_ok", False) :
				( Danger("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: could not remove file")
					.Msg("msg"  , "{type}({node}): could not remove file")
				, Recover("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: remove file worked")
					.Msg("msg"  , "{type}({node}): remove file worked")),

			Equals("check_nmond_ok", False) :
				( Danger("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: hopsa agent(nmond) not found")
					.Msg("msg"  , "{type}({node}): hopsa agent(nmond) not found")
				, Recover("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: hopsa agent(nmond) found")
					.Msg("msg"  , "{type}({node}): hopsa agent(nmond) found")),

			NotEquals("ntpd_drift_state", 1) :
				( Danger("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: ntpd drift is too big")
					.Msg("msg"  , "{type}({node}): ntpd drift({ntpd_drift}) is too big")
				, Recover("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: ntpd drift is ok")
					.Msg("msg"  , "{type}({node}): ntpd drift({ntpd_drift}) is ok")),

			NotEquals("temp_state", 0) :
				( Warning("tag", "TEMPERATURE").Msg("loc", "{node}")
					.Msg("descr", "{type}: bad system temp")
					.Msg("msg"  , "{type}({node}): bad system temp")
				, Recover("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: system temp is ok")
					.Msg("msg"  , "{type}({node}): system temp is ok")),

			Equals("temp_state", 2) :
				Critical("tag", "TEMPERATURE").Msg("loc", "{node}")
					.Msg("descr", "{type}: critical system temp")
					.Msg("msg"  , "{type}({node}): critical system temp"),
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
					.Msg("descr", "{type}: bad temp")
					.Msg("msg"  , "{type}({in_n:node}): bad temp({temp})")
				, Recover("tag", "TEMPERATURE").Msg("loc", "{in_n:node}")
					.Msg("descr", "{type}: temp is ok now ")
					.Msg("msg"  , "{type}({in_n:node}): temp({temp}) is ok now ")),

			Equals("temp_state", 2) :
				Critical("tag", "TEMPERATURE").Msg("loc", "{in_n:node}")
					.Msg("descr", "{type}: critical temp")
					.Msg("msg"  , "{type}({in_n:node}): critical temp({temp})"),
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
				.Msg("descr", "{type}: total mem reduced below check value")
				.Msg("msg"  , "{type}({in_n:node}): total mem({total}) reduced below check value({req_mem})")
			, Recover("tag", "MEM").Msg("loc", "{in_n:node}")
				.Msg("descr", "{type}: total mem is ok")
				.Msg("msg"  , "{type}({in_n:node}): total mem({total}) is ok")),
	}
}

#// ----------------------------------------- ETH --------------------------------------------

def IBModule(timeout = Minutes(10)):
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
		},

		"react" : {
			NotEquals("state", "Active") :
				Danger("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "{type}: IB link problem: state")
					.Msg("msg"  , "{type}({in_n:node}): IB link problem: {state}"),
			NotEquals("physical_state", "LinkUp") :
				Danger("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "{type}: IB link problem: physical state")
					.Msg("msg"  , "{type}({in_n:node}): IB link problem: {physical_state}"),

			NotEquals("SymbolErrors_check", False).Delay(1000) :
				Warning("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "{type}: IB errros growing: SymbolErrors")
					.Msg("msg"  , "{type}({in_n:node}): IB errros growing: SymbolErrors({SymbolErrors})"),
			NotEquals("RcvErrors_check", False).Delay(1000) :
				Warning("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "{type}: IB errros growing: RcvErrors")
					.Msg("msg"  , "{type}({in_n:node}): IB errros growing: RcvErrors({RcvErrors})"),
			NotEquals("RcvRemotePhysErrors_check", False).Delay(1000) :
				Warning("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "{type}: IB errros growing: RcvRemotePhysErrors")
					.Msg("msg"  , "{type}({in_n:node}): IB errros growing: RcvRemotePhysErrors({RcvRemotePhysErrors})"),
			NotEquals("RcvSwRelayErrors_check", False).Delay(1000) :
				Warning("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "{type}: IB errros growing: RcvSwRelayErrors")
					.Msg("msg"  , "{type}({in_n:node}): IB errros growing: RcvSwRelayErrors({RcvSwRelayErrors})"),
			NotEquals("XmtDiscards_check", False).Delay(1000) :
				Warning("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "{type}: IB errros growing: XmtDiscards")
					.Msg("msg"  , "{type}({in_n:node}): IB errros growing: XmtDiscards({XmtDiscards})"),
			NotEquals("XmtConstraintErrors_check", False).Delay(1000) :
				Warning("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "{type}: IB errros growing: XmtConstraintErrors")
					.Msg("msg"  , "{type}({in_n:node}): IB errros growing: XmtConstraintErrors({XmtConstraintErrors})"),
			NotEquals("RcvConstraintErrors_check", False).Delay(1000) :
				Warning("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "{type}: IB errros growing: RcvConstraintErrors")
					.Msg("msg"  , "{type}({in_n:node}): IB errros growing: RcvConstraintErrors({RcvConstraintErrors})"),
			NotEquals("LinkIntegrityErrors_check", False).Delay(1000) :
				Warning("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "{type}: IB errros growing: LinkIntegrityErrors")
					.Msg("msg"  , "{type}({in_n:node}): IB errros growing: LinkIntegrityErrors({LinkIntegrityErrors})"),
			NotEquals("ExcBufOverrunErrors_check", False).Delay(1000) :
				Warning("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "{type}: IB errros growing: ExcBufOverrunErrors")
					.Msg("msg"  , "{type}({in_n:node}): IB errros growing: ExcBufOverrunErrors({ExcBufOverrunErrors})"),
			NotEquals("VL15Dropped_check", False).Delay(1000) :
				Warning("tag", "IB").Msg("loc", "{in_n:node}")
					.Msg("descr", "{type}: IB errros growing: VL15Dropped")
					.Msg("msg"  , "{type}({in_n:node}): IB errros growing: VL15Dropped({VL15Dropped})"),
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
					.Msg("descr", "{type}: wrong speed")
					.Msg("msg"  , "{type}({in_n:node}): wrong speed({speed}), required: {_static_eth_speed_req}"),

			Equals("duplex_ok", False) :
				Danger("tag", "ETH").Msg("loc", "{in_n:node}")
					.Msg("descr", "{type}: wrong duplex mode")
					.Msg("msg"  , "{type}({in_n:node}): wrong duplex mode({duplex})"),

			Equals("check_rx_errors", False).Delay(1000) :
				Warning("tag", "ETH").Msg("loc", "{in_n:node}")
					.Msg("descr", "{type}: recieve errors growing fast for last 1000 seconds")
					.Msg("msg"  , "{type}({in_n:node}): recieve errors({rx_errors}) growing fast for last 1000 seconds"),

			Equals("check_tx_errors", False).Delay(1000) :
				Warning("tag", "ETH").Msg("loc", "{in_n:node}")
					.Msg("descr", "{type}: transm errors growing fast for last 1000 seconds")
					.Msg("msg"  , "{type}({in_n:node}): transm errors({tx_errors}) growing fast for last 1000 seconds"),

			Equals("check_tx_dropped", False).Delay(1000) :
				Warning("tag", "ETH").Msg("loc", "{in_n:node}")
					.Msg("descr", "{type}: tranms dropped growing fast for last 1000 seconds")
					.Msg("msg"  , "{type}({in_n:node}): tranms dropped({tx_dropped}) growing fast for last 1000 seconds"),

			Equals("check_collisions", False).Delay(1000) :
				Warning("tag", "ETH").Msg("loc", "{in_n:node}")
					.Msg("descr", "{type}: collisions growing fast for last 1000 seconds")
					.Msg("msg"  , "{type}({in_n:node}): collisions({collisions}) growing fast for last 1000 seconds"),
		}
	}
