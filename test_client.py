from socketIO_client import SocketIO, BaseNamespace

class Namespace(BaseNamespace):
    def on_connect(selpif):
        print ('[Connected]')

    def on_update_list (selpif, data):
        print(a)
a = [1,2]
socketIO = SocketIO('10.20.96.148', 8080, Namespace)
socketIO.emit("update_list", 'update')
socketIO.wait(seconds=1)