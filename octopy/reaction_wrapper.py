from octopy.utils import *

import ru.parallel.octotron as octotron

class Reaction(object):
	def __init__(self, response, recover = None, delay = 0, repeat = 0):
		self.response = response
		self.recover = recover
		self.delay = delay
		self.repeat = repeat

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
