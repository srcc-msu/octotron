from octopy import *

def FanSnmpModule(timeout = Minutes(1)):
	return {
		"static" :
		{
			"_static_infra_air_in_temp"  : 35,
			"_static_infra_air_out_temp" : 25,

			"_static_infra_humidity" : 70,
		},

		"sensor" : {
			"inlet_1" : Long(timeout),
			"inlet_2" : Long(timeout),
			"inlet_3" : Long(timeout),
			"humidity_in"  : Long(timeout),
			"humidity_out" : Long(timeout),
			"air_in"  : Long(timeout),
			"air_out" : Long(timeout),
			"fluid_in"  : Long(timeout),
			"fluid_out" : Long(timeout),
		},

		"var" : {
			"inlet_1_ok" : UpperArgThreshold("inlet_1", "_static_infra_air_in_temp"),
			"inlet_2_ok" : UpperArgThreshold("inlet_2", "_static_infra_air_in_temp"),
			"inlet_3_ok" : UpperArgThreshold("inlet_3", "_static_infra_air_in_temp"),

			"humidity_in_ok"  : UpperArgThreshold("humidity_in", "_static_infra_humidity"),
			"humidity_out_ok" : UpperArgThreshold("humidity_out", "_static_infra_humidity"),
			"air_in_ok"  : UpperArgThreshold("air_in", "_static_infra_air_in_temp"),
			"air_out_ok" : UpperArgThreshold("air_out", "_static_infra_air_out_temp"),

			"fluid_in_state"  : CheckedInterval("fluid_in", 1, 20, 40),
		},

		"react" : {
			Equals("inlet_1_ok", False) :
				( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: air temperature 1 is too high")
					.Msg("msg"  , "fan {ip}: air temperature 1 is too high: {inlet_1}")
				, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: air temperature 1 is back to normal")
					.Msg("msg"  , "fan {ip}: air temperature 1 is back to normal")),

			Equals("inlet_2_ok", False) :
				( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: air temperature 2 is too high")
					.Msg("msg"  , "fan {ip}: air temperature 2 is too high: {inlet_2}")
				, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: air temperature 2 is back to normal")
					.Msg("msg"  , "fan {ip}: air temperature 2 is back to normal")),

			Equals("inlet_3_ok", False) :
				( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: air temperature 3 is too high")
					.Msg("msg"  , "fan {ip}: air temperature 3 is too high: {inlet_3}")
				, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: air temperature 3 is back to normal")
					.Msg("msg"  , "fan {ip}: air temperature 3 is back to normal")),

			Equals("humidity_in_ok", False) :
				( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
					.Msg("descr", "fan: air humidity_in is too high")
					.Msg("msg"  , "fan {ip}: air humidity_in is too high: {humidity_in}")
				, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
					.Msg("descr", "fan: air humidity_in is back to normal")
					.Msg("msg"  , "fan {ip}: air humidity_in is back to normal")),

			Equals("humidity_out_ok", False) :
				( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
					.Msg("descr", "fan: air humidity_out is too high")
					.Msg("msg"  , "fan {ip}: air humidity_out is too high: {humidity_out}")
				, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
					.Msg("descr", "fan: air humidity_out is back to normal")
					.Msg("msg"  , "fan {ip}: air humidity_out is back to normal")),

			Equals("air_in_ok", False) :
				( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: air_in temperature is too high")
					.Msg("msg"  , "fan {ip}: air_in temperature is too high: {air_in}")
				, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: air_in temperature is back to normal")
					.Msg("msg"  , "fan {ip}: air_in temperature is back to normal")),

			Equals("air_out_ok", False) :
				( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: air_out temperature is too high")
					.Msg("msg"  , "fan {ip}: air_out temperature is too high: {air_out}")
				, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: air_out temperature is back to normal")
					.Msg("msg"  , "fan {ip}: air_out temperature is back to normal")),

			Equals("fluid_in_state", 2) :
				( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: fluid_in temperature is too high")
					.Msg("msg"  , "fan {ip}: fluid_in temperature is too high: {fluid_in}")
				, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: fluid_in temperature is back to normal")
					.Msg("msg"  , "fan {ip}: fluid_in temperature is back to normal")),

			Invalid("fluid_in_state") :
				Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: invalid fluid_in temperature")
					.Msg("msg"  , "fan {ip}: invalid fluid_in temperature: {fluid_in}"),
		}
	}


def FanSnmpTrapModule(timeout = UPDATE_TIME_NOT_SPECIFIED):
	return {
		# True = no trap
		"sensor" : {
			"airCriticalCondition_29" : Boolean(timeout, True),
			"airCriticalCondition_29_descr" : String(timeout, ""),

			"airWarningCondition_24" : Boolean(timeout, True),
			"airWarningCondition_24_descr" : String(timeout, ""),
			"airWarningCondition_27" : Boolean(timeout, True),
			"airWarningCondition_27_descr" : String(timeout, ""),
			"airWarningCondition_28" : Boolean(timeout, True),
			"airWarningCondition_28_descr" : String(timeout, ""),
			"airWarningCondition_32" : Boolean(timeout, True),
			"airWarningCondition_32_descr" : String(timeout, ""),
			"airWarningCondition_39" : Boolean(timeout, True),
			"airWarningCondition_39_descr" : String(timeout, ""),
			"airWarningCondition_40" : Boolean(timeout, True),
			"airWarningCondition_40_descr" : String(timeout, ""),
			"airWarningCondition_54" : Boolean(timeout, True),
			"airWarningCondition_54_descr" : String(timeout, ""),

			"airInformationalCondition_3" : Boolean(timeout, True),
			"airInformationalCondition_3_descr" : String(timeout, ""),
		},

		"var" : {
			"pump_fault" : ContainsString("airCriticalCondition_29_descr", "fault exists"),

			"water_detected" : ContainsString("airWarningCondition_28_descr", "fault exists"),

			"fan_fault" : ContainsString("airWarningCondition_27_descr", "fault exists"),

			"low_water_alarm" : ContainsString("airWarningCondition_32_descr", "alarm exists"),

			"entering_fluid_temp_fault" : ContainsString("airWarningCondition_39_descr", "violation exists"),

			"fluid_temp_sensor_fault" : ContainsString("airWarningCondition_40_descr", "sensor fault exists"),

			"communication_lost" : ContainsString("airWarningCondition_54_descr", "lost"),

			"relay_output_fault" : ContainsString("airInformationalCondition_3_descr", "abnormal state exists")
		},

		"react" : {
			Equals("airWarningCondition_24", False).Repeatable() :
				Warning("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: Frequent Humidifier faults")
					.Msg("msg"  , "fan: Frequent Humidifier faults: {airWarningCondition_24_descr}"),

			Equals("pump_fault", True) :
				( Critical("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: Condensate pump fault")
					.Msg("msg"  , "fan {ip}: Condensate pump fault: {airCriticalCondition_29_descr}")
				, Recover("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: Condensate pump is ok")
					.Msg("msg"  , "fan {ip}: Condensate pump is ok: {airCriticalCondition_29_descr}")),

			Equals("water_detected", True) :
				( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
					.Msg("descr", "fan: Sensor detected a fluid leak!")
					.Msg("msg"  , "fan {ip}: Sensor detected a fluid leak!: {airWarningCondition_28_descr}")
				, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
					.Msg("descr", "fan: Sensor is ok, no fluid detected")
					.Msg("msg"  , "fan {ip}: Sensor is ok, no fluid detected: {airWarningCondition_28_descr}")),

			Equals("fan_fault", True) :
				( Warning("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: fault")
					.Msg("msg"  , "fan {ip}: fault: {airWarningCondition_27_descr}")
				, Recover("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: is ok")
					.Msg("msg"  , "fan {ip}: is ok: {airWarningCondition_27_descr}")),

			Equals("low_water_alarm", True) :
				( Warning("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: Humidifier low water level alarm")
					.Msg("msg"  , "fan {ip}: Humidifier low water level alarm : {airWarningCondition_32_descr}")
				, Recover("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: Humidifier is ok")
					.Msg("msg"  , "fan {ip}: Humidifier is ok: {airWarningCondition_32_descr}")),

			Equals("entering_fluid_temp_fault", True) :
				( Warning("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: Entering fluid temperature is too high")
					.Msg("msg"  , "fan {ip}: Entering fluid temperature is too high: {airWarningCondition_39_descr}")
				, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: Entering fluid temperature is ok")
					.Msg("msg"  , "fan {ip}: Entering fluid temperature is ok: {airWarningCondition_39_descr}")),

			Equals("fluid_temp_sensor_fault", True) :
				( Warning("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: Entering fluid tempereature sensor failed")
					.Msg("msg"  , "fan {ip}: Entering fluid tempereature sensor failed: {airWarningCondition_40_descr}")
				, Recover("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: Entering fluid tempereature sensor is ok")
					.Msg("msg"  , "fan {ip}: Entering fluid tempereature sensor is ok: {airWarningCondition_40_descr}")),

			Equals("communication_lost", True) :
				( Warning("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: Group communication lost")
					.Msg("msg"  , "fan {ip}: Group communication lost: {airWarningCondition_54_descr}")
				, Recover("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: Group communication restored")
					.Msg("msg"  , "fan {ip}: Group communication restored: {airWarningCondition_54_descr}")),

			Equals("relay_output_fault", True) :
				( Info("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: Relay output abnormal state")
					.Msg("msg"  , "fan {ip}: Relay output abnormal state: {airInformationalCondition_3_descr}")
				, Recover("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "fan: Relay output is ok")
					.Msg("msg"  , "fan {ip}: Relay output is ok: {airInformationalCondition_3_descr}")),
		}
	}
