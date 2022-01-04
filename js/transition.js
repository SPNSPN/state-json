"use strict"

function Transition (initial_state_name)
{
	this.initial = initial_state_name;
	this.states = [];
	this.current = this.initial;

	this.regist_state = function (state)
	{
		this.states.push(state)
	};

	this.format_dot_template = function (nodes, edges)
	{
		return `
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
${nodes}
${edges}
}}
`;
	};
	this.format_node_template = function (node)
	{
		return `${node} [shape = box];\n`;
	};
	this.format_edge_template = function (n1, n2, e, ee)
	{
		return `${n1} -> ${n2} [label = "${e}\n${ee}", arrowhead = normal];\n`;
	};
	this.to_diagram = function ()
	{
		let nodes = "s [shape = circle, width = 0.1];\n";
		let edges = this.format_edge_template("s", this.initial, "", "初期状態");
		this.states.map((st) =>
				{
					nodes += this.format_node_template(st.name);
					st.conditions.map((cond) =>
							{
								edges += this.format_edge_template(st.name, cond.next, cond.name, cond.comment);
							});
				});
		return this.format_dot_template(nodes, edges);
	};

	this.to_json = function ()
	{
		let jsonobj = {"initial": this.initial};
		jsonobj.states = this.states.map((st) =>
				{
					let stateobj = {"name": st.name};
					stateobj.conditions = st.conditions.map((cond) =>
							{
								return {"name": cond.name, "next": cond.next, "comment": cond.comment}
							});
					return stateobj;
				});
		return JSON.stringify(jsonobj);
	};

	this.from_json = function (jsonstr)
	{
		let jsonobj = JSON.parse(jsonstr);
		this.initial = jsonobj.initial;
		this.current = this.initial;
		this.states = [];
		jsonobj.states.map((st) =>
				{
					let state = new TransitionState(st.name);
					let conditionobjs = st.conditions;
					conditionobjs.map((cond) =>
							{
								let incomplete_state = function ()
								{
									throw new Error(`incomplete state: ${cond.name}. (load from json)`);
								};
								state.regist_condition(cond.name, cond.next, incomplete_state, cond.comment);
							});
					this.regist_state(state);
				});
	};

	this.update_check_fn = function (state_name, condition_name, check_fn)
	{
		let state_info = this.states.find((e) => e.name == state_name);
		if (undefined === state_info) { throw new Error(`unregistered state: ${state_name}`); }

		let condition_info = state_info.conditions.find((e) => e.name == condition_name);
		if (undefined === condition_info) { throw new Error(`unregistered condition: ${condition_name}, at ${state_name}`); }

		condition_info.check = check_fn;
	};

	this.fill_check_fn = function (check_fn)
	{
		this.states.map((st) =>
				{
					st.conditions.map((cond) => { cond.check = check_fn; });
				});
	};

	this.initialize = function ()
	{
		this.current = this.initial;
	}

	this.transit = function (condition_name)
	{
		let state_info = this.states.find((e) => e.name == this.current);
		if (undefined === state_info) { throw new Error(`unknown state: ${this.current}`); }

		let condition_info = state_info.conditions.find((e) => e.name == condition_name);
		if (undefined === condition_info) { throw new Error(`unregistered condition: ${condition_name}, at ${this.current}`); }

		if (condition_info.check())
		{
			this.current = condition_info.next;
			console.log(`transit to ${this.current}`);
			return true;
		}
		else
		{
			console.log(`fail to transit by condition: ${condition_name}`);
			return false;
		}
	}
}

function TransitionState (name)
{
	this.name = name;
	this.conditions = [];

	this.regist_condition = function (name, next_state_name, check_fn, comment)
	{
		this.conditions.push(new TransitionCondition(name, next_state_name, check_fn, comment));
	};
}

function TransitionCondition (name, next_state_name, check_fn, comment)
{
	this.name = name;
	this.next = next_state_name;
	this.check = check_fn;
	this.comment = comment;
}
