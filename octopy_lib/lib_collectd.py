from octopy import *

def DiskModule(timeout = Minutes(10), reaction = Warning):
	loc = "{in_n:hostname}"
	loc_s = "{in_n:type} {type}: "
	loc_l = "{in_n:hostname} {type}: "

	def ErrorResponse(name):
		return (Reaction()
			.On(name + "_error")
			.Begin(reaction("tag", "DISK").Msg("loc", loc)
				.Msg("descr", loc_s + "disk error: %s" % (name))
				.Msg("msg"  , loc_l + "disk error: %s = {%s}" % (name, name))))

	return {
		"static" : {
			"static_disk_temp_max" :  40,
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
			"cd_disk_total_warnings" : AStrictMatchCount(True, "self"
				, "current_pending_sector_error"
				, "offline_uncorrectable_error"
				, "reallocated_sector_ct_error"
				, "reported_uncorrect_error"
				, "spin_retry_count_error"
				, "udma_crc_error_count_error"),

			"cd_disk_total_errors" : AStrictMatchCount(True, "self"
				, "bad_temperature"),
		},

		"trigger" : {
			"current_pending_sector_error" : NotMatch("current_pending_sector", 0),
			"offline_uncorrectable_error"  : NotMatch("offline_uncorrectable", 0),
			"reallocated_sector_ct_error"  : NotMatch("reallocated_sector_ct", 0),
			"reported_uncorrect_error"     : NotMatch("reported_uncorrect", 0),
			"spin_retry_count_error"       : NotMatch("spin_retry_count", 0),
			"udma_crc_error_count_error"   : NotMatch("udma_crc_error_count", 0),

			"bad_temperature" : GTArg("temperature_celsius", "static_disk_temp_max")
		},

		"react" : {
			"notify_current_pending_sector_error" : ErrorResponse("current_pending_sector"),
			"notify_offline_uncorrectable_error" : ErrorResponse("offline_uncorrectable"),
			"notify_reallocated_sector_ct_error" : ErrorResponse("reallocated_sector_ct"),
			"notify_reported_uncorrect_error" : ErrorResponse("reported_uncorrect"),
			"notify_spin_retry_count_error" : ErrorResponse("spin_retry_count"),
			"notify_udma_crc_error_count_error" : ErrorResponse("udma_crc_error_count"),

			"notify_bad_temperature" : Reaction()
				.On("bad_temperature")
				.Begin(reaction("tag", "TEMPERATURE").Msg("loc", loc)
					.Msg("descr", loc_s + "disk temperature is above threshold")
					.Msg("msg"  , loc_l + "disk temperature is above threshold: {temperature_celsius}"))
				.End(GenRStatus(reaction)("tag", "TEMPERATURE").Msg("loc", loc)
					.Msg("descr", loc_s + "disk temperature is back to normal")
					.Msg("msg"  , loc_l + "disk temperature is back to normal: {temperature_celsius}")),
		}
	}

def DiskProphecy():
	loc = "{in_n:hostname}"
	loc_s = "{in_n:type} {type}: "
	loc_l = "{in_n:hostname} {type}: "

	def GenProphecy(name, repeat = 0, delay = 0):
		base_counter = name.replace("_error", "").replace("bad_temperature", "temperature_celsius") # :(

		return (Reaction()
			.On(name, repeat, delay)
			.Begin(Prophecy("tag", "DISK").Msg("loc", loc)
				.Msg("descr", loc_s + "disk is doomed!")
				.Msg("msg"  , loc_l + "errors growing: %s = {%s}"% (base_counter, base_counter))))

	return {
		"react" : {
			"forecast_1" : GenProphecy("offline_uncorrectable_error"),
			"forecast_2" : GenProphecy("reallocated_sector_ct_error"),
			"forecast_3" : GenProphecy("spin_retry_count_error", 3),
			"forecast_4" : GenProphecy("bad_temperature", 0, Minutes(30)),
		}
	}

def MountPointModule(timeout = Minutes(10), mountpoint = "root", reaction = Warning, threshold = MB(200), pct_threshold = 5):
	loc = "{in_n:hostname}"
	loc_s = "{in_n:type} {type}: "
	loc_l = "{in_n:hostname} {mountpoint}: "

	return {
		"const" : {
			"mountpoint" : mountpoint,
		},

		"static" : {
			"threshold_percent_free" : pct_threshold,
			"threshold_bytes_free" : threshold
		},

		"sensor" : {
			"percent_free" : Long(timeout),
			"bytes_free" : Long(timeout)
		},

		"trigger" : {
			"low_percent_free" : LTArg("percent_free", "threshold_percent_free"),
			"low_bytes_free" : LTArg("bytes_free", "threshold_bytes_free"),
			"low_space" : StrictLogicalOr("low_percent_free", "low_bytes_free")
		},

		"react" : {
			"notify_low_space" : Reaction()
				.On("low_space")
				.Begin(reaction("tag", "DISK").Msg("loc", loc)
					.Msg("descr", loc_s + "free space is low")
					.Msg("msg"  , loc_l + "free space is low: {percent_free}% / {bytes_free}B"))
				.End(GenRStatus(reaction)("tag", "DISK").Msg("loc", loc)
					.Msg("descr", loc_s + "free space is ok")
					.Msg("msg"  , loc_l + "free space is ok: {percent_free}% / {bytes_free}B")),
		}
	}


#// ----------------------------------------- NODE --------------------------------------------

def ExperimentalNodeModule(timeout = Minutes(10), reaction = Info):
	loc = "{hostname}"
	loc_s = "{type}: "
	loc_l = "{hostname}: "

	return {
		"var" : {
			"la_state" : Interval("la_1", 3.0, 33.0),
		},

		"trigger" : {
			"task_present" : Manual(),

			"high_la_free" : Match("la_state", 1),
			"high_la_busy" : Match("la_state", 2),
		},
	}
"""
		"react" : {
			"notify_high_la_free" : Reaction()
				.Off("task_present")
				.On("high_la_free", 0, 1000)
				.Begin(reaction("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "LA exceeded 3.0 for last 1000 seconds, no running task")
					.Msg("msg"  , loc_l + "LA({la_1}) exceeded 3.0 for last 1000 seconds, no running task")),

			"notify_high_la_busy" : Reaction()
				.On("task_present")
				.On("high_la_busy", 0, 1000)
				.Begin(reaction("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "LA exceeded 33.0 for last 1000 seconds, user task presents")
					.Msg("msg"  , loc_l + "LA({la_1}) exceeded 33.0 for last 1000 seconds, user task presents")),
		}
"""

def NodeModule(timeout = Minutes(10), reaction = Info):
	loc = "{hostname}"
	loc_s = "{type}: "
	loc_l = "{hostname}: "

	return {
		"static" : {
			"static_fork_rate_thr" : 50.0,
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
			"fork_rate" : Speed("forks"),
			"ntpd_drift_state" : Interval("ntpd_drift", -2.0, 2.0),
			"temp_state" : Interval("temp", 40, 50),

			"cd_node_total_warnings" : AStrictMatchCount(True, "self"
				, "high_fork_rate"
				, "zombies_present"
				, "high_temp"),

			"cd_node_total_errors" : AStrictMatchCount(True, "self"
				, "tmp_test_error"
				, "home_test_error"
				, "clean_test_error"
				, "nmond_missing"

				, "high_nptd_drift"
				, "very_high_temp"),
		},

		"trigger" : {
			"high_fork_rate" : GTArg("fork_rate", "static_fork_rate_thr"),
			"zombies_present" : NotMatch("zombies", 0),

			"tmp_test_error" : NotMatch("check_tmp", 0),
			"home_test_error" : NotMatch("check_home", 0),
			"clean_test_error" : NotMatch("check_clean", 0),
			"nmond_missing" : NotMatch("check_nmond", 0),

			"high_nptd_drift" : NotMatch("ntpd_drift_state", 1),
			"high_temp" : NotMatch("temp_state", 0),
			"very_high_temp" : Match("temp_state", 2),
		},

		"react" : {
			"notify_fork_rate" : Reaction()
				.On("high_fork_rate", 0, 1000)
				.Begin(reaction("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "high fork rate on for last 1000 seconds")
					.Msg("msg"  , loc_l + "high fork rate on for last 1000 seconds, forks: {forks}, fork_rate: {fork_rate}"))
				.End(GenRStatus(reaction)("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "fork rate is ok")
					.Msg("msg"  , loc_l + "fork rate is ok, forks: {forks}, fork_rate: {fork_rate}")),

			"notify_zombies_present" : Reaction()
				.On("zombies_present", 0, 1000)
				.Begin(reaction("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "zombies present for last 1000 seconds")
					.Msg("msg"  , loc_l + "({zombies}) zombies present for last 1000 seconds, run for your life!"))
				.End(GenRStatus(reaction)("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "zombies are ok")
					.Msg("msg"  , loc_l + "zombies are ok({zombies})")),

			"notify_tmp_test_error" : Reaction()
				.On("tmp_test_error")
				.Begin(reaction("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "could not access tmp")
					.Msg("msg"  , loc_l + "could not access tmp"))
				.End(GenRStatus(reaction)("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "tmp is accessible again")
					.Msg("msg"  , loc_l + "tmp is accessible again")),

			"notify_home_test_error" : Reaction()
				.On("home_test_error")
				.Begin(reaction("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "could not access home")
					.Msg("msg"  , loc_l + "could not access home"))
				.End(GenRStatus(reaction)("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "home is accessible again")
					.Msg("msg"  , loc_l + "home is accessible again")),

			"notify_clean_test_error" : Reaction()
				.On("clean_test_error")
				.Begin(reaction("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "could not remove file")
					.Msg("msg"  , loc_l + "could not remove file"))
				.End(GenRStatus(reaction)("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "remove file worked")
					.Msg("msg"  , loc_l + "remove file worked")),

			"notify_nmond_missing" : Reaction()
				.On("nmond_missing")
				.Begin(reaction("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "hopsa agent(nmond) not found")
					.Msg("msg"  , loc_l + "hopsa agent(nmond) not found"))
				.End(GenRStatus(reaction)("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "hopsa agent(nmond) found")
					.Msg("msg"  , loc_l + "hopsa agent(nmond) found")),

			"notify_high_nptd_drift" : Reaction()
				.On("high_nptd_drift")
				.Begin(reaction("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "ntpd drift is too big")
					.Msg("msg"  , loc_l + "ntpd drift is too big: {ntpd_drift}"))
				.End(GenRStatus(reaction)("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "ntpd drift is ok")
					.Msg("msg"  , loc_l + "ntpd drift is ok: {ntpd_drift}")),

			"notify_high_temp" : Reaction()
				.On("high_temp")
				.Begin(reaction("tag", "TEMPERATURE").Msg("loc", loc)
					.Msg("descr", loc_s + "bad system temp")
					.Msg("msg"  , loc_l + "bad system temp"))
				.End(GenRStatus(reaction)("tag", "NODE").Msg("loc", loc)
					.Msg("descr", loc_s + "system temp is ok")
					.Msg("msg"  , loc_l + "system temp is ok: {temp}")),

			"notify_very_high_temp" : Reaction()
				.On("very_high_temp")
				.Begin(reaction("tag", "TEMPERATURE").Msg("loc", loc)
					.Msg("descr", loc_s + "critical system temp")
					.Msg("msg"  , loc_l + "critical system temp: {temp}")),
		}
	}

#// ----------------------------------------- CPU --------------------------------------------

def CpuModule(timeout = Minutes(10), reaction1 = Info, reaction2 = Warning):
	loc = "{in_n:hostname}"
	loc_s = "{in_n:type} {type}: "
	loc_l = "{in_n:hostname} {type}: "

	return {
		"sensor" : {
			"temp" : Long(timeout),
		},

		"var" : {
			"temp_state" : Interval("temp", 75, 80),
		},

		"trigger" : {
			"high_temp" : NotMatch("temp_state", 0),
			"very_high_temp" : Match("temp_state", 2),
		},

		"react" : {
			"notify_high_temp" : Reaction()
				.On("high_temp")
				.Begin(reaction1("tag", "TEMPERATURE").Msg("loc", loc)
					.Msg("descr", loc_s + "bad temp")
					.Msg("msg"  , loc_l + "bad temp({temp})"))
				.End(GenRStatus(reaction1)("tag", "TEMPERATURE").Msg("loc", loc)
					.Msg("descr", loc_s + "temp is ok now ")
					.Msg("msg"  , loc_l + "temp is ok: {temp}")),

			"notify_very_high_temp" : Reaction()
				.On("very_high_temp")
				.Begin(GenRStatus(reaction2)("tag", "TEMPERATURE").Msg("loc", loc)
					.Msg("descr", loc_s + "critical temp")
					.Msg("msg"  , loc_l + "critical temp: {temp}")),
		}
	}

#// ----------------------------------------- MEMORY --------------------------------------------

def MemoryModule(timeout = Minutes(10), reaction = Danger):
	loc = "{in_n:hostname}"
	loc_s = "{in_n:type} {type}: "
	loc_l = "{in_n:hostname} {type}: "

	return {
	"sensor" : {
		"buffered" : Long(timeout),
		"cached" : Long(timeout),
		"free" : Long(timeout),
		"used" : Long(timeout),
		"total" : Long(timeout),
	},

	"var" : {
		"cd_memory_total_errors" : AStrictMatchCount(True, "self", "memory_reduced")
	},

	"trigger" : {
		"memory_reduced" : LTArg("total", "req_mem"),
	},


	"react" : {
		"notify_memory_reduced" : Reaction()
			.On("memory_reduced")
			.Begin(reaction("tag", "MEM").Msg("loc", loc)
				.Msg("descr", loc_s + "total mem reduced below check value")
				.Msg("msg"  , loc_l + "total mem({total}) reduced below check value({req_mem})"))
			.End(GenRStatus(reaction)("tag", "MEM").Msg("loc", loc)
				.Msg("descr", loc_s + "total mem is ok")
				.Msg("msg"  , loc_l + "total mem({total}) is ok")),
	}
}

#// ----------------------------------------- ETH --------------------------------------------

def IBModule(timeout = Minutes(10), reaction = Warning):
	loc = "{in_n:hostname}"
	loc_s = "{in_n:type} {type}: "
	loc_l = "{in_n:hostname} {type}: "

	def ErrorResponse(name):
		return (Reaction()
			.On(name + "_error", 0, 1000)
			.Begin(reaction("tag", "IB").Msg("loc", loc)
				.Msg("descr", loc_s + "IB errros growing: %s" % (name))
				.Msg("msg"  , loc_l + "IB errros growing: %s = {%s}"% (name, name))))

	return {
		"static" : {
			"static_ib_err_speed_thr" : 10.0,
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

			"cd_ib_total_warnings" : AStrictMatchCount(True, "self"
				, "SymbolErrors_error"
				, "RcvErrors_error"
				, "RcvRemotePhysErrors_error"
				, "RcvSwRelayErrors_error"
				, "XmtDiscards_error"
				, "XmtConstraintErrors_error"
				, "RcvConstraintErrors_error"
				, "LinkIntegrityErrors_error"
				, "ExcBufOverrunErrors_error"
				, "VL15Dropped_error"),

			"cd_ib_total_errors" : AStrictMatchCount(True, "self"
				, "state_error"
				, "physical_state_error"),
		},

		"trigger" : {
			"state_error" : NotMatch("state", "Active"),
			"physical_state_error" : NotMatch("physical_state", "LinkUp"),
			"ib_errors" : NotMatch("cd_ib_total_warnings", 0),

			"SymbolErrors_error" : GTArg("SymbolErrors_speed", "static_ib_err_speed_thr"),
			"RcvErrors_error" : GTArg("RcvErrors_speed", "static_ib_err_speed_thr"),
			"RcvRemotePhysErrors_error" : GTArg("RcvRemotePhysErrors_speed", "static_ib_err_speed_thr"),
			"RcvSwRelayErrors_error" : GTArg("RcvSwRelayErrors_speed", "static_ib_err_speed_thr"),
			"XmtDiscards_error" : GTArg("XmtDiscards_speed", "static_ib_err_speed_thr"),
			"XmtConstraintErrors_error" : GTArg("XmtConstraintErrors_speed", "static_ib_err_speed_thr"),
			"RcvConstraintErrors_error" : GTArg("RcvConstraintErrors_speed", "static_ib_err_speed_thr"),
			"LinkIntegrityErrors_error" : GTArg("LinkIntegrityErrors_speed", "static_ib_err_speed_thr"),
			"ExcBufOverrunErrors_error" : GTArg("ExcBufOverrunErrors_speed", "static_ib_err_speed_thr"),
			"VL15Dropped_error" : GTArg("VL15Dropped_speed", "static_ib_err_speed_thr"),
		},

		"react" : {
			"notify_state_error" : Reaction()
				.On("state_error")
				.Begin(reaction("tag", "IB").Msg("loc", loc)
					.Msg("descr", loc_s + "IB link problem: state")
					.Msg("msg"  , loc_l + "IB link problem: {state}"))
				.End(GenRStatus(reaction)("tag", "IB").Msg("loc", loc)
					.Msg("descr", loc_s + "IB link state is ok")
					.Msg("msg"  , loc_l + "IB link state is ok: {state}")),
			
			"notify_physical_state_error" : Reaction()
				.On("physical_state_error")
				.Begin(reaction("tag", "IB").Msg("loc", loc)
					.Msg("descr", loc_s + "IB link problem: physical state")
					.Msg("msg"  , loc_l + "IB link problem: {physical_state}"))
				.End(GenRStatus(reaction)("tag", "IB").Msg("loc", loc)
					.Msg("descr", loc_s + "IB link physical state is ok")
					.Msg("msg"  , loc_l + "IB link physical state is ok: {physical_state}")),

			"notify_SymbolErrors_error" : ErrorResponse("SymbolErrors"),
			"notify_RcvErrors_error" : ErrorResponse("RcvErrors"),
			"notify_RcvRemotePhysErrors_error" : ErrorResponse("RcvRemotePhysErrors"),
			"notify_RcvSwRelayErrors_error" : ErrorResponse("RcvSwRelayErrors"),
			"notify_XmtDiscards_error" : ErrorResponse("XmtDiscards"),
			"notify_XmtConstraintErrors_error" : ErrorResponse("XmtConstraintErrors"),
			"notify_RcvConstraintErrors_error" : ErrorResponse("RcvConstraintErrors"),
			"notify_LinkIntegrityErrors_error" : ErrorResponse("LinkIntegrityErrors"),
			"notify_ExcBufOverrunErrors_error" : ErrorResponse("ExcBufOverrunErrors"),
			"notify_VL15Dropped_error" : ErrorResponse("VL15Dropped"),
		}
	}


def IBProphecy():
	loc = "{in_n:hostname}"
	loc_s = "{in_n:type} {type}: "
	loc_l = "{in_n:hostname} {type}: "

	def GenProphecy(name, repeat = 0, delay = 0):
		base_counter = name.replace("_error", "_speed")

		return (Reaction()
			.On(name, repeat, delay)
			.Begin(Prophecy("tag", "IB").Msg("loc", loc)
				.Msg("descr", loc_s + "IB is doomed!")
				.Msg("msg"  , loc_l + "reason: %s = {%s}" % (base_counter, base_counter))))

	return {
		"react" : {
			"forecast_ib1" : GenProphecy("SymbolErrors_error", 0, Minutes(30)),
			"forecast_ib2" : GenProphecy("RcvErrors_error", 0, Minutes(30)),
			"forecast_ib3" : GenProphecy("RcvRemotePhysErrors_error", 0, Minutes(30)),
			"forecast_ib4" : GenProphecy("RcvSwRelayErrors_error", 0, Minutes(30)),
			"forecast_ib5" : GenProphecy("XmtDiscards_error", 0, Minutes(30)),
			"forecast_ib6" : GenProphecy("XmtConstraintErrors_error", 0, Minutes(30)),
			"forecast_ib7" : GenProphecy("RcvConstraintErrors_error", 0, Minutes(30)),
			"forecast_ib8" : GenProphecy("LinkIntegrityErrors_error", 0, Minutes(30)),
			"forecast_ib9" : GenProphecy("ExcBufOverrunErrors_error", 0, Minutes(30)),
			"forecast_ib10" : GenProphecy("VL15Dropped_error", 0, Minutes(30)),
		}
	}


def EthModule(timeout = Minutes(10), reaction = Warning):
	loc = "{in_n:hostname}"
	loc_s = "{in_n:type} {type}: "
	loc_l = "{in_n:hostname} {type}: "

	def ErrorResponse(name):
		return (Reaction()
			.On(name + "_growing", 0, 1000)
			.Begin(reaction("tag", "ETH").Msg("loc", loc)
				.Msg("descr", loc_s + "eth errors growing: %s" % (name))
				.Msg("msg"  , loc_l + "eth errors growing: %s = {%s}"% (name, name))))

	return {
		"static" : {
			"static_eth_err_speed_thr" : 10.0
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

			"cd_eth_total_warnings" : AStrictMatchCount(True, "self"
				, "rx_errors_growing"
				, "tx_errors_growing"
				, "tx_dropped_growing"
				, "collisions_growing")
		},

		"trigger" : {
			"rx_errors_growing" : GTArg("rx_errors_speed", "static_eth_err_speed_thr"),
			"tx_errors_growing" : GTArg("tx_errors_speed", "static_eth_err_speed_thr"),

			"tx_dropped_growing" : GTArg("tx_dropped_speed", "static_eth_err_speed_thr"),
			"collisions_growing" : GTArg("collisions_speed", "static_eth_err_speed_thr"),
		},

		"react" : {
			"notify_rx_errors_growing" : ErrorResponse("rx_errors"),
			"notify_tx_errors_growing" : ErrorResponse("tx_errors"),
			"notify_tx_dropped_growing" : ErrorResponse("tx_dropped"),
			"notify_collisions_growing" : ErrorResponse("collisions"),
		}
	}

def EthProphecy():
	loc = "{in_n:hostname}"
	loc_s = "{in_n:type} {type}: "
	loc_l = "{in_n:hostname} {type}: "

	def GenProphecy(name, repeat = 0, delay = 0):
		base_counter = name.replace("_growing", "_speed")

		return (Reaction()
			.On(name, repeat, delay)
			.Begin(Prophecy("tag", "NETWORK").Msg("loc", loc)
				.Msg("descr", loc_s + "ethernet is doomed!")
				.Msg("msg"  , loc_l + "reason: %s = {%s}" % (base_counter, base_counter))))

	return {
		"react" : {
			"forecast_eth1" : GenProphecy("rx_errors_growing", 0, Minutes(30)),
			"forecast_eth2" : GenProphecy("tx_errors_growing", 0, Minutes(30)),
			"forecast_eth3" : GenProphecy("tx_dropped_growing", 0, Minutes(30)),
			"forecast_eth4" : GenProphecy("collisions_growing", 0, Minutes(30)),
		}
	}
