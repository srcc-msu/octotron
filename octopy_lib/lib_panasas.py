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
			"sum_cpu_util"  : ASoftLongSum("out_n", "sum_cpu_util"),
			"sum_disk_util" : ASoftLongSum("out_n", "sum_disk_util"),
			"sum_perf_ops"      : ASoftLongSum("out_n", "sum_perf_ops"),
			"sum_perf_response" : ASoftLongSum("out_n", "sum_perf_response"),
			"sum_perf_in_kbs"   : ASoftLongSum("out_n", "sum_perf_in_kbs"),
			"sum_perf_out_kbs"  : ASoftLongSum("out_n", "sum_perf_out_kbs")
		}
	}

def PanasasShelfModule(timeout = Minutes(10)):
	return {
		"const" : {
			"type" : "panasas_shelf"
		},

		"var" : {
			"sum_cpu_util"  : ASoftLongSum("out_n", "cpu_util"),
			"sum_disk_util" : ASoftLongSum("out_n", "disk_util"),
			"sum_perf_ops"      : ASoftLongSum("out_n", "perf_ops"),
			"sum_perf_response" : ASoftLongSum("out_n", "perf_response"),
			"sum_perf_in_kbs"   : ASoftLongSum("out_n", "perf_in_kbs"),
			"sum_perf_out_kbs"  : ASoftLongSum("out_n", "perf_out_kbs")
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

		"trigger" : {
			"blade_warning" : Match("status", "warning"),
			"blade_offline" : Match("status", "offline"),
		},

		"react" : {
			"blade_warning" : Reaction()
				.On("blade_warning")
				.Begin(Warning("tag", "STORAGE").Msg("loc", "{uid}")
					.Msg("descr", "{type}: {status}")
					.Msg("msg"  , "{type}[{uid}]: {status}")),

			"blade_offline" : Reaction()
				.On("blade_offline")
				.Begin(Danger("tag", "STORAGE").Msg("loc", "{uid}")
					.Msg("descr", "{type}: {status}")
					.Msg("msg"  , "{type}[{uid}]: {status}"))
				.End(Recover("tag", "STORAGE").Msg("loc", "{uid}")
					.Msg("descr", "{type}: {status}")
					.Msg("msg"  , "{type}[{uid}]: {status}")),
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

		"trigger" : {
			"not_online" : NotMatch("info", "Online")
		},
		
		"react" : {
			"notify_not_online" : Reaction()
				.On("not_online")
				.Begin(Danger("tag", "STORAGE").Msg("loc", "{mount}")
					.Msg("descr", "{type}: info changed")
					.Msg("msg"  , "{type}[{mount}]: info changed: {info}"))
				.End(Recover("tag", "STORAGE").Msg("loc", "{mount}")
					.Msg("descr", "{type}: is ok")
					.Msg("msg"  , "{type}[{mount}]: is ok: {info}")),
		}
	}
