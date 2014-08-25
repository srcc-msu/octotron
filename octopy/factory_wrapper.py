from octopy.system import SystemCtx
from octopy.utils import *

import ru.parallel.octotron as octotron

def CreateObjects(const = None, static = None, sensor = None, var = None, react = None, count = None, modules):
	if const is None: const = {}
	if static is None: static = {}
	if sensor is None: sensor = {}
	if var is None: var = {}
	if react is None: react = {}

	factory = octotron.generators.ObjectFactory()

	factory = factory.Constants(ConvertAttributes(const))
	factory = factory.Sensors(ConvertAttributes(sensor))
	factory = factory.Varyings(ConvertVar(var))
	factory = factory.Reactions(ConvertReact(react))

	if count is None:
		count = 1

	return factory.Create(count)

def CreateObject(const = None, static = None, sensor = None, var = None, react = None):
	SystemCtx.Debug("created 1 object")
	return CreateObjects(const, static, sensor, var, react).Only()

Enumerator = octotron.generators.Enumerator
CSVReader = octotron.generators.CSVReader
