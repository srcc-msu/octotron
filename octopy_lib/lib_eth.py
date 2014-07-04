from octopy import *

eth_link_r = {
	"duplex_match" : LinkedVarArgMatch("duplex"),
	"speed_match" : LinkedVarArgMatch("speed"),
}

eth_link_react = {
	("duplex_match", False) :
		Reaction(Danger("mismatch duplex mode on two sides of the link", "type")
			, Recover("duplex on the link is ok", "type")),

	("speed_match", False) :
		Reaction(Danger("mismatch speed on two sides of the link", "type")
			, Recover("speed on the link is ok", "type")),
}
