import numpy as np
import random


class renju(object):
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.time_out = time_out
        self.chessboard = np.zeros((chessboard_size, chessboard_size), dtype=np.int)
        if color==-1:
            self.chessboard[chessboard_size//2,chessboard_size//2]=self.color

    def output(self, pos):
        self.chessboard[pos[0], pos[1]] = -self.color
        idx = np.where(self.chessboard == 0)
        idx = list(zip(idx[0], idx[1]))
        pos_idx = random.randint(0, len(idx)-1)
        new_pos = idx[pos_idx]
        assert self.chessboard[new_pos[0],new_pos[1]]==0
        self.chessboard[new_pos[0],new_pos[1]]=self.color
        return new_pos
