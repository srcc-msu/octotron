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
			( Critical("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups: capacity is low")
				.Msg("msg"  , "ups {ip}: capacity({capacity}) is low")
			, Recover("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups: capacity is ok")
				.Msg("msg"  , "ups {ip}: capacity is ok")),

		Equals("input_voltage_ok", False) :
			( Critical("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups: low input voltage")
				.Msg("msg"  , "ups {ip}: low input voltage({input_voltage})")
			, Recover("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups: voltage is ok")
				.Msg("msg"  , "ups {ip}: voltage is ok")),

		Equals("output_status_ok", False) :
			( Critical("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups: status changed")
				.Msg("msg"  , "ups {ip}: status changed: {output_status}")
			, Recover("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups: status is ok")
				.Msg("msg"  , "ups {ip}: status is ok")),

		Equals("ups_temp_ok", False) :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ups: temperature is too high")
				.Msg("msg"  , "ups {ip}: temperature({temp}) is too high")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ups: temperature is ok")
				.Msg("msg"  , "ups {ip}: temperature is ok")),

		Equals("ups_num_batteries_ok", False) :
			( Danger("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups: lost some batteries")
				.Msg("msg"  , "ups {ip}: lost some batteries({num_batteries})")
			, Recover("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups: obtained some batteries")
				.Msg("msg"  , "ups {ip}: obtained some batteries({num_batteries})")),

		Equals("pm_good", False) :
			( Danger("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups: power module failed")
				.Msg("msg"  , "ups {ip}: power module failed: pm_ok: {pm_ok}/{pm_ok_ref}, pm_not: {pm_not}/{pm_not_ref}, pm_fail: {pm_fail}/{pm_fail_ref}")
			, Recover("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups: power modules are fine")
				.Msg("msg"  , "ups {ip}: power modules are fine: pm_ok: {pm_ok}/{pm_ok_ref}, pm_not: {pm_not}/{pm_not_ref}, pm_fail: {pm_fail}/{pm_fail_ref})")),
	}
}

ups_snmp_trap_module = {
	"sensor" : {
		"communicationLost" : True, "communicationLost_descr" : "",
		"upsOnBattery" : True, "upsOnBattery_descr" : "",
		"lowBattery" : True, "lowBattery_descr" : "",
		"bypass" : True, "bypass_descr" : "",
		"badVoltage" : True, "badVoltage_descr" : "",
		"chargerFailure" : True, "chargerFailure_descr" : "",
		"batteryOverTemperature" : True, "batteryOverTemperature_descr" : "",
		"abnormalCondition" : True, "abnormalCondition_descr" : "",
		"upsOverload" : True, "upsOverload_descr" : "",
		"upsDiagnosticsFailed" : True, "upsDiagnosticsFailed_descr" : "",
		"upsDischarged" : True, "upsDischarged_descr" : "",
		"upsTurnedOff" : True, "upsTurnedOff_descr" : "",
		"upsSleeping" : True, "upsSleeping_descr" : "",
		"upsWokeUp" : True, "upsWokeUp_descr" : "",
		"upsRebootStarted" : True, "upsRebootStarted_descr" : "",
		"upsBatteryNeedsReplacement" : True, "upsBatteryNeedsReplacement_descr" : "",
		"bypassPowerSupplyFailure" : True, "bypassPowerSupplyFailure_descr" : "",
		"baseFanFailure" : True, "baseFanFailure_descr" : "",
		"batteryPackCommLost" : True, "batteryPackCommLost_descr" : "",
		"calibrationStart" : True, "calibrationStart_descr" : "",
		"upsTurnedOn" : True, "upsTurnedOn_descr" : "",
		"upsBatteryReplaced" : True, "upsBatteryReplaced_descr" : "",
		"powerModuleIncrease" : True, "powerModuleIncrease_descr" : "",
		"powerModuleDecrease" : True, "powerModuleDecrease_descr" : "",
	},

	"react" : {
		Equals("communicationLost", False) :
			( Danger("tag", "INFRASTRUCUTRE").Msg("loc", "{ip}")
				.Msg("descr", "ups: communication lost")
				.Msg("msg"  , "ups {ip}: communication lost")
			, Recover("tag", "INFRASTRUCUTRE").Msg("loc", "{ip}")
				.Msg("descr", "ups: communication established")
				.Msg("msg"  , "ups {ip}: communication established")),

		Equals("upsOnBattery", False) :
			( Critical("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups: power off, ups is on battary")
				.Msg("msg"  , "ups {ip}: power off, ups is on battary")
			, Recover("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups: power on")
				.Msg("msg"  , "ups {ip}: power on")),

		Equals("lowBattery", False) :
			( Critical("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups: low battery")
				.Msg("msg"  , "ups {ip}: low battery")
			, Recover("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups: battery is ok")
				.Msg("msg"  , "ups {ip}: battery is ok")),

		Equals("bypass", False) :
			( Danger("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups: up is on bypass")
				.Msg("msg"  , "ups {ip}: up is on bypass: {bypass_descr}")
			, Recover("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups: returned from bypass")
				.Msg("msg"  , "ups {ip}: returned from bypass")),

		Equals("badVoltage", False) :
			( Critical("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups: bad voltage")
				.Msg("msg"  , "ups {ip}: bad voltage")
			, Recover("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups: voltage is ok")
				.Msg("msg"  , "ups {ip}: voltage is ok")),
		Equals("chargerFailure", False) :
			( Critical("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups: charger failure")
				.Msg("msg"  , "ups {ip}: charger failure")
			, Recover("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups: charger is ok")
				.Msg("msg"  , "ups {ip}: charger is ok")),
		Equals("batteryOverTemperature", False) :
			( Critical("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ups: battery temperature is too high")
				.Msg("msg"  , "ups {ip}: battery temperature is too high")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ups: battery temperature is ok")
				.Msg("msg"  , "ups {ip}: battery temperature is ok")),

		Equals("abnormalCondition", False) :
			( Critical("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups: abnormal condition")
				.Msg("msg"  , "ups {ip}: abnormal condition: {abnormalCondition_descr}")
			, Recover("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups: normal condition")
				.Msg("msg"  , "ups {ip}: normal condition: {abnormalCondition_descr}")),

		Equals("upsOverload", False).Repeatable() :
			Danger("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups trap: upsOverload")
				.Msg("msg"  , "ups {ip} trap: upsOverload"),
		Equals("upsDiagnosticsFailed", False).Repeatable() :
			Danger("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups trap: upsDiagnosticsFailed")
				.Msg("msg"  , "ups {ip} trap: upsDiagnosticsFailed"),
		Equals("upsDischarged", False).Repeatable() :
			Danger("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups trap: upsDischarged")
				.Msg("msg"  , "ups {ip} trap: upsDischarged"),
		Equals("upsTurnedOff", False).Repeatable() :
			Danger("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups trap: upsTurnedOff")
				.Msg("msg"  , "ups {ip} trap: upsTurnedOff"),
		Equals("upsSleeping", False).Repeatable() :
			Danger("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups trap: upsSleeping")
				.Msg("msg"  , "ups {ip} trap: upsSleeping"),
		Equals("upsWokeUp", False).Repeatable() :
			Danger("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups trap: upsWokeUp")
				.Msg("msg"  , "ups {ip} trap: upsWokeUp"),
		Equals("upsRebootStarted", False).Repeatable() :
			Danger("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups trap: upsRebootStarted")
				.Msg("msg"  , "ups {ip} trap: upsRebootStarted"),
		Equals("upsBatteryNeedsReplacement", False).Repeatable() :
			Danger("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups trap: upsBatteryNeedsReplacement")
				.Msg("msg"  , "ups {ip} trap: upsBatteryNeedsReplacement"),
		Equals("bypassPowerSupplyFailure", False).Repeatable() :
			Danger("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups trap: bypassPowerSupplyFailure")
				.Msg("msg"  , "ups {ip} trap: bypassPowerSupplyFailure"),
		Equals("baseFanFailure", False).Repeatable() :
			Danger("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups trap: baseFanFailure")
				.Msg("msg"  , "ups {ip} trap: baseFanFailure"),
		Equals("batteryPackCommLost", False).Repeatable() :
			Danger("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups trap: batteryPackCommLost")
				.Msg("msg"  , "ups {ip} trap: batteryPackCommLost"),
		Equals("calibrationStart", False).Repeatable() :
			Danger("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups trap: calibrationStart")
				.Msg("msg"  , "ups {ip} trap: calibrationStart"),
		Equals("upsTurnedOn", False).Repeatable() :
			Danger("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups trap: upsTurnedOn")
				.Msg("msg"  , "ups {ip} trap: upsTurnedOn"),
		Equals("upsBatteryReplaced", False).Repeatable() :
			Danger("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups trap: upsBatteryReplaced")
				.Msg("msg"  , "ups {ip} trap: upsBatteryReplaced"),
		Equals("powerModuleIncrease", False).Repeatable() :
			Danger("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups trap: powerModuleIncrease")
				.Msg("msg"  , "ups {ip} trap: powerModuleIncrease"),
		Equals("powerModuleDecrease", False).Repeatable() :
			Danger("tag", "POWER").Msg("loc", "{ip}")
				.Msg("descr", "ups trap: powerModuleDecrease")
				.Msg("msg"  , "ups {ip} trap: powerModuleDecrease"),
	}
}
