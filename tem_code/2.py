# -*- coding:utf-8 -*
import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0


class AI(object):

    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.time_out = time_out
        self.candidate_list = []
        
    def count(self, chessboard, a, b, j, k, COLOR):
        i = 0
        while (-1 < a + j < 15 and -1 < b + k < 15 and chessboard[a + j, b + k] == COLOR):
            i = i + 1
            a = a + j
            b = b + k
        if (-1 < a + j < 15 and -1 < b + k < 15):
            if chessboard[a + j, b + k] == COLOR_NONE:
                i = i * 2
            else:
                i = i * 2 -1
        else:
            i = i * 2 - 1
        return i

    def calcute_value(self, chessboard, a, b, COLOR):
        x = []
        value = 0
        x.append(self.count(chessboard, a, b, 1, 1, COLOR))
        x.append(self.count(chessboard, a, b, -1, 1, COLOR))
        x.append(self.count(chessboard, a, b, 1, 0, COLOR))
        x.append(self.count(chessboard, a, b, 0, 1, COLOR))
        x.append(self.count(chessboard, a, b, -1, -1, COLOR))
        x.append(self.count(chessboard, a, b, 1, -1, COLOR))
        x.append(self.count(chessboard, a, b, -1, 0, COLOR))
        x.append(self.count(chessboard, a, b, 0, -1, COLOR))
        y = []
        for i in range(0, 4):
            flag = x[i] + x[i + 4]
            if flag > 6:
                y.append(1)
            elif flag == 6:
                if (x[i] * x[i + 4] < 0 or x[i] == x[i + 4] or (x[i] == 5 or x[i + 4] == 5)):
                    y.append(1)  # 五连
                else:
                    y.append(2)  # 活四
            elif flag == 5:
                y.append(3)  # 冲四
            elif flag == 4:
                if (x[i] * x[i + 4] < 0):
                    y.append(10)  # 死四
                else:
                    y.append(4)  # 活三
            elif flag == 3:
                y.append(5)  # 冲三
            elif flag == 2:
                if (x[i] == x[i + 4] or x[i] * x[i + 4] < 0):
                    y.append(10)  # 死二死三
                else:
                    y.append(6)  # 活二
            elif flag == 1:
                y.append(7)  # 冲二
            elif flag == 0:
                if (x[i] * x[i+4])==0:
                    y.append(8) #活一
                else:
                    y.append(10) #死二
            elif flag == -1:
                y.append(9) #冲一

        z = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for m in y:
            z[m] = z[m] + 1
        if z[1] > 0:
            value = 100
        elif z[2] > 0:
            value = 70 + z[3]*4 + z[4]*2
        elif z[3] > 1:  # 双冲四
            value = 60 + z[4]*2
        elif (z[3] > 0 and z[4 ] > 0):  # 四三
            value = 50 + z[3]*2
        elif z[4] > 1:  # 双三
            value = 40 + z[4]*2
        elif (z[4] > 0 and z[6] > 0):  # 活三+活二
            value = 30 + z[6]*2
        elif (z[4] > 0 and z[5] >0): #活三 + 冲三
            value = 26 + z[5]
        elif z[4] > 0:  # 活三
            value = 24
        elif z[3] > 0:  # 冲四
            value = 18 + z[3] + z[5]
        elif z[5] > 0:  # 冲三
            value = 10 + z[5] * 2
        elif (z[5] > 0 and z[6] > 0):#冲三+活二
            value = 10 + z[6]
        elif z[6] > 0: #活二
            value = 6 + z[6]
        elif z[7] > 0: #冲二
            value = 4 + z[7]
        elif z[8] > 0: #活一
            value = 2 + z[8]
        elif z[9] > 0:
            value = z[9]
        else:
            value = 4
        return value


    def go_timeout(self, chessboard):
        COLOR = self.color
        #print(chessboard)
        self.candidate_list.clear()
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        pos_idx = random.randint(0, len(idx) - 1)
        new_pos = idx[pos_idx]
        assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
        #print(new_pos)
        self.candidate_list.append(new_pos)

    def go(self, chessboard):
        candidate_value = np.array([[-2 for j in range(self.chessboard_size)] for i in range(self.chessboard_size)])
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        COLOR = self.color
        #print(chessboard)
        self.candidate_list.clear()
        for pos in idx:
            value = self.calcute_value(chessboard, pos[0], pos[1], COLOR)
            if value > candidate_value[pos[0], pos[1]]:
                candidate_value[pos[0], pos[1]] = value
        COLOR = -self.color
        for pos in idx:
            value = self.calcute_value(chessboard, pos[0], pos[1], COLOR)
            if value > 0:
                value = value - 1
                if value > candidate_value[pos[0], pos[1]]:
                    candidate_value[pos[0], pos[1]] = value
        pos_list = []
        temp_max = -1
        for pos in idx:
                if candidate_value[pos[0], pos[1]] > temp_max:
                    pos_list.clear()
                    pos_list.append(pos)
                    temp_max = candidate_value[pos[0], pos[1]]
                elif candidate_value[pos[0], pos[1]] == temp_max:
                    pos_list.append(pos)
        #print(candidate_value)
        pos_index = random.randint(0, len(pos_list) - 1)
        new_pos = pos_list[pos_index]
        #print(len(pos_list))
        assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
        self.candidate_list.append(new_pos)
