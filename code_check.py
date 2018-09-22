#!/usr/bin/env python3
"""
check the security and functionability of uploaded code 
- forbid from importing os (although not a good way compared to sandbox)
- scanning for 'import os' and 'exec'
- random chessboard check
"""
import imp
import sys
import os
import traceback

from timeout_decorator import timeout
import timeout_decorator
import numpy as np


FORBIDDEN_LIST = ['import os', 'exec']

class CodeCheck():
    def __init__(self, script_file_path):
        self.time_out = 1
        self.script_file_path = script_file_path
        self.chessboard_size = 15
        self.agent = None
        self.test_color = -1
        tmp0 = [1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1]
        tmp1 = np.stack([tmp0]*3)
        tmp2 = -tmp1
        self.chessboard = np.concatenate([tmp1, tmp2, tmp1, tmp2, tmp1], axis=0)
        idx = np.random.choice(15*15, 10)
        self.chessboard = np.reshape(self.chessboard, [15*15])
        self.chessboard[idx] = 0
        self.chessboard = np.reshape(self.chessboard, [15, 15])
        self.errormsg = ''
        # print(self.chessboard)
        
    
    def check_code(self):
        if self.__check_forbidden_import() == False:
            return False
        self.agent = imp.load_source('AI', self.script_file_path).AI(self.chessboard_size, 1, self.time_out)
        print("check1 passed")
        if self.__check_simple_chessboard() == False:
            return False
        print("check2 passed")
        return True


    def __check_forbidden_import(self):
        '''
        :return 1: ok
        :return 0: import error 
        '''
        with open(self.script_file_path, 'r') as myfile:
            data = myfile.read()
            for keyword in FORBIDDEN_LIST:
                idx = data.find(keyword)
                if idx != -1:
                    self.errormsg = "import forbidden"
                    return False
        return True
        
    def __check_simple_chessboard(self):
        try:
            timeout(1)(self.agent.go)(self.chessboard)
        except MemoryError:
            self.errormsg = "Memory Error"
        except timeout_decorator.timeout_decorator.TimeoutError:
            self.errormsg = "Time Limit Exceeded"
        
        ## check validity
        try:
            if self.chessboard[self.agent.candidate_list[-1]] == 0:
                return True
            else:
                self.errormsg = "Invalid Position"
                return False
        except ValueError:
            self.errormsg = "Invalid Position"
            return False
        except IndexError:
            self.errormsg = "Invalid Position"
            return False