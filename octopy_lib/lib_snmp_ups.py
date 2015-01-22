from octopy import *

def UpsSnmpModule(timeout = Minutes(1)):
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
			"capacity" : Long(timeout),

			"remaining_battery_time" : Long(timeout),

			"temp" : Long(timeout),
			"num_batteries" : Long(timeout),

			"input_voltage" : Long(timeout),

			"output_status" : String(timeout),
			"battery_status" : String(timeout),

			"pm_ok"   : Long(timeout),
			"pm_not"  : Long(timeout),
			"pm_fail" : Long(timeout),

			"pm_fail_ref" : Long(timeout),
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
					.Msg("descr", "{type}: capacity is low")
					.Msg("msg"  , "{type}({ip}): capacity({capacity}) is low")
				, Recover("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "{type}: capacity is ok")
					.Msg("msg"  , "{type}({ip}): capacity is ok")),

			Equals("input_voltage_ok", False) :
				( Critical("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "{type}: low input voltage")
					.Msg("msg"  , "{type}({ip}): low input voltage({input_voltage})")
				, Recover("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "{type}: voltage is ok")
					.Msg("msg"  , "{type}({ip}): voltage is ok")),

			Equals("output_status_ok", False) :
				( Critical("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "{type}: status changed")
					.Msg("msg"  , "{type}({ip}): status changed: {output_status}")
				, Recover("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "{type}: status is ok")
					.Msg("msg"  , "{type}({ip}): status is ok")),

			Equals("ups_temp_ok", False) :
				( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: temperature is too high")
					.Msg("msg"  , "{type}({ip}): temperature({temp}) is too high")
				, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: temperature is ok")
					.Msg("msg"  , "{type}({ip}): temperature is ok")),

			Equals("ups_num_batteries_ok", False) :
				( Danger("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "{type}: lost some batteries")
					.Msg("msg"  , "{type}({ip}): lost some batteries({num_batteries})")
				, Recover("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "{type}: obtained some batteries")
					.Msg("msg"  , "{type}({ip}): obtained some batteries({num_batteries})")),

			Equals("pm_good", False) :
				( Danger("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "{type}: power module failed")
					.Msg("msg"  , "{type}({ip}): power module failed: pm_ok: {pm_ok}/{pm_ok_ref}, pm_not: {pm_not}/{pm_not_ref}, pm_fail: {pm_fail}/{pm_fail_ref}")
				, Recover("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "{type}: power modules are fine")
					.Msg("msg"  , "{type}({ip}): power modules are fine: pm_ok: {pm_ok}/{pm_ok_ref}, pm_not: {pm_not}/{pm_not_ref}, pm_fail: {pm_fail}/{pm_fail_ref})")),
		}
	}

def UpsSnmpTrapModule(timeout = UPDATE_TIME_NOT_SPECIFIED):
	return {
		"sensor" : {
			"communicationLost" : Boolean(timeout, True),
			"communicationLost_descr" : String(timeout, ""),

			"upsOnBattery" : Boolean(timeout, True),
			"upsOnBattery_descr" : String(timeout, ""),

			"lowBattery" : Boolean(timeout, True),
			"lowBattery_descr" : String(timeout, ""),

			"bypass" : Boolean(timeout, True),
			"bypass_descr" : String(timeout, ""),

			"badVoltage" : Boolean(timeout, True),
			"badVoltage_descr" : String(timeout, ""),

			"chargerFailure" : Boolean(timeout, True),
			"chargerFailure_descr" : String(timeout, ""),

			"batteryOverTemperature" : Boolean(timeout, True),
			"batteryOverTemperature_descr" : String(timeout, ""),

			"abnormalCondition" : Boolean(timeout, True),
			"abnormalCondition_descr" : String(timeout, ""),

			"upsOverload" : Boolean(timeout, True),
			"upsOverload_descr" : String(timeout, ""),

			"upsDiagnosticsFailed" : Boolean(timeout, True),
			"upsDiagnosticsFailed_descr" : String(timeout, ""),

			"upsDischarged" : Boolean(timeout, True),
			"upsDischarged_descr" : String(timeout, ""),

			"upsTurnedOff" : Boolean(timeout, True),
			"upsTurnedOff_descr" : String(timeout, ""),

			"upsSleeping" : Boolean(timeout, True),
			"upsSleeping_descr" : String(timeout, ""),

			"upsWokeUp" : Boolean(timeout, True),
			"upsWokeUp_descr" : String(timeout, ""),

			"upsRebootStarted" : Boolean(timeout, True),
			"upsRebootStarted_descr" : String(timeout, ""),

			"upsBatteryNeedsReplacement" : Boolean(timeout, True),
			"upsBatteryNeedsReplacement_descr" : String(timeout, ""),

			"bypassPowerSupplyFailure" : Boolean(timeout, True),
			"bypassPowerSupplyFailure_descr" : String(timeout, ""),

			"baseFanFailure" : Boolean(timeout, True),
			"baseFanFailure_descr" : String(timeout, ""),

			"batteryPackCommLost" : Boolean(timeout, True),
			"batteryPackCommLost_descr" : String(timeout, ""),

			"calibrationStart" : Boolean(timeout, True),
			"calibrationStart_descr" : String(timeout, ""),

			"upsTurnedOn" : Boolean(timeout, True),
			"upsTurnedOn_descr" : String(timeout, ""),

			"upsBatteryReplaced" : Boolean(timeout, True),
			"upsBatteryReplaced_descr" : String(timeout, ""),

			"powerModuleIncrease" : Boolean(timeout, True),
			"powerModuleIncrease_descr" : String(timeout, ""),

			"powerModuleDecrease" : Boolean(timeout, True),
			"powerModuleDecrease_descr" : String(timeout, ""),
		},


		"react" : {
			Equals("communicationLost", False) :
				( Danger("tag", "INFRASTRUCUTRE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: communication lost")
					.Msg("msg"  , "{type}({ip}): communication lost")
				, Recover("tag", "INFRASTRUCUTRE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: communication established")
					.Msg("msg"  , "{type}({ip}): communication established")),

			Equals("upsOnBattery", False) :
				( Critical("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "{type}: power off, ups is on battary")
					.Msg("msg"  , "{type}({ip}): power off, ups is on battary")
				, Recover("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "{type}: power on")
					.Msg("msg"  , "{type}({ip}): power on")),

			Equals("lowBattery", False) :
				( Critical("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "{type}: low battery")
					.Msg("msg"  , "{type}({ip}): low battery")
				, Recover("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "{type}: battery is ok")
					.Msg("msg"  , "{type}({ip}): battery is ok")),

			Equals("bypass", False) :
				( Danger("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "{type}: up is on bypass")
					.Msg("msg"  , "{type}({ip}): up is on bypass: {bypass_descr}")
				, Recover("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "{type}: returned from bypass")
					.Msg("msg"  , "{type}({ip}): returned from bypass")),

			Equals("badVoltage", False) :
				( Critical("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "{type}: bad voltage")
					.Msg("msg"  , "{type}({ip}): bad voltage")
				, Recover("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "{type}: voltage is ok")
					.Msg("msg"  , "{type}({ip}): voltage is ok")),
			Equals("chargerFailure", False) :
				( Critical("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "{type}: charger failure")
					.Msg("msg"  , "{type}({ip}): charger failure")
				, Recover("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "{type}: charger is ok")
					.Msg("msg"  , "{type}({ip}): charger is ok")),
			Equals("batteryOverTemperature", False) :
				( Critical("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: battery temperature is too high")
					.Msg("msg"  , "{type}({ip}): battery temperature is too high")
				, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: battery temperature is ok")
					.Msg("msg"  , "{type}({ip}): battery temperature is ok")),

			Equals("abnormalCondition", False) :
				( Critical("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "{type}: abnormal condition")
					.Msg("msg"  , "{type}({ip}): abnormal condition: {abnormalCondition_descr}")
				, Recover("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "{type}: normal condition")
					.Msg("msg"  , "{type}({ip}): normal condition: {abnormalCondition_descr}")),

			Equals("upsOverload", False).Repeatable() :
				Danger("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "ups trap: upsOverload")
					.Msg("msg"  , "{type}({ip}) trap: upsOverload"),
			Equals("upsDiagnosticsFailed", False).Repeatable() :
				Danger("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "ups trap: upsDiagnosticsFailed")
					.Msg("msg"  , "{type}({ip}) trap: upsDiagnosticsFailed"),
			Equals("upsDischarged", False).Repeatable() :
				Danger("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "ups trap: upsDischarged")
					.Msg("msg"  , "{type}({ip}) trap: upsDischarged"),
			Equals("upsTurnedOff", False).Repeatable() :
				Danger("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "ups trap: upsTurnedOff")
					.Msg("msg"  , "{type}({ip}) trap: upsTurnedOff"),
			Equals("upsSleeping", False).Repeatable() :
				Danger("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "ups trap: upsSleeping")
					.Msg("msg"  , "{type}({ip}) trap: upsSleeping"),
			Equals("upsWokeUp", False).Repeatable() :
				Danger("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "ups trap: upsWokeUp")
					.Msg("msg"  , "{type}({ip}) trap: upsWokeUp"),
			Equals("upsRebootStarted", False).Repeatable() :
				Danger("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "ups trap: upsRebootStarted")
					.Msg("msg"  , "{type}({ip}) trap: upsRebootStarted"),
			Equals("upsBatteryNeedsReplacement", False).Repeatable() :
				Danger("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "ups trap: upsBatteryNeedsReplacement")
					.Msg("msg"  , "{type}({ip}) trap: upsBatteryNeedsReplacement"),
			Equals("bypassPowerSupplyFailure", False).Repeatable() :
				Danger("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "ups trap: bypassPowerSupplyFailure")
					.Msg("msg"  , "{type}({ip}) trap: bypassPowerSupplyFailure"),
			Equals("baseFanFailure", False).Repeatable() :
				Danger("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "ups trap: baseFanFailure")
					.Msg("msg"  , "{type}({ip}) trap: baseFanFailure"),
			Equals("batteryPackCommLost", False).Repeatable() :
				Danger("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "ups trap: batteryPackCommLost")
					.Msg("msg"  , "{type}({ip}) trap: batteryPackCommLost"),
			Equals("calibrationStart", False).Repeatable() :
				Danger("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "ups trap: calibrationStart")
					.Msg("msg"  , "{type}({ip}) trap: calibrationStart"),
			Equals("upsTurnedOn", False).Repeatable() :
				Danger("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "ups trap: upsTurnedOn")
					.Msg("msg"  , "{type}({ip}) trap: upsTurnedOn"),
			Equals("upsBatteryReplaced", False).Repeatable() :
				Danger("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "ups trap: upsBatteryReplaced")
					.Msg("msg"  , "{type}({ip}) trap: upsBatteryReplaced"),
			Equals("powerModuleIncrease", False).Repeatable() :
				Danger("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "ups trap: powerModuleIncrease")
					.Msg("msg"  , "{type}({ip}) trap: powerModuleIncrease"),
			Equals("powerModuleDecrease", False).Repeatable() :
				Danger("tag", "POWER").Msg("loc", "{ip}")
					.Msg("descr", "ups trap: powerModuleDecrease")
					.Msg("msg"  , "{type}({ip}) trap: powerModuleDecrease"),
		}
	}
