from octopy.utils import *

from ru.parallel.octotron.core.logic.impl import Equals
from ru.parallel.octotron.core.logic.impl import NotEquals

from ru.parallel.octotron.reactions.CommonReactions import Info
from ru.parallel.octotron.reactions.CommonReactions import Warning
from ru.parallel.octotron.reactions.CommonReactions import Danger
from ru.parallel.octotron.reactions.CommonReactions import Critical
from ru.parallel.octotron.reactions.CommonReactions import Recover

def ReactionsFromDict(react_dict):
	res = []

	for event, response in react_dict.items():
		collection = GetCollection(response)

		if len(collection) == 2:
			res.append(event.Response(collection[0]).RecoverResponse(collection[1]))
		elif len(collection) == 1:
			res.append(event.Response(collection[0]))
		else:
			raise RuntimeError("expected a single response or list/tuple with 2 responses, got: " + response)

	return res

def ConvertReacts(react):
	return ReactionsFromDict(MergeUniqueDicts(react))