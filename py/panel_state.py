#! /usr/bin/env python3
#! -*- coding: utf-8 -*-

from transition import *

def allow_always ():
	return True

def deny_always ():
	return False

manual_state = TransitionState("manual")
manual_state.regist_condition("select_auto", "prerun", allow_always, "常に成功")
manual_state.regist_condition("click_autorun", "autorun", deny_always, "常に失敗")
manual_state.regist_condition("click_estop", "stop", allow_always, "常に成功")

prerun_state = TransitionState("prerun")
prerun_state.regist_condition("select_manu", "manual", allow_always, "常に成功")
prerun_state.regist_condition("click_auto", "autorun", allow_always, "常に成功")
prerun_state.regist_condition("click_estop", "stop", allow_always, "常に成功")

autorun_state = TransitionState("autorun")
autorun_state.regist_condition("select_manu", "manual", allow_always, "常に成功")
autorun_state.regist_condition("click_estop", "stop", allow_always, "常に成功")

stop_state = TransitionState("stop")
stop_state.regist_condition("click_reset", "manual", allow_always, "常に成功")

machine = Transition("manual")
machine.regist_state(manual_state)
machine.regist_state(prerun_state)
machine.regist_state(autorun_state)
machine.regist_state(stop_state)

