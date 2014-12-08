from octopy.utils import *

from ru.parallel.octotron.generators import ObjectFactory

from octopy.const_wrapper import *
from octopy.sensor_wrapper import *
from octopy.var_wrapper import *
from octopy.react_wrapper import *

def CreateObject(*modules):
	return CreateObjects(1, *modules).Only()

def CreateObjects(count, *modules):
	params = MergeDicts(modules)

	CheckAllowed(params)

	factory = ObjectFactory(context.model_service)

	factory = factory.Constants(ConvertConsts(params["const"]))
	factory = factory.Constants(ConvertConsts(params["static"]))
	factory = factory.Sensors  (ConvertSensors(params["sensor"]))
	factory = factory.Vars     (ConvertVars(params["var"]))

	factory = factory.Reactions(ConvertReacts(params["react"]))

	return factory.Create(count)

def UpdateObject(object, *modules):
	params = MergeDicts(modules)

	CheckAllowed(params)

	object.GetBuilder(context.model_service).DeclareConst(ConvertConsts(params["const"]))
	object.GetBuilder(context.model_service).DeclareConst(ConvertConsts(params["static"]))
	object.GetBuilder(context.model_service).DeclareSensor(ConvertSensors(params["sensor"]))
	object.GetBuilder(context.model_service).DeclareVar(ConvertVars(params["var"]))

	object.GetBuilder(context.model_service).AddReaction(ConvertReacts(params["react"]))
