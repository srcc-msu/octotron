from octopy import *

def PanasasSystemModule(update_time = Minutes(10)):
	return {
		"const" : {
			"type" : "panasas_system"
		},

		"sensor" : {
			"capacity_total" : Long(update_time),
			"capacity_used"  : Long(update_time),
			"capacity_avail" : Long(update_time),
			"nfs_perf_ops" : Long(update_time),
			"nfs_perf_mbs" : Long(update_time),
		},

		"var" : {
			"sum_cpu_util"  : ASoftLongSum(EDependencyType.OUT, "sum_cpu_util"),
			"sum_disk_util" : ASoftLongSum(EDependencyType.OUT, "sum_disk_util"),
			"sum_perf_ops"      : ASoftLongSum(EDependencyType.OUT, "sum_perf_ops"),
			"sum_perf_response" : ASoftLongSum(EDependencyType.OUT, "sum_perf_response"),
			"sum_perf_in_kbs"   : ASoftLongSum(EDependencyType.OUT, "sum_perf_in_kbs"),
			"sum_perf_out_kbs"  : ASoftLongSum(EDependencyType.OUT, "sum_perf_out_kbs")
		}
	}

def PanasasShelfModule(update_time = Minutes(10)):
	return {
		"const" : {
			"type" : "panasas_shelf"
		},

		"var" : {
			"sum_cpu_util"  : ASoftLongSum(EDependencyType.OUT, "cpu_util"),
			"sum_disk_util" : ASoftLongSum(EDependencyType.OUT, "disk_util"),
			"sum_perf_ops"      : ASoftLongSum(EDependencyType.OUT, "perf_ops"),
			"sum_perf_response" : ASoftLongSum(EDependencyType.OUT, "perf_response"),
			"sum_perf_in_kbs"   : ASoftLongSum(EDependencyType.OUT, "perf_in_kbs"),
			"sum_perf_out_kbs"  : ASoftLongSum(EDependencyType.OUT, "perf_out_kbs")
		}
	}

def PanasasBladeModule(update_time = Minutes(10)):
	return {
		"const" : {
			"type" : "panasas_blade"
		},

		"sensor" : {
			"status"     : String(update_time),
			"blade_type" : String(update_time),
			"cpu_util"  : Long(update_time),
			"disk_util" : Long(update_time),
			"perf_ops"      : Long(update_time),
			"perf_response" : Long(update_time),
			"perf_in_kbs"   : Long(update_time),
			"perf_out_kbs"  : Long(update_time),
		},

		"react" : {
			Equals("status", "warning") :
				( Danger("tag", "STORAGE").Msg("loc", "{uid}")
					.Msg("descr", "warning on panasas blade")
					.Msg("msg"  , "warning on panasas blade {uid}")
				, Recover("tag", "STORAGE").Msg("loc", "{uid}")
					.Msg("descr", "panasas blade is ok uid")
					.Msg("msg"  , "panasas blade is ok {uid}")),

			Equals("status", "offline") :
				( Danger("tag", "STORAGE").Msg("loc", "{uid}")
					.Msg("descr", "panasas blade went offline")
					.Msg("msg"  , "panasas blade went offline {uid}")
				, Recover("tag", "STORAGE").Msg("loc", "{uid}")
					.Msg("descr", "panasas blade is ok uid")
					.Msg("msg"  , "panasas blade is ok {uid}")),
		}
	}

def PanasasVolumeModule(update_time = Minutes(10)):
	return {
		"const" : {
			"type" : "panasas_volume",
		},

		"sensor" : {
			"info" : "",
		},

		"react" : {
			NotEquals("info", "Online") :
				( Danger("tag", "STORAGE").Msg("loc", "{panasas_volume}")
					.Msg("descr", "panasas volume info changed")
					.Msg("msg"  , "panasas volume({panasas_volume}) info changed: {info}")
				, Recover("tag", "STORAGE").Msg("loc", "{panasas_volume}")
					.Msg("descr", "panasas volume is ok")
					.Msg("msg"  , "panasas volume({panasas_volume}) is ok: {info}")),
		}
	}
