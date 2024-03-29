from socketIO_client import SocketIO, BaseNamespace


class Namespace(BaseNamespace):
    def on_connect(selpif):
        print ('[Connected]')

    def on_check_games (selpif, data):
        for a in data:
            print(data[a])

    def on_check_players (selpif, data):
        for a in data:
            print(a, data[a])


socketIO = SocketIO('10.20.96.148', 8080, Namespace)
# socketIO.emit("order", {'order': 'down', 'params': {'can_play': False, 'message': "Time out. Round-robin gaming is going."}})
# socketIO.emit("order", {'order':'down', 'params':{'can_play': True, 'message': "System update success."}})
# socketIO.emit("order", {'order': 'update_rank', 'params': 0})
# socketIO.emit("order", {'order': "check_games", 'params': 0})
# socketIO.emit("order", {'order': "check_players", 'params': 0})
socketIO.emit('round_play', {'player1': '11610408', 'player2': '11611313', 'tag': 1})

# for i in range(10, 0, -1):
#    socketIO.emit('play', {'player': 11210162, 'tag': i})

socketIO.wait(1)
