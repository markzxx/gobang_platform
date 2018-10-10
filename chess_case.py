#!/usr/bin/env python3
'''
This is the class to define the test cases to test the uploaded code.
'''
import numpy as np

class ChessCase():
    def __init__(self, chessboard_size):
        '''
        params: chessboard should have the same number of balck and white piece
        params: rational_steps: rational locations the next piece should be put
        '''
        self.chessboard = np.zeros((chessboard_size, chessboard_size), dtype=np.int)
        self.rational_steps = None

    def add_partial_board(self, board, offset):
        '''
         params: board: the partial board in numpy array
         params: offset location of the left top piece of the particial board in the main board
        '''
        shape = board.shape
        board[board==2] = -1
        self.chessboard[offset[0]:offset[0]+shape[0], offset[1]:offset[1]+shape[1]] = board

    @staticmethod
    def load_cases_files(filename):
        # filename='testcases.txt'
        case_list = []
        with open(filename) as fileobj:
            content = fileobj.read()
        usefulpart = content.split("###############")[1]
        all_cases = usefulpart.split("===============")
        for case in all_cases:
            new_case = ChessCase(15)
            subboards = case.split("---------------")
            for board in subboards:
                offset, arr_2d = ChessCase.__parse_array(board)
                if 3 in arr_2d:
                    rational_steps = np.argwhere(arr_2d==3)
                    new_case.set_rational_steps(rational_steps+offset)
                else:
                    new_case.add_partial_board(arr_2d, offset)
            case_list.append(new_case)
        return case_list
    @staticmethod
    def __parse_array(text):
        lines = text.split()
        offset = (int(lines[0]), int(lines[1]))
        arr_list = []
        for line in lines[2:]:
            arr_list.append(np.array([int(char) for char in line]))
        arr_2d = np.stack(arr_list)
        return offset, arr_2d
       #print(offset, lines)

    def get_board(self):
        return self.chessboard
    
    def get_rational_steps(self):
        '''
        -1 first
        '''
        return self.rational_steps

    def set_rational_steps(self, steps):
        '''
        -1 first
        '''
        self.rational_steps = steps