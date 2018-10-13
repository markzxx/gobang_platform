#!/usr/bin/env python3
import sys

from socketIO_client import SocketIO

from code_check import CodeCheck

if __name__ == '__main__':
    path = sys.argv[1]
    sid = sys.argv[2]
    info = ""
    is_pass = False
    code_checker = CodeCheck("{}/{}.py".format(path, sid), 15)
    if not code_checker.check_code():
        print(code_checker.errormsg)
        info = code_checker.errormsg
    else:
        print('pass')
        info = 'Upload success, usability test pass.'
        is_pass = True
    
    socketIO = SocketIO('localhost', 8080)
    socketIO.emit("upload_test", {'sid': sid, 'info': info, 'is_pass': is_pass})
    socketIO.wait(seconds=1)
