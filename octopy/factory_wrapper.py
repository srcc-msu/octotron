from octopy.utils import *

#from ru.parallel.octotron.generators import Enumerator
#from ru.parallel.octotron.generators import CSVReader
from ru.parallel.octotron.generators import ObjectFactory

def CreateObject(*modules):
	return CreateObjects(1, *modules).Only()

def CreateObjects(count, *modules):
	params = MergeDicts(modules)

	factory = ObjectFactory(context.model_service)

	factory = factory.Constants(ConvertAttributes(MergeDicts(params["const"])))
	factory = factory.Constants(ConvertAttributes(MergeDicts(params["static"])))
	factory = factory.Sensors  (ConvertAttributes(MergeDicts(params["sensor"])))
	factory = factory.Varyings (ConvertVars(MergeDicts(params["var"])))

	factory = factory.Reactions(ConvertReacts(MergeUniqueDicts(params["react"])))

	return factory.Create(count)

def UpdateObject(object, *modules):
	params = MergeDicts(modules)

	object.GetBuilder(context.model_service).DeclareConst(ConvertAttributes(MergeDicts(params["const"])))
	object.GetBuilder(context.model_service).DeclareConst(ConvertAttributes(MergeDicts(params["static"])))
	object.GetBuilder(context.model_service).DeclareSensor(ConvertAttributes(MergeDicts(params["sensor"])))
	object.GetBuilder(context.model_service).DeclareVar(ConvertVars(MergeDicts(params["var"])))

	object.GetBuilder(context.model_service).AddReaction(ConvertReacts(MergeUniqueDicts(params["react"])))
