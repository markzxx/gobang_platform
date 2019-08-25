import numpy as np
import random


class AI(object):
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.time_out = time_out
        self.chessboard = np.zeros((chessboard_size, chessboard_size), dtype=np.int)
        self.candidate_list = []
        if color == -1:
            self.chessboard[self.chessboard_size//2,self.chessboard_size//2] = -1

    def first_chess(self):
        assert self.color ==-1
        self.candidate_list.clear()
        self.candidate_list.append((self.chessboard_size//2,self.chessboard_size//2))
        self.chessboard[self.candidate_list[-1][0], self.candidate_list[-1][0]] = self.color


    def go(self, chessboard):
        self.candidate_list.clear()
        self.chessboard = chessboard
        idx = np.where(self.chessboard == 0)
        idx = list(zip(idx[0], idx[1]))
        pos_idx = random.randint(0, len(idx) - 1)
        new_pos = idx[pos_idx]
        assert self.chessboard[new_pos[0],new_pos[1]]==0
        self.candidate_list.append(new_pos)


