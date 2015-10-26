from octopy.utils import *

from ru.parallel.octotron.generators import ObjectFactory
from ru.parallel.octotron.core.collections import ModelObjectList as ModelObjectList

from octopy.const_wrapper import *
from octopy.sensor_wrapper import *
from octopy.var_wrapper import *
from octopy.react_wrapper import *
from octopy.trigger_wrapper import *

def CreateObject(*modules):
	return CreateObjects(1, *modules).Only()

def CreateObjects(count, *modules):
	params = MergeDicts(modules)

	CheckAllowed(params)

	factory = ObjectFactory()

	factory = factory.Constants(ConvertConsts  (params["const"]))
	factory = factory.Statics  (ConvertConsts  (params["static"]))
	factory = factory.Sensors  (ConvertSensors (params["sensor"]))
	factory = factory.Triggers (ConvertTriggers(params["trigger"]))
	factory = factory.Vars     (ConvertVars    (params["var"]))
	factory = factory.Reactions(ConvertReacts(params["react"]))

	objects = factory.Create(count)

	CreateObjects.all_objects = CreateObjects.all_objects.append(objects)

	return objects

CreateObjects.all_objects = ModelObjectList()

def UpdateObject(object, *modules):
	params = MergeDicts(modules)

	CheckAllowed(params)

	object.GetBuilder().DeclareConst(ConvertConsts(params["const"]))
	object.GetBuilder().DeclareStatic(ConvertConsts(params["static"]))
	object.GetBuilder().DeclareSensor(ConvertSensors(params["sensor"]))
	object.GetBuilder().DeclareVar(ConvertVars(params["var"]))
	object.GetBuilder().DeclareTrigger(ConvertTriggers(params["trigger"]))
	object.GetBuilder().DeclareReaction(ConvertReacts(params["react"]))
