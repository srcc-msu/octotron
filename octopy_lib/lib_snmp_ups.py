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
			(Critical("POWER", "ups({ip}): capacity({capacity}) is low")
				, Recover("ups({ip}): capacity({capacity}) is ok")),

		Equals("input_voltage_ok", False) :
			(Critical("POWER", "ups({ip}): low input voltage({input_voltage})")
				, Recover("ups({ip}): voltage is ok")),

		Equals("output_status_ok", False) :
			(Critical("POWER", "ups({ip}): status changed: {output_status}")
				, Recover("ups({ip}): status is ok")),

		Equals("ups_temp_ok", False) :
			(Danger("TEMPERATURE", "ups({ip}): temperature({temp}) is too high")
				, Recover("ups({ip}): temperature is ok")),

		Equals("ups_num_batteries_ok", False) :
			(Danger("POWER", "ups({ip}): lost some batteries({num_batteries})")
				, Recover("ups({ip}): obtained some batteries({num_batteries})")),

		Equals("pm_good", False) :
			(Danger("POWER", "ups({ip}): power module failed: pm_ok: {pm_ok}/{pm_ok_ref}, pm_not: {pm_not}/{pm_not_ref}, pm_fail: {pm_fail}/{pm_fail_ref}")
				, Recover("ups({ip}): power modules are fine: pm_ok: {pm_ok}/{pm_ok_ref}, pm_not: {pm_not}/{pm_not_ref}, pm_fail: {pm_fail}/{pm_fail_ref}"))
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
			(Danger("INFRASTRUCUTRE", "ups({ip}): communication lost")
				, Recover("ups({ip}): communication established")),

		Equals("upsOnBattery", True) :
			(Critical("POWER", "ups({ip}): power off, ups({ip}) is on battary")
				, Recover("ups({ip}): power on")),

		Equals("lowBattery", True) :
			(Critical("POWER", "ups({ip}): low battery")
				, Recover("ups({ip}): battery is ok")),

		Equals("bypass", True) :
			(Danger("POWER", "ups({ip}): up is on bypass: {bypass_descr}")
				, Recover("ups({ip}): returned from bypass")),

		Equals("badVoltage", True) :
			(Critical("POWER", "ups({ip}): bad voltage")
				, Recover("ups({ip}): voltage is ok")),
		Equals("chargerFailure", True) :
			(Critical("POWER", "ups({ip}): charger failure")
				, Recover("ups({ip}): charger is ok")),
		Equals("batteryOverTemperature", True) :
			(Critical("TEMPERATURE", "ups({ip}): battery temperature is too high")
				, Recover("ups({ip}): battery temperature is ok")),

		Equals("abnormalCondition", True) :
			(Critical("POWER", "ups({ip}): abnormal condition: {abnormalCondition_descr}")
				, Recover("ups({ip}): normal condition: {abnormalCondition_descr}")),

		Equals("upsOverload", True).Repeatable() :
			Danger("POWER", "ups({ip}) trap: upsOverload"),
		Equals("upsDiagnosticsFailed", True).Repeatable() :
			Danger("POWER", "ups({ip}) trap: upsDiagnosticsFailed"),
		Equals("upsDischarged", True).Repeatable() :
			Danger("POWER", "ups({ip}) trap: upsDischarged"),
		Equals("upsTurnedOff", True).Repeatable() :
			Danger("POWER", "ups({ip}) trap: upsTurnedOff"),
		Equals("upsSleeping", True).Repeatable() :
			Danger("POWER", "ups({ip}) trap: upsSleeping"),
		Equals("upsWokeUp", True).Repeatable() :
			Danger("POWER", "ups({ip}) trap: upsWokeUp"),
		Equals("upsRebootStarted", True).Repeatable() :
			Danger("POWER", "ups({ip}) trap: upsRebootStarted"),
		Equals("upsBatteryNeedsReplacement", True).Repeatable() :
			Danger("POWER", "ups({ip}) trap: upsBatteryNeedsReplacement"),
		Equals("bypassPowerSupplyFailure", True).Repeatable() :
			Danger("POWER", "ups({ip}) trap: bypassPowerSupplyFailure"),
		Equals("baseFanFailure", True).Repeatable() :
			Danger("POWER", "ups({ip}) trap: baseFanFailure"),
		Equals("batteryPackCommLost", True).Repeatable() :
			Danger("POWER", "ups({ip}) trap: batteryPackCommLost"),
		Equals("calibrationStart", True).Repeatable() :
			Danger("POWER", "ups({ip}) trap: calibrationStart"),
		Equals("upsTurnedOn", True).Repeatable() :
			Danger("POWER", "ups({ip}) trap: upsTurnedOn"),
		Equals("upsBatteryReplaced", True).Repeatable() :
			Danger("POWER", "ups({ip}) trap: upsBatteryReplaced"),
		Equals("powerModuleIncrease", True).Repeatable() :
			Danger("POWER", "ups({ip}) trap: powerModuleIncrease"),
		Equals("powerModuleDecrease", True).Repeatable() :
			Danger("POWER", "ups({ip}) trap: powerModuleDecrease"),
	}
}
