from socketIO_client import SocketIO, BaseNamespace

class Namespace(BaseNamespace):
    def on_connect(selpif):
        print ('[Connected]')

    def on_check_games (selpif, data):
        print(data)

socketIO = SocketIO('10.20.96.148', 8080, Namespace)
# socketIO.emit("downtime", {'can_play': False, 'message': "System will update soon, please don't open new game."})
# socketIO.emit("downtime", {'can_play': True, 'message': "System have updated."})
socketIO.emit("check_games", 0)

socketIO.wait(seconds=2)