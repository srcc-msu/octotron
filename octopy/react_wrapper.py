from octopy.utils import *

from ru.parallel.octotron.reactions.CommonReactions import Info
from ru.parallel.octotron.reactions.CommonReactions import Warning
from ru.parallel.octotron.reactions.CommonReactions import Danger
from ru.parallel.octotron.reactions.CommonReactions import Critical
from ru.parallel.octotron.reactions.CommonReactions import Recover

from ru.parallel.octotron.generators.tmpl import ReactionTemplate
from ru.parallel.octotron.generators.tmpl import ReactionAction as Reaction

def ReactsFromDict(reactions_dict):
	res = []

	for name, reaction in reactions_dict.items():
		if len(reaction) > 1:
			raise RuntimeError("duplicated reaction: " + name + " : " + str(reaction))

		res.append(ReactionTemplate(name, reaction[0]))

	return res

def ConvertReacts(var):
	return ReactsFromDict(MergeDicts(var))
