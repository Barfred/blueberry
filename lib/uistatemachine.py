from statemachine import StateMachine, State


class UIStateMachine(StateMachine):
    player = State('Player', initial=True)
    radioselect = State('RadioSelect')
    playlistselect = State('PlaylistSelect')
    queueselect = State('QueueSelect')

    playernextmenu = player.to(radioselect)

    radionextmenu = radioselect.to(playlistselect)
    playlistnextmenu = playlistselect.to(queueselect)
    queueselectnextmenu = queueselect.to(radioselect)

    playradio = radioselect.to(player)
    playplaylist = playlistselect.to(player)
    playqueue = queueselect.to(player)


