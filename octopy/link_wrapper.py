from octopy.system import SystemCtx
from octopy.utils import *

import ru.parallel.octotron as octotron

def GetLinkFactory(attributes):
	return octotron.generators \
		.LinkFactory(SystemCtx.GetGraphService()) \
		.Attributes(FromNested(attributes, AttributesFromDict))

def OneToOne(obj1, obj2, *attributes):
	if len(attributes) == 0:
		raise RuntimeError("specify some attributes for link")
	for attribute in attributes:
		GetLinkFactory(attribute).OneToOne(obj1, obj2)
		SystemCtx.Debug("created 1 link")

def OneToEvery(obj1, obj2, *attributes):
	if len(attributes) == 0:
		raise RuntimeError("specify some attributes for link")
	for attribute in attributes:
		size = GetLinkFactory(attribute).OneToEvery(obj1, obj2).size()
		SystemCtx.Debug("created " + str(size) + " links")

def EveryToOne(obj1, obj2, *attributes):
	if len(attributes) == 0:
		raise RuntimeError("specify some attributes for link")
	for attribute in attributes:
		size = GetLinkFactory(attribute).EveryToOne(obj1, obj2).size()
		SystemCtx.Debug("created " + str(size) + " links")

def AllToAll(obj1, obj2, *attributes):
	if len(attributes) == 0:
		raise RuntimeError("specify some attributes for link")
	for attribute in attributes:
		size = GetLinkFactory(attribute).AllToAll(obj1, obj2).size()
		SystemCtx.Debug("created " + str(size) + " links")

def EveryToEvery(obj1, obj2, *attributes):
	if len(attributes) == 0:
		raise RuntimeError("specify some attributes for link")
	for attribute in attributes:
		size = GetLinkFactory(attribute).EveryToEvery(obj1, obj2).size()
		SystemCtx.Debug("created " + str(size) + " links")

def ChunksToEvery(obj1, obj2, *attributes):
	if len(attributes) == 0:
		raise RuntimeError("specify some attributes for link")
	for attribute in attributes:
		size = GetLinkFactory(attribute).ChunksToEvery(obj1, obj2).size()
		SystemCtx.Debug("created " + str(size) + " links")

def EveryToChunks(obj1, obj2, *attributes):
	if len(attributes) == 0:
		raise RuntimeError("specify some attributes for link")
	for attribute in attributes:
		size = GetLinkFactory(attribute).EveryToChunks(obj1, obj2).size()
		SystemCtx.Debug("created " + str(size) + " links")

def ChunksToEvery_LastLess(obj1, obj2, *attributes):
	if len(attributes) == 0:
		raise RuntimeError("specify some attributes for link")
	for attribute in attributes:
		size = GetLinkFactory(attribute).ChunksToEvery_LastLess(obj1, obj2).size()
		SystemCtx.Debug("created " + str(size) + " links")

def EveryToChunks_LastLess(obj1, obj2, *attributes):
	if len(attributes) == 0:
		raise RuntimeError("specify some attributes for link")
	for attribute in attributes:
		size = GetLinkFactory(attribute).EveryToChunks_LastLess(obj1, obj2).size()
		SystemCtx.Debug("created " + str(size) + " links")

def ChunksToEvery_Guided(obj1, obj2, guide, *attributes):
	if len(attributes) == 0:
		raise RuntimeError("specify some attributes for link")
	for attribute in attributes:
		size = GetLinkFactory(attribute).ChunksToEvery_Guided(obj1, obj2, guide).size()
		SystemCtx.Debug("created " + str(size) + " links")

def EveryToChunks_Guided(obj1, obj2, guide, *attributes):
	if len(attributes) == 0:
		raise RuntimeError("specify some attributes for link")
	for attribute in attributes:
		size = GetLinkFactory(attribute).EveryToChunks_Guided(obj1, obj2, guide).size()
		SystemCtx.Debug("created " + str(size) + " links")

Enumerator = octotron.generators.Enumerator
