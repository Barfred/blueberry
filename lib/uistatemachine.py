from statemachine import StateMachine, State


class UIStateMachine(StateMachine):
    player = State('Player', initial=True)
    presetradioselect = State('PresetRadioSelect')
    playlistselect = State('PlaylistSelect')

    showpresetradioselections = player.to(presetradioselect)
    showplayer = presetradioselect.to(player)
    showplayerfromplaylist = playlistselect.to(player)


