from socketIO_client import SocketIO, BaseNamespace

class Namespace(BaseNamespace):
    def on_connect(selpif):
        print ('[Connected]')

    def on_reply (selpif, data):
        for d in data:
            print(d)

socketIO = SocketIO('10.20.96.148', 8080, Namespace)
for sid in [123,456,888,111]:
    socketIO.emit("play", {'sid':sid})
socketIO.wait(seconds=1)