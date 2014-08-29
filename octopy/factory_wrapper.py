from octopy.system import SystemCtx
from octopy.utils import *

import ru.parallel.octotron as octotron

def CreateObject(*modules):
	return CreateObjects(1, *modules).Only()

def CreateObjects(count, *modules):
	params = MergeDicts(modules)

	factory = octotron.generators.ObjectFactory()

	factory = factory.Constants(ConvertAttributes(MergeDicts(params["const"])))
	factory = factory.Constants(ConvertAttributes(MergeDicts(params["static"])))
	factory = factory.Sensors  (ConvertAttributes(MergeDicts(params["sensor"])))
	factory = factory.Varyings (ConvertVars(MergeDicts(params["var"])))
	factory = factory.Reactions(ConvertReacts(MergeDicts(params["react"])))

	SystemCtx.Debug("created list with %d objects" % count)

	return factory.Create(count)

Enumerator = octotron.generators.Enumerator
CSVReader = octotron.generators.CSVReader

def UpdateObject(object, *modules):
	params = MergeDicts(modules)

	object.DeclareConstants(ConvertAttributes(MergeDicts(params["const"])))
	object.DeclareConstants(ConvertAttributes(MergeDicts(params["static"])))
	object.DeclareSensors(ConvertAttributes(MergeDicts(params["sensor"])))

	object.DeclareVaryings(ConvertVars(MergeDicts(params["var"])))
	object.AddReactions(ConvertReacts(MergeDicts(params["react"])))
