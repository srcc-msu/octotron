from octopy.utils import *

from ru.parallel.octotron.core.collections import ModelLinkList
from ru.parallel.octotron.core.collections import ModelObjectList
from ru.parallel.octotron.generators import LinkFactory

import java.lang
import jarray

from octopy.const_wrapper import *
from octopy.sensor_wrapper import *
from octopy.var_wrapper import *
from octopy.react_wrapper import *
from octopy.trigger_wrapper import *

def GetLinkFactory(params, type):
	factory = LinkFactory()

	CheckAllowed(params)

	factory = factory.Constants(ConvertConsts  (params["const"]))
	factory = factory.Statics  (ConvertConsts  (params["static"]))
	factory = factory.Sensors  (ConvertSensors (params["sensor"]))
	factory = factory.Vars     (ConvertVars    (params["var"]))
	factory = factory.Triggers (ConvertTriggers(params["trigger"]))
	factory = factory.Reactions(ConvertReacts  (params["react"]))

	return factory.Constants(ConvertConsts([{ "type" : type }]))

def CallFactoryMethod(factory, name, args):
	arg_types = []

# TODO rethink
	args = list(args)
	for i in range(len(args)):
		if isinstance(args[i], list): # only int arrays here
			arg_types.append(java.lang.Class.forName("[I"))
			args[i] = jarray.array(args[i], 'i')
		else:
			if isinstance(args[i], bool): arg_types.append(java.lang.Boolean.TYPE) # must check before int - PEP 285
			elif isinstance(args[i], int):arg_types.append(java.lang.Integer.TYPE)
			elif isinstance(args[i], float): arg_types.append(java.lang.Float.TYPE)
			elif isinstance(args[i], str): arg_types.append(java.lang.String.TYPE)
			else: arg_types.append(args[i].class)

	method = factory.getClass().getMethod(name, arg_types)

	return method.invoke(factory, *args)

def Call(name, types, modules, *args):
	params = MergeDicts(modules)

	result = ModelLinkList()

	for type in GetCollection(types):
		factory = GetLinkFactory(params, type)

		links = CallFactoryMethod(factory, name, args)

		result.append(links)

	return result

def CallSingle(types, modules, *args):
	params = MergeDicts(modules)

	result = ModelLinkList()

	for type in GetCollection(types):
		factory = GetLinkFactory(params, type)

		link = CallFactoryMethod(factory, "OneToOne", args)

		result.add(link)

	return result

# directed

def OneToOne(obj1, obj2, types, *modules):
	result = CallSingle(types, modules, obj1, obj2, True)

	return result.Only() if result.size() == 1 else result

def OneToEvery(obj1, obj2, types, *modules):
	return Call(OneToEvery.__name__, types, modules, obj1, obj2, True)

def EveryToOne(obj1, obj2, types, *modules):
	return Call(EveryToOne.__name__, types, modules, obj1, obj2, True)

def AllToAll(obj1, obj2, types, *modules):
	return Call(AllToAll.__name__, types, modules, obj1, obj2, True)

def EveryToEvery(obj1, obj2, types, *modules):
	return Call(EveryToEvery.__name__, types, modules, obj1, obj2, True)

def ChunksToEvery(obj1, obj2, types, *modules):
	return Call(ChunksToEvery.__name__, types, modules, obj1, obj2, True)

def EveryToChunks(obj1, obj2, types, *modules):
	return Call(EveryToChunks.__name__, types, modules, obj1, obj2, True)

def ChunksToEvery_LastLess(obj1, obj2, types, *modules):
	return Call(ChunksToEvery_LastLess.__name__, types, modules, obj1, obj2, True)

def EveryToChunks_LastLess(obj1, obj2, types, *modules):
	return Call(EveryToChunks_LastLess.__name__, types, modules, obj1, obj2, True)

def ChunksToEvery_Guided(obj1, obj2, guide, types, *modules):
	return Call(ChunksToEvery_Guided.__name__, types, modules, obj1, obj2, True, guide)

def EveryToChunks_Guided(obj1, obj2, guide, types, *modules):
	return Call(EveryToChunks_Guided.__name__, types, modules, obj1, obj2, True, guide)

# undirected

def OneWithOne(obj1, obj2, types, *modules):
	result = CallSingle(types, modules, obj1, obj2, False)

	return result.Only() if result.size() == 1 else result

def OneWithEvery(obj1, obj2, types, *modules):
	return Call(OneToEvery.__name__, types, modules, obj1, obj2, False)

def EveryWithOne(obj1, obj2, types, *modules):
	return Call(EveryToOne.__name__, types, modules, obj1, obj2, False)

def AllWithAll(obj1, obj2, types, *modules):
	return Call(AllToAll.__name__, types, modules, obj1, obj2, False)

def EveryWithEvery(obj1, obj2, types, *modules):
	return Call(EveryToEvery.__name__, types, modules, obj1, obj2, False)

def ChunksWithEvery(obj1, obj2, types, *modules):
	return Call(ChunksToEvery.__name__, types, modules, obj1, obj2, False)

def EveryWithChunks(obj1, obj2, types, *modules):
	return Call(EveryToChunks.__name__, types, modules, obj1, obj2, False)

def ChunksWithEvery_LastLess(obj1, obj2, types, *modules):
	return Call(ChunksToEvery_LastLess.__name__, types, modules, obj1, obj2, False)

def EveryWithChunks_LastLess(obj1, obj2, types, *modules):
	return Call(EveryToChunks_LastLess.__name__, types, modules, obj1, obj2, False)

def ChunksWithEvery_Guided(obj1, obj2, guide, types, *modules):
	return Call(ChunksToEvery_Guided.__name__, types, modules, obj1, obj2, False, guide)

def EveryWithChunks_Guided(obj1, obj2, guide, types, *modules):
	return Call(EveryToChunks_Guided.__name__, types, modules, obj1, obj2, False, guide)

def DiscoverConnect(sources, target_attributes, allowed_links, chain_attribute, chain_filters, link_type, max_length, connect_function = None, debug = None):
	"""
	sources - ModelList of elements to start from
	target_attributes - list of attributes (pairs) to detect target attributes
	allowed_links - list of attributes (pairs) to filter allowed links during traversing

	chain_attribute - attribute that will be used to generate path string for chain_filters
		the path string will be generated using values of the required attributes, separated by '-'
		e.g. "ib_node-ib_port-ib_port-ib_switch_element-ib_switch"

	chain_filters - list of regular expressions, all of them must succeed on target path string
		, or it will be discarded

	link_type - type for a new link

	example: DiscoverConnect(list_of_switches, [("type", "ib_switch"), ("type", "node")], [("type", "ib")], "type", ["^.*-ib_port-ib_port-[^p]*$"], "logical_ib")
	"""

	for source in sources:
		DiscoverConnectOne(source, target_attributes, allowed_links, chain_attribute, chain_filters, link_type, max_length, connect_function, debug)

import re
from ru.parallel.octotron.core.collections import ModelLinkList

def DiscoverConnectOne(source, target_attributes, allowed_links, chain_attribute, chain_filters, link_type, max_length, connect_function = None, debug = None):
	debug = debug is not None

	if connect_function is None:
		connect_function = OneWithOne

	compiled_chain_filters = []

	for chain_filter in chain_filters:
		compiled_chain_filters.append(re.compile(chain_filter))

#---------------

	def Step(paths):
		new_paths = []

		if debug:
			print "paths: ", map(lambda y: map(lambda x: x.GetID(), y), paths)

		for path in paths:
			neighbor_list = ModelObjectList()

			for allowed_link in allowed_links:
				for neighbor in path[-1].GetAllNeighbors(allowed_link[0], allowed_link[1]).Uniq():
					neighbor_list.add(neighbor)

			neighbor_list = neighbor_list.Uniq()


			for neighbor in neighbor_list:
				if neighbor in path:
					continue

				ext_path = path[:]
				ext_path.append(neighbor)

				new_paths.append(ext_path)

				if debug:
					print "added neighbor: ", neighbor.GetID()

		if debug:
			print "new paths: ", map(lambda y: map(lambda x: x.GetID(), y), new_paths)

		return new_paths

	def CheckPath(path):
		chain = ""
		prefix = ""

		for object in path:
			if not object.TestAttribute(chain_attribute):
				return False

			chain += prefix + object.GetAttribute(chain_attribute).GetValue().GetRaw()
			prefix = "-"

		for chain_filter in compiled_chain_filters:
			if not chain_filter.match(chain):
				if debug:
					print "chain %s failed regexp" % chain
				return False

		if debug:
			print "chain %s passed regexp" % chain

		return True

#---------------

	result = ModelLinkList()

	paths = [[source]]

	for i in xrange(1, max_length): # 1 elememnt already presents
		if debug:
			print "step ", i

		new_paths = Step(paths)

		unfinished_paths = []
		finished_paths = []

		for path in new_paths:
			added = False

			for target_attribute in target_attributes:
				name = target_attribute[0]
				value = target_attribute[1]

				if path[-1].TestAttribute(name) and path[-1].GetAttribute(name).eq(value):
					finished_paths.append(path)
					added = True

			if not added:
				unfinished_paths.append(path)

		for path in finished_paths:
			if CheckPath(path):
				result.add(connect_function(path[0], path[-1], link_type))

				if debug:
					print "added for: ", map(lambda x: x.GetID(), path)

		paths = unfinished_paths

	if debug:
		print "finished"

	return result
