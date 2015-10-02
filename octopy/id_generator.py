import re

from ru.parallel.octotron.core.collections import ModelList as ModelList

ID_NAME = "_id"
ID_SEPARATOR = "#"

prog = re.compile("{[^}]+}")

def GenID(target, format = "{type}"):
	if not isinstance(target, ModelList):
		to_process = ModelList.Single(target)
	else:
		to_process = target

	for i, entity in enumerate(to_process):
		user_str = format

		while prog.search(user_str):
			match = prog.search(user_str)
			user_str = user_str.replace(match.group(0), entity.GetAttribute(match.group(0)[1:-1]).GetString())

		id_str = user_str + "-" + str(i)

		if id_str in GenID.declared:
			raise RuntimeError("id is already declared: " + id_str)

		GenID.declared.add(id_str)

		entity.GetBuilder().DeclareConst(ID_NAME, id_str)

	return target

GenID.declared = set()
