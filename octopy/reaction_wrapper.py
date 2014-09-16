from octopy.utils import *

import ru.parallel.octotron as octotron

Equals = octotron.core.logic.impl.Equals
NotEquals = octotron.core.logic.impl.NotEquals

def Info(msg, *args):
	return octotron.reactions.CommonReactions.Info(msg, *args)

def Warning(msg, *args):
	return octotron.reactions.CommonReactions.Warning(msg, *args)

def Danger(msg, *args):
	return octotron.reactions.CommonReactions.Danger(msg, *args)

def Critical(msg, *args):
	return octotron.reactions.CommonReactions.Critical(msg, *args)

def Recover(msg, *args):
	return octotron.reactions.CommonReactions.Recover(msg, *args)
