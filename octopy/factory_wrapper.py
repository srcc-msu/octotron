from octopy.system import SystemCtx

from utils import *

import ru.parallel.octotron as octotron

class Reaction(object):
	def __init__(self, response, recover = None, delay = 0):
		self.response = response
		self.recover = recover
		self.delay = delay

class Rule(object):
	def __init__(self, args):
		self.args = args
		self.arg_name = None

	def SetArgName(self, arg_name):
		self.arg_name = arg_name

def CreateObjects(attributes = {}, rules = {}, reactions = {}, count = 1):
	SystemCtx.Debug("created a list with " + str(count) + " objects")

	graph_service = SystemCtx.GetGraphService()

	factory = octotron.generators.ObjectFactory(graph_service)

	factory = factory.Attributes(FromNested(attributes, AttributesFromDict))
	factory = factory.Rules(FromNested(rules, RulesFromDict))
	factory = factory.Reactions(FromNested(reactions, ReactionsFromDict))

	return factory.Create(count)

def CreateObject(attributes = {}, rules = {}, reactions = {}):
	SystemCtx.Debug("created 1 object")

	return CreateObjects(attributes, rules, reactions, 1).Only()
