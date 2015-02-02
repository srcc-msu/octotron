from octopy import *

def PanasasSystemModule(timeout = Minutes(10)):
	return {
		"const" : {
			"type" : "panasas_system"
		},

		"sensor" : {
			"capacity_total" : Long(timeout),
			"capacity_used"  : Long(timeout),
			"capacity_avail" : Long(timeout),
			"nfs_perf_ops" : Long(timeout),
			"nfs_perf_mbs" : Long(timeout),
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

def PanasasShelfModule(timeout = Minutes(10)):
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

def PanasasBladeModule(timeout = Minutes(10)):
	return {
		"const" : {
			"type" : "panasas_blade"
		},

		"sensor" : {
			"status"     : String(timeout),
			"blade_type" : String(timeout),
			"cpu_util"  : Long(timeout),
			"disk_util" : Long(timeout),
			"perf_ops"      : Long(timeout),
			"perf_response" : Long(timeout),
			"perf_in_kbs"   : Long(timeout),
			"perf_out_kbs"  : Long(timeout),
		},

		"react" : {
			Equals("status", "warning") :
				( Danger("tag", "STORAGE").Msg("loc", "{uid}")
					.Msg("descr", "{type}: warning")
					.Msg("msg"  , "{type}[{uid}]: warning")
				, Recover("tag", "STORAGE").Msg("loc", "{uid}")
					.Msg("descr", "{type}: is ok")
					.Msg("msg"  , "{type}[{uid}]: is ok")),

			Equals("status", "offline") :
				( Danger("tag", "STORAGE").Msg("loc", "{uid}")
					.Msg("descr", "{type}: went offline")
					.Msg("msg"  , "{type}: went offline {uid}")
				, Recover("tag", "STORAGE").Msg("loc", "{uid}")
					.Msg("descr", "{type}: is ok")
					.Msg("msg"  , "{type}[{uid}]: is ok")),
		}
	}

def PanasasVolumeModule(timeout = Minutes(10)):
	return {
		"const" : {
			"type" : "panasas_volume",
		},

		"sensor" : {
			"info" : String(timeout),
		},

		"react" : {
			NotEquals("info", "Online") :
				( Danger("tag", "STORAGE").Msg("loc", "{mount}")
					.Msg("descr", "{type}: info changed")
					.Msg("msg"  , "{type}[{mount}]: info changed: {info}")
				, Recover("tag", "STORAGE").Msg("loc", "{mount}")
					.Msg("descr", "{type}: is ok")
					.Msg("msg"  , "{type}[{mount}]: is ok: {info}")),
		}
	}
