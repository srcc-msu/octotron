from octopy import *

ups_snmp_sensor = {
	"capacity" : 100,

	"remaining_battery_time" : 0,

	"temp" : 0,
	"num_batteries" : 0,

	"input_voltage" : 0,

	"output_status" : "",
	"battery_status" : "",

	"pm_ok"   : 0,
	"pm_not"  : 0,
	"pm_fail" : 0,

	"pm_fail_ref" : 0,

	"_static_voltage_min" :  200,

	"_static_output_status_ref" : "onLine",
	"_static_battery_status_ref" : "batteryNormal",

	"_static_remaining_battery_time_min" :  180,
	"_static_capacity_min" :  30,
	"_static_ups_temp_max" :  40,
}

ups_snmp_var = {
	"remaining_battery_time_ok" : LowerArgThreshold("remaining_battery_time", "_static_remaining_battery_time_min"),
	"battery_status_ok" : ArgMatch("battery_status", "_static_battery_status_ref"),

	"ups_capacity_ok" : LowerArgThreshold("capacity", "_static_capacity_min"),
	"ups_temp_ok" : UpperArgThreshold("temp", "_static_ups_temp_max"),

	"ups_num_batteries_ok" : Match("num_batteries", 64),

	"input_voltage_ok" : LowerArgThreshold("input_voltage", "_static_voltage_min"),

	"output_status_ok" : ArgMatch("output_status", "_static_output_status_ref"),

	"pm_good" : ArgMatch("pm_ok", "pm_ok_ref"),
}

ups_snmp_react = {
	("ups_capacity_ok", False) :
		Reaction(Critical("ups: capacity is low", "type", "ip", "capacity")
			, Recover("ups: capacity is ok", "type", "ip", "capacity")),

	("input_voltage_ok", False) :
		Reaction(Critical("ups: low input voltage", "type", "ip", "input_voltage")
			, Recover("ups: voltage is ok", "type", "ip", "input_voltage")),

	("output_status_ok", False) :
		Reaction(Critical("ups: status changed", "type", "ip", "output_status")
			, Recover("ups: status is ok", "type", "ip", "output_status")),

	("ups_temp_ok", False) :
		Reaction(Danger("ups: temperature is too high", "type", "ip", "temp")
			, Recover("ups: temperature is ok", "type", "ip", "temp")),

	("ups_num_batteries_ok", False) :
		Reaction(Danger("ups: lost some batteries", "type", "ip", "num_batteries")
			, Recover("ups: obtained some batteries", "type", "ip", "num_batteries")),

	("pm_good", False) :
		Reaction(Danger("ups: power module failed", "type", "ip", "pm_ok", "pm_not", "pm_fail", "pm_ok_ref", "pm_not_ref", "pm_fail_ref")
			, Recover("ups: power modules are fine", "type", "ip", "pm_ok", "pm_not", "pm_fail", "pm_ok_ref", "pm_not_ref", "pm_fail_ref"))
}

ups_snmp_trap_sensor = {
	"communicationLost" : False,
	"upsOnBattery" : False,
	"lowBattery" : False,
	"bypass" : False,
	"badVoltage" : False,
	"chargerFailure" : False,
	"batteryOverTemperature" : False,

	"abnormalCondition" : False,
	"abnormalCondition_descr" : "",

	"upsOverload" : False,
	"upsDiagnosticsFailed" : False,
	"upsDischarged" : False,
	"upsTurnedOff" : False,
	"upsSleeping" : False,
	"upsWokeUp" : False,
	"upsRebootStarted" : False,
	"upsBatteryNeedsReplacement" : False,
	"bypassPowerSupplyFailure" : False,
	"baseFanFailure" : False,
	"batteryPackCommLost" : False,
	"calibrationStart" : False,
	"upsTurnedOn" : False,
	"upsBatteryReplaced" : False,
	"powerModuleIncrease" : False,
	"powerModuleDecrease" : False,
}

ups_snmp_trap_var = {
	"upsOverload_changed" : UpdatedRecently("upsOverload", 10),
	"upsDiagnosticsFailed_changed" : UpdatedRecently("upsDiagnosticsFailed", 10),
	"upsDischarged_changed" : UpdatedRecently("upsDischarged", 10),
	"upsTurnedOff_changed" : UpdatedRecently("upsTurnedOff", 10),
	"upsSleeping_changed" : UpdatedRecently("upsSleeping", 10),
	"upsWokeUp_changed" : UpdatedRecently("upsWokeUp", 10),
	"upsRebootStarted_changed" : UpdatedRecently("upsRebootStarted", 10),
	"upsBatteryNeedsReplacement_changed" : UpdatedRecently("upsBatteryNeedsReplacement", 10),
	"bypassPowerSupplyFailure_changed" : UpdatedRecently("bypassPowerSupplyFailure", 10),
	"baseFanFailure_changed" : UpdatedRecently("baseFanFailure", 10),
	"batteryPackCommLost_changed" : UpdatedRecently("batteryPackCommLost", 10),
	"calibrationStart_changed" : UpdatedRecently("calibrationStart", 10),
	"upsTurnedOn_changed" : UpdatedRecently("upsTurnedOn", 10),
	"upsBatteryReplaced_changed" : UpdatedRecently("upsBatteryReplaced", 10),
	"powerModuleIncrease_changed" : UpdatedRecently("powerModuleIncrease", 10),
	"powerModuleDecrease_changed" : UpdatedRecently("powerModuleDecrease", 10),
}

ups_snmp_trap_react = {
	("communicationLost", True) : Reaction(Danger("ups: communication lost", "type")
		, Recover("ups: communication established", "type")),

	("upsOnBattery", True) : Reaction(Critical("ups: power off, ups is on battary", "type", "ip")
		, Recover("ups: power on", "type", "ip")),

	("lowBattery", True) : Reaction(Critical("ups: low battery", "type", "ip")
		, Recover("ups: battery is ok", "type", "ip")),

	("bypass", True) : Reaction(Danger("ups: up is on bypass", "type", "ip", "bypass_descr")
		, Recover("ups: returned from bypass", "type", "ip")),

	("badVoltage", True) : Reaction(Critical("ups: bad voltage", "type", "ip")
		, Recover("ups: voltage is ok", "type", "ip")),
	("chargerFailure", True) : Reaction(Critical("ups: charger failure", "type", "ip")
		, Recover("ups: charger is ok", "type", "ip")),
	("batteryOverTemperature", True) : Reaction(Critical("ups: battery temperature is too high", "type", "ip")
		, Recover("ups: battery temperature is ok", "type", "ip")),

	("abnormalCondition", True) : Reaction(Critical("ups: abnormal condition", "type", "ip", "abnormalCondition_descr")
		, Recover("ups: normal condition", "type", "ip", "abnormalCondition_descr")),

	("upsOverload_changed", True) : Reaction(Danger("ups trap: upsOverload", "type", "ip")),
	("upsDiagnosticsFailed_changed", True) : Reaction(Danger("ups trap: upsDiagnosticsFailed", "type", "ip")),
	("upsDischarged_changed", True) : Reaction(Danger("ups trap: upsDischarged", "type", "ip")),
	("upsTurnedOff_changed", True) : Reaction(Danger("ups trap: upsTurnedOff", "type", "ip")),
	("upsSleeping_changed", True) : Reaction(Danger("ups trap: upsSleeping", "type", "ip")),
	("upsWokeUp_changed", True) : Reaction(Danger("ups trap: upsWokeUp", "type", "ip")),
	("upsRebootStarted_changed", True) : Reaction(Danger("ups trap: upsRebootStarted", "type", "ip")),
	("upsBatteryNeedsReplacement_changed", True) : Reaction(Danger("ups trap: upsBatteryNeedsReplacement", "type", "ip")),
	("bypassPowerSupplyFailure_changed", True) : Reaction(Danger("ups trap: bypassPowerSupplyFailure", "type", "ip")),
	("baseFanFailure_changed", True) : Reaction(Danger("ups trap: baseFanFailure", "type", "ip")),
	("batteryPackCommLost_changed", True) : Reaction(Danger("ups trap: batteryPackCommLost", "type", "ip")),
	("calibrationStart_changed", True) : Reaction(Danger("ups trap: calibrationStart", "type", "ip")),
	("upsTurnedOn_changed", True) : Reaction(Danger("ups trap: upsTurnedOn", "type", "ip")),
	("upsBatteryReplaced_changed", True) : Reaction(Danger("ups trap: upsBatteryReplaced", "type", "ip")),
	("powerModuleIncrease_changed", True) : Reaction(Danger("ups trap: powerModuleIncrease", "type", "ip")),
	("powerModuleDecrease_changed", True) : Reaction(Danger("ups trap: powerModuleDecrease", "type", "ip")),
}
