import re

from ru.parallel.octotron.core.collections import ModelList as ModelList

ID_NAME = "_id"

prog = re.compile("{[^}]+}")

def GenID(target, format = "{type}", n = None):
	if '#' in format:
		raise RuntimeError("_id must not include # symbol")

	if not isinstance(target, ModelList):
		to_process = ModelList.Single(target)
	else:
		to_process = target

	i = 0 if n is None else n

	for entity in to_process:
		user_str = format

		while prog.search(user_str):
			match = prog.search(user_str)
			user_str = user_str.replace(match.group(0), entity.GetAttribute(match.group(0)[1:-1]).GetString())

		id_str = user_str + "-" + str(i)

		if id_str in GenID.declared:
			raise RuntimeError("_id is already declared: " + id_str)

		if entity.TestAttribute(ID_NAME):
			raise RuntimeError("object has _id already: "
				+ entity.GetAttribute(ID_NAME).GetString() + "; declined _id: " + id_str)

		GenID.declared.add(id_str)

		entity.GetBuilder().DeclareConst(ID_NAME, id_str)

		i += 1

	return target

GenID.declared = set()

def GenNestedID(targets, parents, format = "{type}"):
	for i, entity in enumerate(targets):
		target_parents = entity.GetInNeighbors().Uniq();

		for target_parent in target_parents:
			if target_parent in parents:
				target_parent_id = target_parent.GetAttribute(ID_NAME).GetString()
				GenID(entity, target_parent_id + "_" + format, n = i)
