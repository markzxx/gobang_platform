#!/usr/bin/env python3
import sys

from code_check import CodeCheck

if __name__ == '__main__':
    path = sys.argv[1]
    userlist = sys.argv[2]
    passlist = sys.argv[3]
    f_user = open(userlist,'r')
    f_pass = open(passlist, 'w')
    for sid in f_user.readlines():
        sid = sid.strip('.py\n')
        is_pass = False
        code_checker = CodeCheck("{}/{}.py".format(path, sid), 15)
        if not code_checker.check_code():
            info = code_checker.errormsg
        else:
            f_pass.writelines("%s\n" % sid)
            info = 'Upload success, usability test pass.'
            is_pass = True

