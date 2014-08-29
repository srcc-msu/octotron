from octopy.system import SystemCtx
from octopy.utils import *

import java.lang
import jarray

import ru.parallel.octotron as octotron

def GetLinkFactory(params, type):
	factory = octotron.generators.LinkFactory()

	factory = factory.Constants(ConvertAttributes(MergeDicts(params["const"])))
	factory = factory.Constants(ConvertAttributes(MergeDicts(params["static"])))
	factory = factory.Sensors  (ConvertAttributes(MergeDicts(params["sensor"])))
	factory = factory.Varyings (ConvertVars(MergeDicts(params["var"])))
	factory = factory.Reactions(ConvertReacts(MergeDicts(params["react"])))

	return factory.Constants(octotron.core.primitive.SimpleAttribute("type", type))

def CallFactoryMethod(factory, name, args):
	arg_types = []

# TODO rethink
	args = list(args)
	for i in range(len(args)):
		if isinstance(args[i], list): # only int arrays here
			arg_types.append(java.lang.Class.forName("[I"))
			args[i] = jarray.array(args[i], 'i')
		else:
			arg_types.append(args[i].class)

	method = factory.getClass().getMethod(name, arg_types)

	return method.invoke(factory, *args)

def Call(name, types, modules, *args):
	params = MergeDicts(modules)

	result = octotron.core.model.impl.ModelLinkList()

	for type in GetIterable(types):
		factory = GetLinkFactory(params, type)

		links = CallFactoryMethod(factory, name, args)

		SystemCtx.Debug("created " + str(links.size()) + " links for type " + type)
		result.append(links)

	return result

def OneToOne(obj1, obj2, types, *modules):
	return Call(OneToOne.__name__, types, modules, obj1, obj2)

def OneToEvery(obj1, obj2, types, *modules):
	return Call(OneToEvery.__name__, types, modules, obj1, obj2)

def EveryToOne(obj1, obj2, types, *modules):
	return Call(EveryToOne.__name__, types, modules, obj1, obj2)

def AllToAll(obj1, obj2, types, *modules):
	return Call(AllToAll.__name__, types, modules, obj1, obj2)

def EveryToEvery(obj1, obj2, types, *modules):
	return Call(EveryToEvery.__name__, types, modules, obj1, obj2)

def ChunksToEvery(obj1, obj2, types, *modules):
	return Call(ChunksToEvery.__name__, types, modules, obj1, obj2)

def EveryToChunks(obj1, obj2, types, *modules):
	return Call(EveryToChunks.__name__, types, modules, obj1, obj2)

def ChunksToEvery_LastLess(obj1, obj2, types, *modules):
	return Call(ChunksToEvery_LastLess.__name__, types, modules, obj1, obj2)

def EveryToChunks_LastLess(obj1, obj2, types, *modules):
	return Call(EveryToChunks_LastLess.__name__, types, modules, obj1, obj2)

def ChunksToEvery_Guided(obj1, obj2, guide, types, *modules):
	return Call(ChunksToEvery_Guided.__name__, types, modules, obj1, obj2, guide)

def EveryToChunks_Guided(obj1, obj2, guide, types, *modules):
	return Call(EveryToChunks_Guided.__name__, types, modules, obj1, obj2, guide)
