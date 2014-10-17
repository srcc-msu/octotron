from octopy import *

panasas_system_module = {
	"const" : {
		"type" : "panasas_system"
	},

	"sensor" : {
		"capacity_total" : 0,
		"capacity_used"  : 0,
		"capacity_avail" : 0,
		"nfs_perf_ops" : 0,
		"nfs_perf_mbs" : 0
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
		"status" : "good",
		"blade_type" : "",
		"cpu_util"  : 0,
		"disk_util" : 0,
		"perf_ops"      : 0,
		"perf_response" : 0,
		"perf_in_kbs"   : 0,
		"perf_out_kbs"  : 0
	},

	"reaction" : {
		Equals("status", "warning") :
			( Danger("tag", "STORAGE")
				.Msg("descr", "warning on panasas blade uid")
				.Msg("msg"  , "warning on panasas blade {uid}")
			, Recover("tag", "STORAGE")
				.Msg("descr", "panasas blade is ok uid")
				.Msg("msg"  , "panasas blade is ok {uid}")),

		Equals("status", "offline") :
			( Danger("tag", "STORAGE")
				.Msg("descr", "panasas blade went offline uid")
				.Msg("msg"  , "panasas blade went offline {uid}")
			, Recover("tag", "STORAGE")
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
