# include all system wrappers
from octopy import *

#
# module-style declaration
#
my_module = {
# declare constants
	"const" : {
		"temperature_max" : 70,
	},

# declare sensors
# the sensor must be updated every minute or timeout notification will be triggered
	"sensor" : {
		"temperature" : Long(Minutes(1))
	},

# declare varying attribute
# temperatrue_speed store a speed of the temperature changes
	"var" : {
		"temperatrue_speed" : Speed("temperature"),
	},

# declare triggers
# bad_temperature will be triggered, when temperature sensor is above threshold
	"trigger" :
	{
		"bad_temperature" : GTArg("temperature", "temperature_max"),
		"disable_all" : Manual()
	},

# declare reactions
# it will be execute when required trigger is turned on (by user or by condition)
# in this case - when temperature is above threshold
	"react" : {
		"notify_temperature" : Reaction()
			.On("bad_temperature")
			.Off("disable_all")
			.Begin(Danger("tag", "TEMPERATURE")
				.Msg("msg", "very high cpu temperature: {temperature}"))
			.Repeatable()
			.End(Recover("tag", "TEMPERATURE")
				.Msg("msg", "temperature is back to normal: {temperature}"))
	}
}

#
# separate declaration
#
my_const = {
	"load_max" : 90,
}

# declare sensors
my_sensor = {
	"avg_load" : Long(Minutes(1)),
}

my_trigger = {
	"bad_load" : GTArg("avg_load", "load_max")
}

# invoke the Warning() reaction when "avg_load" becomes greater
# than "load_max" and stays so for 60 or more seconds

my_react = {
	"notify_load" : Reaction()
		.On("bad_load", 0, 60)
		.Begin(Warning("msg", "high cpu load for last minute: {avg_load}"))
}
