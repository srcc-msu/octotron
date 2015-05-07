from octopy.utils import *

from ru.parallel.octotron.reactions.CommonReactions import Info
from ru.parallel.octotron.reactions.CommonReactions import Warning
from ru.parallel.octotron.reactions.CommonReactions import Danger
from ru.parallel.octotron.reactions.CommonReactions import Critical
from ru.parallel.octotron.reactions.CommonReactions import Recover

from ru.parallel.octotron.generators.tmpl import ReactionTemplate as Reaction

def ConvertReacts(react):
	if not isinstance(react, list):
		raise ValueError("list expected, got: " + str(react))

	return ReactionsFromList(react)
