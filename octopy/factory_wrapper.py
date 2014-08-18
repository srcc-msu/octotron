from octopy.system import SystemCtx
from octopy.utils import *

import ru.parallel.octotron as octotron

def CreateObjects(const = None, static = None, sensor = None, var = None, react = None, count = None):
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
		SystemCtx.Debug("created 1 object")
		return factory.Create()
	else:
		SystemCtx.Debug("created a list with " + str(count) + " objects")
		return factory.Create(count)

Enumerator = octotron.generators.Enumerator
CSVReader = octotron.generators.CSVReader
