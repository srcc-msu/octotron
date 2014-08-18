from octopy.system import SystemCtx
from octopy.utils import *

import ru.parallel.octotron as octotron

def CreateObjects(constants = None, sensors = None, variables = None, reactions = None, count = 1):
	if constants is None: constants = {}
	if sensors is None: sensors = {}
	if variables is None: variables = {}
	if reactions is None: reactions = {}

	SystemCtx.Debug("created a list with " + str(count) + " objects")

	factory = octotron.generators.ObjectFactory()

	factory = factory.Constants(ConvertAttributes(constants))
	factory = factory.Sensors(ConvertAttributes(sensors))
	factory = factory.Variables(ConvertVariables(variables))
	factory = factory.Reactions(ConvertReactions(reactions))

	return factory.Create(count)

def CreateObject(constants = None, sensors = None, variables = None, reactions = None):
	SystemCtx.Debug("created 1 object")

	return CreateObjects(constants, sensors, variables, reactions).Only()

Enumerator = octotron.generators.Enumerator
CSVReader = octotron.generators.CSVReader
