"use strict"

function allow_always () { return true; }
function deny_always () { return false; }

let request = new XMLHttpRequest();
request.open("GET", "./panel_state.json");
request.send();

let machine = new Transition("");
request.onreadystatechange = function ()
{
	if (4 == request.readyState && 200 == request.status)
	{
		machine.from_json(request.responseText);
		machine.fill_check_fn(allow_always);
	}
};

