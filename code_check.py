#!/usr/bin/env python3
"""
check the security and functionability of uploaded code 
- forbid from importing os
- random chessboard check
- some special case check
"""
import imp
import traceback
import sys
import numpy as np
from timeout_decorator import timeout
from socketIO_client import SocketIO

from chess_case import ChessCase

FORBIDDEN_LIST = ['import os', 'exec']

class CodeCheck():
    def __init__ (self, script_file_path, chessboard_size):
        self.time_out = 5
        self.script_file_path = script_file_path
        self.chessboard_size = chessboard_size
        self.agent = None
        self.errormsg = ''
        # sys.stdout = open(os.devnull, 'w')
        # sys.stderr = open(os.devnull, 'w')
        # print(self.chessboard)

    # Call this function and get True or False, self.errormsg has the massage
    def check_code(self):
        # check if contains forbidden library
        try:
            if self.__check_forbidden_import() == False:
                return False
        except Exception:
            self.errormsg = self.errormsg + traceback.format_exc()
            return False
    
        # check initialization
        try:
            timeout(self.time_out)(self.time_out_init)()
            # self.time_out_init()
        except Exception:
            self.errormsg = "Your code fail to init." + traceback.format_exc()
            return False
    
        # check simple condition
        if not self.__check_simple_chessboard():
            self.errormsg = "Your code can not pass usability test." + self.errormsg
            return False
    
        # check advance condition, online test contain more test case than this demo
        if not self.__check_advance_chessboard():
            self.errormsg = "Your code is too weak, fail to pass advance test." + self.errormsg
            return False

        return True

    def time_out_init (self):
        self.agent = imp.load_source('AI', self.script_file_path).AI(self.chessboard_size, 1, self.time_out)
        self.agent = imp.load_source('AI', self.script_file_path).AI(self.chessboard_size, -1, self.time_out)

    def __check_forbidden_import(self):
        with open(self.script_file_path, 'r', encoding='UTF-8') as myfile:
            data = myfile.read()
            for keyword in FORBIDDEN_LIST:
                idx = data.find(keyword)
                if idx != -1:
                    self.errormsg = "import forbidden"
                    return False
        return True
    
    def __check_go (self, chessboard):
        self.agent = imp.load_source('AI', self.script_file_path).AI(self.chessboard_size, -1, self.time_out)
        try:
            # self.agent.go(np.copy(chessboard))
            timeout(self.time_out)(self.agent.go)(np.copy(chessboard))
        except Exception:
            if len(self.agent.candidate_list) == 0:
                self.errormsg = "Error: Time out and candidate list empty." + traceback.format_exc()
                return False
        return True
    
    def __check_result (self, chessboard, result):
        try:
            if not self.__check_go(chessboard):
                return False
            if not self.agent.candidate_list or list(self.agent.candidate_list[-1]) not in result:
                print('user go:', list(self.agent.candidate_list[-1]))
                return False
        except Exception:
            self.errormsg = traceback.format_exc()
            return False
        return True
        
    def __check_simple_chessboard(self):
        # empty chessboard
        if not self.__check_go(np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)):
            return False
    
        # only one empty position remain
        for j in range(5):
            chessboard = np.ones((self.chessboard_size, self.chessboard_size))
            chessboard[:, ::2] = -1
            for i in range(0, self.chessboard_size, 4):
                chessboard[i] = -chessboard[i]
            x, y = np.random.choice(self.chessboard_size, 2)
            chessboard[x, y] = 0
    
            if not self.__check_result(chessboard, [[x, y]]):
                return False

        return True
    
    def __check_advance_chessboard (self):
        case_list = ChessCase.load_cases_files("testcases.txt")
        for case in case_list:
            if not self.__check_result(case.get_board(), case.get_rational_steps()):
                print((case.get_board(), case.get_rational_steps()))
                return False
        return True


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
