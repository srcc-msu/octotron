from octopy import *

panasas_system_a = {
	"type" : "panasas",
	"capacity_total" : 0,
	"capacity_used"  : 0,
	"capacity_avail" : 0,
	"nfs_perf_ops" : 0,
	"nfs_perf_mbs" : 0
}

panasas_system_r = {
	"sum_cpu_util"  : AggregateLongSum(EDependencyType.OUT, "sum_cpu_util"),
	"sum_disk_util" : AggregateLongSum(EDependencyType.OUT, "sum_disk_util"),
	"sum_perf_ops"      : AggregateLongSum(EDependencyType.OUT, "sum_perf_ops"),
	"sum_perf_response" : AggregateLongSum(EDependencyType.OUT, "sum_perf_response"),
	"sum_perf_in_kbs"   : AggregateLongSum(EDependencyType.OUT, "sum_perf_in_kbs"),
	"sum_perf_out_kbs"  : AggregateLongSum(EDependencyType.OUT, "sum_perf_out_kbs")

}

panasas_shelf_a = {
	"type" : "panasas_shelf",
}

panasas_shelf_r = {
	"sum_cpu_util"  : AggregateLongSum(EDependencyType.OUT, "cpu_util"),
	"sum_disk_util" : AggregateLongSum(EDependencyType.OUT, "disk_util"),
	"sum_perf_ops"      : AggregateLongSum(EDependencyType.OUT, "perf_ops"),
	"sum_perf_response" : AggregateLongSum(EDependencyType.OUT, "perf_response"),
	"sum_perf_in_kbs"   : AggregateLongSum(EDependencyType.OUT, "perf_in_kbs"),
	"sum_perf_out_kbs"  : AggregateLongSum(EDependencyType.OUT, "perf_out_kbs")
}

panasas_blade_a = {
	"type" : "panasas_blade",
	"status" : "good",
	"ref_status" : "good",
	"blade_type" : "",
	"cpu_util"  : 0,
	"disk_util" : 0,
	"perf_ops"      : 0,
	"perf_response" : 0,
	"perf_in_kbs"   : 0,
	"perf_out_kbs"  : 0
}

panasas_blade_r = {
	"state_warning" : NotMatch("status", "warning"),
	"state_offline" : NotMatch("status", "offline"),
}

panasas_blade_reaction = {
	("state_warning", False) :
		Reaction(Danger("warning on panasas blade", "type", "uid", "status")
			, Recover("panasas blade is ok", "type", "uid", "status")),

	("state_offline", False) :
		Reaction(Danger("panasas blade went offline", "type", "uid", "status")
			, Recover("panasas blade is ok", "type", "uid", "status")),
}

panasas_volume_a = {
	"type" : "panasas_volume",
	"info" : "",
}

panasas_volume_r = {}
