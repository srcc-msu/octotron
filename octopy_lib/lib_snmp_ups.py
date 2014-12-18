from octopy import *

def UpsSnmpModule(update_time = Minutes(1)):
	return {
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
			"capacity" : Long(update_time),

			"remaining_battery_time" : Long(update_time),

			"temp" : Long(update_time),
			"num_batteries" : Long(update_time),

			"input_voltage" : Long(update_time),

			"output_status" : String(update_time),
			"battery_status" : String(update_time),

			"pm_ok"   : Long(update_time),
			"pm_not"  : Long(update_time),
			"pm_fail" : Long(update_time),

			"pm_fail_ref" : Long(update_time),
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

def UpsSnmpTrapModule(update_time = UPDATE_TIME_NOT_SPECIFIED):
	return {
		"sensor" : {
			"communicationLost" : Boolean(update_time, True),
			"communicationLost_descr" : String(update_time, ""),

			"upsOnBattery" : Boolean(update_time, True),
			"upsOnBattery_descr" : String(update_time, ""),

			"lowBattery" : Boolean(update_time, True),
			"lowBattery_descr" : String(update_time, ""),

			"bypass" : Boolean(update_time, True),
			"bypass_descr" : String(update_time, ""),

			"badVoltage" : Boolean(update_time, True),
			"badVoltage_descr" : String(update_time, ""),

			"chargerFailure" : Boolean(update_time, True),
			"chargerFailure_descr" : String(update_time, ""),

			"batteryOverTemperature" : Boolean(update_time, True),
			"batteryOverTemperature_descr" : String(update_time, ""),

			"abnormalCondition" : Boolean(update_time, True),
			"abnormalCondition_descr" : String(update_time, ""),

			"upsOverload" : Boolean(update_time, True),
			"upsOverload_descr" : String(update_time, ""),

			"upsDiagnosticsFailed" : Boolean(update_time, True),
			"upsDiagnosticsFailed_descr" : String(update_time, ""),

			"upsDischarged" : Boolean(update_time, True),
			"upsDischarged_descr" : String(update_time, ""),

			"upsTurnedOff" : Boolean(update_time, True),
			"upsTurnedOff_descr" : String(update_time, ""),

			"upsSleeping" : Boolean(update_time, True),
			"upsSleeping_descr" : String(update_time, ""),

			"upsWokeUp" : Boolean(update_time, True),
			"upsWokeUp_descr" : String(update_time, ""),

			"upsRebootStarted" : Boolean(update_time, True),
			"upsRebootStarted_descr" : String(update_time, ""),

			"upsBatteryNeedsReplacement" : Boolean(update_time, True),
			"upsBatteryNeedsReplacement_descr" : String(update_time, ""),

			"bypassPowerSupplyFailure" : Boolean(update_time, True),
			"bypassPowerSupplyFailure_descr" : String(update_time, ""),

			"baseFanFailure" : Boolean(update_time, True),
			"baseFanFailure_descr" : String(update_time, ""),

			"batteryPackCommLost" : Boolean(update_time, True),
			"batteryPackCommLost_descr" : String(update_time, ""),

			"calibrationStart" : Boolean(update_time, True),
			"calibrationStart_descr" : String(update_time, ""),

			"upsTurnedOn" : Boolean(update_time, True),
			"upsTurnedOn_descr" : String(update_time, ""),

			"upsBatteryReplaced" : Boolean(update_time, True),
			"upsBatteryReplaced_descr" : String(update_time, ""),

			"powerModuleIncrease" : Boolean(update_time, True),
			"powerModuleIncrease_descr" : String(update_time, ""),

			"powerModuleDecrease" : Boolean(update_time, True),
			"powerModuleDecrease_descr" : String(update_time, ""),
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
