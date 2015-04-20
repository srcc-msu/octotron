from octopy.utils import *

from ru.parallel.octotron.core.collections import ModelLinkList
from ru.parallel.octotron.generators import LinkFactory

import java.lang
import jarray

from octopy.const_wrapper import *
from octopy.sensor_wrapper import *
from octopy.var_wrapper import *
from octopy.react_wrapper import *

def GetLinkFactory(params, type):
	factory = LinkFactory(model_service)

	CheckAllowed(params)

	factory = factory.Constants(ConvertConsts(params["const"]))
	factory = factory.Constants(ConvertConsts(params["static"]))
	factory = factory.Sensors  (ConvertSensors(params["sensor"]))
	factory = factory.Vars     (ConvertVars(params["var"]))
	factory = factory.Reactions(ConvertReacts(params["react"]))

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
