from octopy import *

def FanSnmpModule(timeout = Minutes(1)):
	return {
		"static" :
		{
			"static_infra_air_in_temp"  : 35,
			"static_infra_air_out_temp" : 25,

			"static_infra_humidity" : 70,
		},

		"sensor" : {
			"inlet_1" : Long(timeout),
			"inlet_2" : Long(timeout),
			"inlet_3" : Long(timeout),

			"air_in"  : Long(timeout),
			"air_out" : Long(timeout),
			"humidity_in"  : Long(timeout),
			"humidity_out" : Long(timeout),

			"fluid_in"  : Long(timeout),
			"fluid_out" : Long(timeout),
		},

		"var" : {
			"fluid_in_state"  : CheckedInterval("fluid_in", 1, 20, 40),
		},

		"trigger" : {
			"high_inlet_1" : GTArg("inlet_1", "static_infra_air_in_temp"),
			"high_inlet_2" : GTArg("inlet_2", "static_infra_air_in_temp"),
			"high_inlet_3" : GTArg("inlet_3", "static_infra_air_in_temp"),

			"high_air_in"  : GTArg("air_in", "static_infra_air_in_temp"),
			"high_air_out" : GTArg("air_out", "static_infra_air_out_temp"),
			"high_humidity_in"  : GTArg("humidity_in", "static_infra_humidity"),
			"high_humidity_out" : GTArg("humidity_out", "static_infra_humidity"),

			"high_fluid_in" : Match("fluid_in", 2),
		},

		"react" : {
			"notify_high_inlet_1" : Reaction()
				.On("high_inlet_1")
				.Begin(Warning("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: air temperature 1 is too high")
					.Msg("msg"  , "{type}[{ip}]: air temperature 1 is too high: {inlet_1}"))
				.End(RWarning("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: air temperature 1 is back to normal")
					.Msg("msg"  , "{type}[{ip}]: air temperature 1 is back to normal")),

			"notify_high_inlet_2" : Reaction()
				.On("high_inlet_2")
				.Begin(Warning("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: air temperature 2 is too high")
					.Msg("msg"  , "{type}[{ip}]: air temperature 2 is too high: {inlet_2}"))
				.End(RWarning("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: air temperature 2 is back to normal")
					.Msg("msg"  , "{type}[{ip}]: air temperature 2 is back to normal")),

			"notify_high_inlet_3" : Reaction()
				.On("high_inlet_3")
				.Begin(Warning("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: air temperature 3 is too high")
					.Msg("msg"  , "{type}[{ip}]: air temperature 3 is too high: {inlet_3}"))
				.End(RWarning("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: air temperature 3 is back to normal")
					.Msg("msg"  , "{type}[{ip}]: air temperature 3 is back to normal")),

			"notify_high_humidity_in" : Reaction()
				.On("high_humidity_in")
				.Begin(Warning("tag", "ENVIRONMENT").Msg("loc", "{ip}")
					.Msg("descr", "{type}: air humidity_in is too high")
					.Msg("msg"  , "{type}[{ip}]: air humidity_in is too high: {humidity_in}"))
				.End(RWarning("tag", "ENVIRONMENT").Msg("loc", "{ip}")
					.Msg("descr", "{type}: air humidity_in is back to normal")
					.Msg("msg"  , "{type}[{ip}]: air humidity_in is back to normal")),

			"notify_high_humidity_out" : Reaction()
				.On("high_humidity_out")
				.Begin(Warning("tag", "ENVIRONMENT").Msg("loc", "{ip}")
					.Msg("descr", "{type}: air humidity_out is too high")
					.Msg("msg"  , "{type}[{ip}]: air humidity_out is too high: {humidity_out}"))
				.End(RWarning("tag", "ENVIRONMENT").Msg("loc", "{ip}")
					.Msg("descr", "{type}: air humidity_out is back to normal")
					.Msg("msg"  , "{type}[{ip}]: air humidity_out is back to normal")),

			"notify_high_air_in" : Reaction()
				.On("high_air_in")
				.Begin(Warning("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: air_in temperature is too high")
					.Msg("msg"  , "{type}[{ip}]: air_in temperature is too high: {air_in}"))
				.End(RWarning("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: air_in temperature is back to normal")
					.Msg("msg"  , "{type}[{ip}]: air_in temperature is back to normal")),

			"notify_high_air_out" : Reaction()
				.On("high_air_out")
				.Begin(Warning("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: air_out temperature is too high")
					.Msg("msg"  , "{type}[{ip}]: air_out temperature is too high: {air_out}"))
				.End(RWarning("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: air_out temperature is back to normal")
					.Msg("msg"  , "{type}[{ip}]: air_out temperature is back to normal")),

			"notify_high_fluid_in" : Reaction()
				.On("high_fluid_in")
				.Begin(Warning("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: fluid_in temperature is too high")
					.Msg("msg"  , "{type}[{ip}]: fluid_in temperature is too high: {fluid_in}"))
				.End(RWarning("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: fluid_in temperature is back to normal")
					.Msg("msg"  , "{type}[{ip}]: fluid_in temperature is back to normal")),
		}
	}


def FanSnmpTrapModule(timeout = UPDATE_TIME_NOT_SPECIFIED):
	return None # TODO
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
					.Msg("descr", "{type}: Frequent Humidifier faults")
					.Msg("msg"  , "{type}: Frequent Humidifier faults: {airWarningCondition_24_descr}"),

			Equals("pump_fault", True) :
				( Critical("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: Condensate pump fault")
					.Msg("msg"  , "{type}[{ip}]: Condensate pump fault: {airCriticalCondition_29_descr}")
				, Recover("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: Condensate pump is ok")
					.Msg("msg"  , "{type}[{ip}]: Condensate pump is ok: {airCriticalCondition_29_descr}")),

			Equals("water_detected", True) :
				( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
					.Msg("descr", "{type}: Sensor detected a fluid leak!")
					.Msg("msg"  , "{type}[{ip}]: Sensor detected a fluid leak!: {airWarningCondition_28_descr}")
				, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
					.Msg("descr", "{type}: Sensor is ok, no fluid detected")
					.Msg("msg"  , "{type}[{ip}]: Sensor is ok, no fluid detected: {airWarningCondition_28_descr}")),

			Equals("fan_fault", True) :
				( Warning("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: fault")
					.Msg("msg"  , "{type}[{ip}]: fault: {airWarningCondition_27_descr}")
				, Recover("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: is ok")
					.Msg("msg"  , "{type}[{ip}]: is ok: {airWarningCondition_27_descr}")),

			Equals("low_water_alarm", True) :
				( Warning("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: Humidifier low water level alarm")
					.Msg("msg"  , "{type}[{ip}]: Humidifier low water level alarm : {airWarningCondition_32_descr}")
				, Recover("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: Humidifier is ok")
					.Msg("msg"  , "{type}[{ip}]: Humidifier is ok: {airWarningCondition_32_descr}")),

			Equals("entering_fluid_temp_fault", True) :
				( Warning("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: Entering fluid temperature is too high")
					.Msg("msg"  , "{type}[{ip}]: Entering fluid temperature is too high: {airWarningCondition_39_descr}")
				, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: Entering fluid temperature is ok")
					.Msg("msg"  , "{type}[{ip}]: Entering fluid temperature is ok: {airWarningCondition_39_descr}")),

			Equals("fluid_temp_sensor_fault", True) :
				( Warning("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: Entering fluid tempereature sensor failed")
					.Msg("msg"  , "{type}[{ip}]: Entering fluid tempereature sensor failed: {airWarningCondition_40_descr}")
				, Recover("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: Entering fluid tempereature sensor is ok")
					.Msg("msg"  , "{type}[{ip}]: Entering fluid tempereature sensor is ok: {airWarningCondition_40_descr}")),

			Equals("communication_lost", True) :
				( Warning("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: Group communication lost")
					.Msg("msg"  , "{type}[{ip}]: Group communication lost: {airWarningCondition_54_descr}")
				, Recover("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: Group communication restored")
					.Msg("msg"  , "{type}[{ip}]: Group communication restored: {airWarningCondition_54_descr}")),

			Equals("relay_output_fault", True) :
				( Info("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: Relay output abnormal state")
					.Msg("msg"  , "{type}[{ip}]: Relay output abnormal state: {airInformationalCondition_3_descr}")
				, Recover("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
					.Msg("descr", "{type}: Relay output is ok")
					.Msg("msg"  , "{type}[{ip}]: Relay output is ok: {airInformationalCondition_3_descr}")),
		}
	}
