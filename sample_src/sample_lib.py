# include all system wrappers
from octopy import *

# declare attributes
cpu_attributes = {
	"temperature" : 0,
	"avg_load" : 0,
	"_static_temp_max" : 70,
	"_static_load_max" : 90,
}

cpu_rules = {
	"temp_ok" : UpperArgThreshold("temperature", "_static_temp_max"),
	"load_ok" : UpperArgThreshold("avg_load", "_static_load_max")
}

cpu_reactions = {

# invoke the Danger() reaction if "temperature" becomes greater
# than "_static_temp_max"
# invoke the Recover() reaction when "temperature" lowers
	("temp_ok", False) :
		Reaction(Danger("very high cpu temperature", "temperature").PrintParent("type", "ip")
			, Recover("temperature is back to normal", "temperature").PrintParent("type", "ip")),

# invoke the Warning() reaction when "avg_load" becomes greater
# than "_static_load_max" and stays so for 60 or more seconds
	("load_ok", False) :
		Reaction(Warning("high cpu load for last minute", "avg_load").PrintParent("type", "ip")
			, delay = 60),
}
