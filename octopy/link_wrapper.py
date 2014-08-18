from octopy.system import SystemCtx
from octopy.utils import *

import java.lang
import jarray

import ru.parallel.octotron as octotron

def GetLinkFactory(const, sensor, var, react, type):
	factory = octotron.generators.LinkFactory()

	factory = factory.Constants(ConvertAttributes(const))
	factory = factory.Sensors(ConvertAttributes(sensor))
	factory = factory.Varyings(ConvertVar(var))
	factory = factory.Reactions(ConvertReact(react))

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

def Call(name, types, kwargs, *args):
	if len(types) == 0:
		raise RuntimeError("specify some types for link")

	keywords = ["const", "sensor", "var", "react", "single"]

	const = kwargs.get(keywords[0], {})
	sensor   = kwargs.get(keywords[1], {})
	var = kwargs.get(keywords[2], {})
	react = kwargs.get(keywords[3], {})
	single    = kwargs.get(keywords[4], False)

	for key in kwargs:
		if key not in keywords:
			raise RuntimeError("unknown keyword: " + key)

	result = octotron.core.model.impl.ModelLinkList()

	for type in types:
		factory = GetLinkFactory(const, sensor, var, react, type)

		links = CallFactoryMethod(factory, name, args)

		if single:
			SystemCtx.Debug("created 1 link")
			result.add(links)
		else:
			SystemCtx.Debug("created " + str(links.size()) + " links")
			result.append(links)

	return result

def OneToOne(obj1, obj2, *types, **kwargs):
	kwargs["single"] = True
	result = Call(OneToOne.__name__, types, kwargs, obj1, obj2)

	if len(types) == 1:
		return result.get(0) # return the single object, if is the only

def OneToEvery(obj1, obj2, *types, **kwargs):
	Call(OneToEvery.__name__, types, kwargs, obj1, obj2)

def EveryToOne(obj1, obj2, *types, **kwargs):
	Call(EveryToOne.__name__, types, kwargs, obj1, obj2)

def AllToAll(obj1, obj2, *types, **kwargs):
	Call(AllToAll.__name__, types, kwargs, obj1, obj2)

def EveryToEvery(obj1, obj2, *types, **kwargs):
	Call(EveryToEvery.__name__, types, kwargs, obj1, obj2)

def ChunksToEvery(obj1, obj2, *types, **kwargs):
	Call(ChunksToEvery.__name__, types, kwargs, obj1, obj2)

def EveryToChunks(obj1, obj2, *types, **kwargs):
	Call(EveryToChunks.__name__, types, kwargs, obj1, obj2)

def ChunksToEvery_LastLess(obj1, obj2, *types, **kwargs):
	Call(ChunksToEvery_LastLess.__name__, types, kwargs, obj1, obj2)

def EveryToChunks_LastLess(obj1, obj2, *types, **kwargs):
	Call(EveryToChunks_LastLess.__name__, types, kwargs, obj1, obj2)

def ChunksToEvery_Guided(obj1, obj2, guide, *types, **kwargs):
	Call(ChunksToEvery_Guided.__name__, types, kwargs, obj1, obj2, guide)

def EveryToChunks_Guided(obj1, obj2, guide, *types, **kwargs):
	Call(EveryToChunks_Guided.__name__, types, kwargs, obj1, obj2, guide)
