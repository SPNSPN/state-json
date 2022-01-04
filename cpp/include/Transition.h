#include <string>
#include <vector>
#include <function>

class TransitionCondition
{
	private:
		std::string name;
		std::string next;
		std::function<bool()> check;
		std::string comment;

	public:
		TransitionCondition (const std::string &name, const std::string &next_state_name, const std::function<bool()> &check_fn, const std::string &comment);
};

class TransitionState
{
	private:
		std::string name;
		std::vector<TransitionCondition> conditions;

	public:
		TransitionState (const std::string &name);
		void regist_condition (TransitionCondition condition);
		void regist_condition (const std::string &name, const std::string &next_state_name, const std::function<bool()> &check_fn, const std::string &comment);
};

class Transition
{
	private:
		std::string initial;
		std::vector<TransitionState> states;
		std::string current;

	public:
		Transition (const std::string &initial_state_name);

		void regist_state (TransitionState state);
		std::string to_diagram ();
		std::string to_json ();
		void from_json (const  std::string &jsonstr);
		void update_check_fn (const std::string &state_name, const std::string &condition_name, const std::function<bool()> &check_fn);
		void fill_check_fn (const std::function<bool()> &check_fn);
		void initialize ();
		bool transit (const std::string &condition_name);
};
