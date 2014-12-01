from octopy import *

PANASAS_UPDATE_TIME = Minutes(10)

panasas_system_module = {
	"const" : {
		"type" : "panasas_system"
	},

	"sensor" : {
		"capacity_total" : Long(PANASAS_UPDATE_TIME),
		"capacity_used"  : Long(PANASAS_UPDATE_TIME),
		"capacity_avail" : Long(PANASAS_UPDATE_TIME),
		"nfs_perf_ops" : Long(PANASAS_UPDATE_TIME),
		"nfs_perf_mbs" : Long(PANASAS_UPDATE_TIME),
	},

	"var" : {
		"sum_cpu_util"  : AggregateLongSum(EDependencyType.OUT, "sum_cpu_util"),
		"sum_disk_util" : AggregateLongSum(EDependencyType.OUT, "sum_disk_util"),
		"sum_perf_ops"      : AggregateLongSum(EDependencyType.OUT, "sum_perf_ops"),
		"sum_perf_response" : AggregateLongSum(EDependencyType.OUT, "sum_perf_response"),
		"sum_perf_in_kbs"   : AggregateLongSum(EDependencyType.OUT, "sum_perf_in_kbs"),
		"sum_perf_out_kbs"  : AggregateLongSum(EDependencyType.OUT, "sum_perf_out_kbs")
	}
}

panasas_shelf_module = {
	"const" : {
		"type" : "panasas_shelf"
	},

	"var" : {
		"sum_cpu_util"  : AggregateLongSum(EDependencyType.OUT, "cpu_util"),
		"sum_disk_util" : AggregateLongSum(EDependencyType.OUT, "disk_util"),
		"sum_perf_ops"      : AggregateLongSum(EDependencyType.OUT, "perf_ops"),
		"sum_perf_response" : AggregateLongSum(EDependencyType.OUT, "perf_response"),
		"sum_perf_in_kbs"   : AggregateLongSum(EDependencyType.OUT, "perf_in_kbs"),
		"sum_perf_out_kbs"  : AggregateLongSum(EDependencyType.OUT, "perf_out_kbs")
	}
}

panasas_blade_module = {
	"const" : {
		"type" : "panasas_blade"
	},

	"sensor" : {
		"status"     : String(PANASAS_UPDATE_TIME),
		"blade_type" : String(PANASAS_UPDATE_TIME),
		"cpu_util"  : Long(PANASAS_UPDATE_TIME),
		"disk_util" : Long(PANASAS_UPDATE_TIME),
		"perf_ops"      : Long(PANASAS_UPDATE_TIME),
		"perf_response" : Long(PANASAS_UPDATE_TIME),
		"perf_in_kbs"   : Long(PANASAS_UPDATE_TIME),
		"perf_out_kbs"  : Long(PANASAS_UPDATE_TIME),
	},

	"react" : {
		Equals("status", "warning") :
			( Danger("tag", "STORAGE").Msg("loc", "{uid}")
				.Msg("descr", "warning on panasas blade uid")
				.Msg("msg"  , "warning on panasas blade {uid}")
			, Recover("tag", "STORAGE").Msg("loc", "{uid}")
				.Msg("descr", "panasas blade is ok uid")
				.Msg("msg"  , "panasas blade is ok {uid}")),

		Equals("status", "offline") :
			( Danger("tag", "STORAGE").Msg("loc", "{uid}")
				.Msg("descr", "panasas blade went offline uid")
				.Msg("msg"  , "panasas blade went offline {uid}")
			, Recover("tag", "STORAGE").Msg("loc", "{uid}")
				.Msg("descr", "panasas blade is ok uid")
				.Msg("msg"  , "panasas blade is ok {uid}")),
	}
}

panasas_volume_module = {
	"const" : {
		"type" : "panasas_volume",
		"info" : "",
	}
}
