from socketIO_client import SocketIO, BaseNamespace

class Namespace(BaseNamespace):
    def on_connect(selpif):
        print ('[Connected]')

    def on_reply (selpif, data):
        for d in data:
            print(d)

socketIO = SocketIO('localhost', 8080, Namespace)
socketIO.emit("go", "finally")
socketIO.wait(seconds=1)