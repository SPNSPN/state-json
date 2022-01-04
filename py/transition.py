#! /usr/bin/env python3

import json

def find_if (pred, collection):
	try:
		return next(filter(pred, collection))
	except StopIteration:
		return None

class Transition:
	def __init__ (self, initial_state_name):
		self.initial = initial_state_name
		self.states = []
		self.current = self.initial

	def regist_state (self, state):
		self.states.append(state)

	DOT_TEMPLATE = """
digraph transition {{
graph [
	charset = "UTF-8"
	, label = "transition graph"
	, labelloc = "t"
	, labeljust = "c"
	, bgcolor = "#ffffff"
	, fontcolor = black
	, fontsize = 18
	, style = "filled"
	, rankdir = TB
	, margin = 0.2
	, splines = spline
	, ranksep = 1.0
	, nodesep = 0.9
];
node [
	colorscheme = "rdylgn11"
	, style = "solid"
	, fontsize = 16
	, fontcolor = black
	, fontname = "Migu 1M"
	, color = black
	, fillcolor = 7
	, fixedsize = true
	, height = 0.6
	, width = 1.2
];
edge [
	style = solid
	, fontsize = 10
	, fontcolor = black
	, fontname = "Migu 1M"
	, color = black
	, labelfloat = true
	, labeldistance = 2.5
	, labelangle = 70
];
{nodes}
{edges}
}}
"""
	NODE_TEMPLATE = "{0} [shape = box];\n"
	EDGE_TEMPLATE = "{0} -> {1} [label = \"{2}\n({3})\", arrowhead = normal];\n"
	def to_diagram (self):
		nodes = "s [shape = circle, width = 0.1];\n"
		edges = Transition.EDGE_TEMPLATE.format("s", self.initial, "", "初期状態")
		for st in self.states:
			nodes += Transition.NODE_TEMPLATE.format(st.name)
			for cond in st.conditions:
				edges += Transition.EDGE_TEMPLATE.format(st.name, cond.next, cond.name, cond.comment)
		return Transition.DOT_TEMPLATE.format(nodes = nodes, edges = edges)

	def to_json (self):
		jsondict = {"initial": self.initial, "states": []}
		for st in self.states:
			statedict = {"name": st.name, "conditions": []}
			for cond in st.conditions:
				statedict["conditions"].append(\
						{"name": cond.name, "next": cond.next, "comment": cond.comment})
			jsondict["states"].append(statedict)
		return json.dumps(jsondict, ensure_ascii = False)

	def from_json (self, jsonstr):
		jsondict = json.loads(jsonstr)
		self.initial = jsondict["initial"]
		self.current = self.initial
		self.states = []
		statedicts = jsondict["states"]
		for st in statedicts:
			state = TransitionState(st["name"])
			conditiondicts = st["conditions"]
			for cond in conditiondicts:
				def incomplete_state ():
					raise RuntimeError("incomplete state: {0}. (load from json)".format(cond["name"]))
				state.regist_condition(cond["name"], cond["next"], incomplete_state, cond["comment"])
			self.regist_state(state)

	def update_check_fn (self, state_name, condition_name, check_fn):
		state_info = find_if(lambda  e: e.name == state_name, self.states)
		if state_info is None:
			raise RuntimeError("unregistered state: {0}".format(state_name))

		condition_info = find_if(lambda e: e.name == condition_name, state_info.conditions)
		if condition_info is None:
			raise RuntimeError("unregistered condition: {0}, at {1}".format(condition_name, state_name))

		condition_info.check = check_fn

	def fill_check_fn (self, check_fn):
		for st in self.states:
			for cond in st.conditions:
				cond.check = check_fn

	def initialize (self):
		self.current = self.initial

	def transit (self, condition_name):
		state_info = find_if(lambda e: e.name == self.current, self.states)
		if state_info is None:
			raise RuntimeError("unknown state: {0}".format(self.current))
		condition_info = find_if(lambda e: e.name == condition_name, state_info.conditions)
		if condition_info is None:
			raise RuntimeError("unregistered condition: {0}, at {1}".format(condition_name, self.current))
		if condition_info.check():
			self.current = condition_info.next
			print("transit to {0}".format(self.current))
			return True
		else:
			print("fail transit by condition: {0}".format(condition_name))
			return False

class TransitionState:
	def __init__ (self, name):
		self.name = name
		self.conditions = []

	def regist_condition (self, condition):
		self.conditions.append(condition)

	def regist_condition (self, name, next_state_name, check_fn, comment):
		self.conditions.append(TransitionCondition(name, next_state_name, check_fn, comment))

class TransitionCondition:
	def __init__ (self, name, next_state_name, check_fn, comment):
		self.name = name
		self.next = next_state_name
		self.check = check_fn
		self.comment = comment

