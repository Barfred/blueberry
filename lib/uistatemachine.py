from statemachine import StateMachine, State

# TODO: need a call back for showpresetradioselections to harvest radiostations!
class UIStateMachine(StateMachine):
    player = State('Player', initial=True)
    presetradioselect = State('PresetRadioSelect')

    showpresetradioselections = player.to(presetradioselect)
    showplayer = presetradioselect.to(player)


