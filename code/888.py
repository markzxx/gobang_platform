import numpy as np
import random
import time

class AI(object):
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.time_out = time_out
        self.chessboard = np.zeros((chessboard_size, chessboard_size), dtype=np.int)

        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your decision .
        self.candidate_list = []

    # If your are first, this function will be used.
    def first_chess(self):
        assert self.color ==-1
        self.candidate_list.clear()
        self.candidate_list.append((self.chessboard_size//2,self.chessboard_size//2))
        self.chessboard[self.candidate_list[-1][0], self.candidate_list[-1][0]] = self.color

    # The input is postion of your competitor decision which look like (x1, y1).
    def go(self, pos):
        # Clear candidate_list
        self.candidate_list.clear()
        # Records the chess board
        self.chessboard[pos[0], pos[1]] = -self.color
        # Random decision
        idx = np.where(self.chessboard == 0)
        idx = list(zip(idx[0], idx[1]))
        pos_idx = random.randint(0, len(idx)-1)
        new_pos = idx[pos_idx]
        # Make sure that the position of your decision in chess board is empty. If not, return error.
        assert self.chessboard[new_pos[0],new_pos[1]]==0
        #Add your decision into candidate_list
        self.candidate_list.append(new_pos)
        # Records the chess board
        self.chessboard[new_pos[0],new_pos[1]]=self.color


