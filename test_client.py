from time import sleep

from socketIO_client import SocketIO, BaseNamespace


class Namespace(BaseNamespace):
    def on_connect(selpif):
        print ('[Connected]')

    def on_check_games (selpif, data):
        for a in data:
            print(a)


socketIO = SocketIO('10.20.96.148', 8080, Namespace)
# socketIO.emit("order", {'order':'down', 'params':{'can_play': False, 'message': "System will update soon, please don't open new game."}})
# socketIO.emit("order", {'order':'down', 'params':{'can_play': True, 'message': "System update success."}})
# socketIO.emit("order", {'order': 'update_rank', 'params': 0})
# socketIO.emit("check_games", 0)

for i in range(100, 0, -1):
    socketIO.emit('play', {'player': 11210162, 'tag': i})
    sleep(0.1)
    socketIO.emit('play', {'player': 11210162, 'tag': -i})

socketIO.wait(1)
