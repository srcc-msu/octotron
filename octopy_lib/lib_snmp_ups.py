from octopy import *

ups_snmp_module = {
	"static" :
	{
		"_static_voltage_min" :  200,

		"_static_output_status_ref" : "onLine",
		"_static_battery_status_ref" : "batteryNormal",

		"_static_remaining_battery_time_min" :  180,
		"_static_capacity_min" :  30,
		"_static_ups_temp_max" :  40,
	},

	"sensor" : {
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
	},

	"var" : {
		"remaining_battery_time_ok" : LowerArgThreshold("remaining_battery_time", "_static_remaining_battery_time_min"),
		"battery_status_ok" : ArgMatch("battery_status", "_static_battery_status_ref"),

		"ups_capacity_ok" : LowerArgThreshold("capacity", "_static_capacity_min"),
		"ups_temp_ok" : UpperArgThreshold("temp", "_static_ups_temp_max"),

		"ups_num_batteries_ok" : Match("num_batteries", 64),

		"input_voltage_ok" : LowerArgThreshold("input_voltage", "_static_voltage_min"),

		"output_status_ok" : ArgMatch("output_status", "_static_output_status_ref"),

		"pm_good" : ArgMatch("pm_ok", "pm_ok_ref"),
	},

	"react" : {
		Equals("ups_capacity_ok", False) :
			(Critical("ups: capacity is low", "type", "ip", "capacity")
				, Recover("ups: capacity is ok", "type", "ip", "capacity")),

		Equals("input_voltage_ok", False) :
			(Critical("ups: low input voltage", "type", "ip", "input_voltage")
				, Recover("ups: voltage is ok", "type", "ip", "input_voltage")),

		Equals("output_status_ok", False) :
			(Critical("ups: status changed", "type", "ip", "output_status")
				, Recover("ups: status is ok", "type", "ip", "output_status")),

		Equals("ups_temp_ok", False) :
			(Danger("ups: temperature is too high", "type", "ip", "temp")
				, Recover("ups: temperature is ok", "type", "ip", "temp")),

		Equals("ups_num_batteries_ok", False) :
			(Danger("ups: lost some batteries", "type", "ip", "num_batteries")
				, Recover("ups: obtained some batteries", "type", "ip", "num_batteries")),

		Equals("pm_good", False) :
			(Danger("ups: power module failed", "type", "ip", "pm_ok", "pm_not", "pm_fail", "pm_ok_ref", "pm_not_ref", "pm_fail_ref")
				, Recover("ups: power modules are fine", "type", "ip", "pm_ok", "pm_not", "pm_fail", "pm_ok_ref", "pm_not_ref", "pm_fail_ref"))
	}
}

ups_snmp_trap_module = {

	"sensor" : {
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
	},

	"react" : {
		Equals("communicationLost", True) :
			(Danger("ups: communication lost", "type")
				, Recover("ups: communication established", "type")),

		Equals("upsOnBattery", True) :
			(Critical("ups: power off, ups is on battary", "type", "ip")
				, Recover("ups: power on", "type", "ip")),

		Equals("lowBattery", True) :
			(Critical("ups: low battery", "type", "ip")
				, Recover("ups: battery is ok", "type", "ip")),

		Equals("bypass", True) :
			(Danger("ups: up is on bypass", "type", "ip", "bypass_descr")
				, Recover("ups: returned from bypass", "type", "ip")),

		Equals("badVoltage", True) :
			(Critical("ups: bad voltage", "type", "ip")
				, Recover("ups: voltage is ok", "type", "ip")),
		Equals("chargerFailure", True) :
			(Critical("ups: charger failure", "type", "ip")
				, Recover("ups: charger is ok", "type", "ip")),
		Equals("batteryOverTemperature", True) :
			(Critical("ups: battery temperature is too high", "type", "ip")
				, Recover("ups: battery temperature is ok", "type", "ip")),

		Equals("abnormalCondition", True) :
			(Critical("ups: abnormal condition", "type", "ip", "abnormalCondition_descr")
				, Recover("ups: normal condition", "type", "ip", "abnormalCondition_descr")),

		Equals("upsOverload", True).Repeatable() :
			Danger("ups trap: upsOverload", "type", "ip"),
		Equals("upsDiagnosticsFailed", True).Repeatable() :
			Danger("ups trap: upsDiagnosticsFailed", "type", "ip"),
		Equals("upsDischarged", True).Repeatable() :
			Danger("ups trap: upsDischarged", "type", "ip"),
		Equals("upsTurnedOff", True).Repeatable() :
			Danger("ups trap: upsTurnedOff", "type", "ip"),
		Equals("upsSleeping", True).Repeatable() :
			Danger("ups trap: upsSleeping", "type", "ip"),
		Equals("upsWokeUp", True).Repeatable() :
			Danger("ups trap: upsWokeUp", "type", "ip"),
		Equals("upsRebootStarted", True).Repeatable() :
			Danger("ups trap: upsRebootStarted", "type", "ip"),
		Equals("upsBatteryNeedsReplacement", True).Repeatable() :
			Danger("ups trap: upsBatteryNeedsReplacement", "type", "ip"),
		Equals("bypassPowerSupplyFailure", True).Repeatable() :
			Danger("ups trap: bypassPowerSupplyFailure", "type", "ip"),
		Equals("baseFanFailure", True).Repeatable() :
			Danger("ups trap: baseFanFailure", "type", "ip"),
		Equals("batteryPackCommLost", True).Repeatable() :
			Danger("ups trap: batteryPackCommLost", "type", "ip"),
		Equals("calibrationStart", True).Repeatable() :
			Danger("ups trap: calibrationStart", "type", "ip"),
		Equals("upsTurnedOn", True).Repeatable() :
			Danger("ups trap: upsTurnedOn", "type", "ip"),
		Equals("upsBatteryReplaced", True).Repeatable() :
			Danger("ups trap: upsBatteryReplaced", "type", "ip"),
		Equals("powerModuleIncrease", True).Repeatable() :
			Danger("ups trap: powerModuleIncrease", "type", "ip"),
		Equals("powerModuleDecrease", True).Repeatable() :
			Danger("ups trap: powerModuleDecrease", "type", "ip"),
	}
}
