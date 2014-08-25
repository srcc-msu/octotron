from octopy import *

link_module = {
	"var" : {
		"duplex_match" : LinkedVarArgMatch("duplex"),
		"speed_match" : LinkedVarArgMatch("speed"),
	},

	"react" : {
		("duplex_match", False) :
			Reaction(Danger("mismatch duplex mode on two sides of the link", "type")
				, Recover("duplex on the link is ok", "type")),

		("speed_match", False) :
			Reaction(Danger("mismatch speed on two sides of the link", "type")
				, Recover("speed on the link is ok", "type")),
	}
}
