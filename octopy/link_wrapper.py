from octopy.system import SystemCtx
from octopy.utils import *

import ru.parallel.octotron as octotron

def GetLinkFactory(attributes, rules, reactions, type):
	factory = octotron.generators.LinkFactory(SystemCtx.GetGraphService())

	factory = factory.Attributes(ConvertAttributes(attributes))
	factory = factory.Rules(ConvertRules(rules))
	factory = factory.Reactions(ConvertReactions(reactions))

	return factory.Attributes(octotron.primitive.SimpleAttribute("type", type))

def CallFactoryMethod(factory, name, args):
	arg_types = map(lambda x: x.class, args)

	method = factory.getClass().getMethod(name, arg_types)

	return method.invoke(factory, args)

def Call(name, types, kwargs, *args):
	if len(types) == 0:
		raise RuntimeError("specify some types for link")

	keywords = ["attributes", "rules", "reactions"]

	attributes = kwargs.get(keywords[0], {})
	rules      = kwargs.get(keywords[1], {})
	reactions  = kwargs.get(keywords[2], {})

	for key in kwargs:
		if key not in keywords:
			raise RuntimeError("unknown keyword: " + key)

	result = octotron.utils.OctoLinkList()

	for type in types:
		factory = GetLinkFactory(attributes, rules, reactions, type)

		links = CallFactoryMethod(factory, name, args)
		SystemCtx.Debug("created " + str(links.size()) + " links")
		result.append(links)

	return result

def OneToOne(obj1, obj2, *types, **kwargs):
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

Enumerator = octotron.generators.Enumerator
