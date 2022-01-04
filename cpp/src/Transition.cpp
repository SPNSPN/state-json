#include "Transition.h"

TransitionCondition::TransitionCOndition (const std::string &name, const std::string &next_state_name, const std::function<bool()> &check_fn, const std::string &comment)
	: name(name)
	  , next(next_state_name)
	  , check(check_fn)
	  , comment(comment)
{
}

TransitionState::TransitionState (const std::string &name)
	: name(name)
	  , conditions()
{
}

void TransitionState::regist_condition (TransitionCondition condition)
{
	conditions.push_back(condition);
}

void TransitionState::regist_condition (const std::string &name, const std::string &next_state_name, const std::function<bool()> &check_fn, const std::string &comment)
{
	condition.push_back(TransitionCondition(name, next_state_name, check_fn, comment));
}


Transition::Transition (const std::string &initial_state_name)
	: initial(initial_state_name)
	  , states()
	  , current(initial_state_name)
{
}

void Transition::regist_state (TransitionState state)
{
	states.push_back(state);
}

std::string Transition::to_diagram ()
{
	assert(false);
}

std::string Transition::to_json ()
{
	assert(false);
}

void Transition::from_json (const  std::string &jsonstr)
{
	assert(false);
}

void Transition::update_check_fn (const std::string &state_name, const std::string &condition_name, const std::function<bool()> &check_fn)
{
	assert(false);
}

void Transition::fill_check_fn (const std::function<bool()> &check_fn)
{
	assert(false);
}

void Transition::initialize ()
{
	current = initial;
}

bool Transition::transit (const std::string &condition_name)
{
	assert(false);
}
