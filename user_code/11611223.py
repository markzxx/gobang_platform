#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import copy
import time

COLOR_BLACK = 2
COLOR_WHITE = 1
COLOR_NONE = 0


class WHITE(object):
    def __init__(self):
        self.WIN = {"11111"}
        self.HUO4 = {"011110"}
        self.CHONG4 = {"011112", "211110", "10111", "11011", "11101"}
        self.HUO3 = {"001110", "011100", "010110", "011010"}
        self.MIAN3 = {"001112", "010112", "011012", "201110", "011102", "211100", "211010", "210110", "10011", "10101",
                      "11001"}
        self.HUO2 = {"001100", "010100", "001010", "010010"}
        self.MIAN2 = {"211000", "210100", "210010", "10001", "000112", "001012", "010012", "01100", "00110"}


class BLACK(object):
    def __init__(self):
        self.WIN = {"22222"}
        self.HUO4 = {"022220"}
        self.CHONG4 = {"022221", "122220", "20222", "22022", "22202"}
        self.HUO3 = {"002220", "022200", "020220", "022020"}
        self.MIAN3 = {"002221", "020221", "022021", "102220", "022201", "122200", "122020", "120220", "20022", "20202",
                      "22002"}
        self.HUO2 = {"002200", "020200", "002020", "020020"}
        self.MIAN2 = {"122000", "120200", "120020", "20002", "000221", "002021", "020021", "02200", "00220"}


class Lines72(object):
    def __init__(self, chessboard_size):
        # 横竖斜 二维index 元组坐标
        self.column_index, self.row_index, self.left_up_index, self.right_up_index = [], [], [], []
        # 横竖斜 一行的局面
        self.column, self.row, self.left_up, self.right_up = [], [], [], []
        # 我的 该行最好棋型
        self.my_column_best, self.my_row_best, self.my_left_up_best, self.my_right_up_best = [], [], [], []
        # 对手的 该行最好棋型
        self.o_column_best, self.o_row_best, self.o_left_up_best, self.o_right_up_best = [], [], [], []
        for i in range(chessboard_size):
            self.row.append([])
            self.column.append([])
            self.row_index.append([])
            self.column_index.append([])
            for j in range(chessboard_size):
                self.row[i].append('0')
                self.column[i].append('0')
                self.row_index[i].append((i, j))
                self.column_index[i].append((j, i))
            self.my_row_best.append(-1)
            self.my_column_best.append(-1)
            self.o_row_best.append(-1)
            self.o_column_best.append(-1)
        for i in range(2 * (chessboard_size - 5) + 1):
            self.left_up.append([])
            self.right_up.append([])
            self.left_up_index.append([])
            self.right_up_index.append([])
            for j in range((chessboard_size - abs(i - (chessboard_size - 5)))):
                # 从左上到右下 [0] 为 (10,0) 到 (14,4) , [20] 为 (0,10) 到 (4,14)
                self.left_up[i].append('0')
                # 从左下到右上 [0] 为 (4,0) 到 (0,4) , [20] 为 (14,10) 到 (10,14)
                self.right_up[i].append('0')
                if i <= (chessboard_size - 5):
                    x = (chessboard_size - 5) - i + j
                    y = j
                else:
                    x = j
                    y = -(chessboard_size - 5) + i + j
                self.left_up_index[i].append((x, y))
                if i <= (chessboard_size - 5):
                    x = 4 + i - j
                    y = j
                else:
                    x = 4 + (chessboard_size - 5) - j
                    y = -(chessboard_size - 5) + i + j
                self.right_up_index[i].append((x, y))
            self.my_left_up_best.append(-1)
            self.my_right_up_best.append(-1)
            self.o_left_up_best.append(-1)
            self.o_right_up_best.append(-1)


class AI(object):

    def __init__(self, chessboard_size, color, time_out):
        color = 2 if color == -1 else 1
        board = []
        for i in range(chessboard_size):
            board.append([])
            for j in range(chessboard_size):
                board[i].append(0)
        self.last_board = np.array(board)  # 上一步棋  棋面  待使用
        self.current_point_score = -1
        self.best_point = set()
        self.can_tuple = set()  # 所有可以落子的点
        self.already_tuple = set()  # 所有已经落子的点
        self.lines72 = Lines72(chessboard_size)

        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of candidate_list as your decision .
        self.candidate_list = []

    def get_o_point(self, chessboard, last_board):
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if chessboard[i, j] != last_board[i, j]:
                    return (i, j)

    def maintain_tuple(self, can_tuple, already_tuple, tuple):  # set必然会传引用
        already_tuple = already_tuple | {tuple}
        for i in range(-1, 2):
            for j in range(-1, 2):
                can_tuple = can_tuple | {(ww[0] + i, ww[1] + j) for ww in {tuple} if
                                         self.chessboard_size > ww[0] + i >= 0 and self.chessboard_size >
                                         ww[1] + j >= 0}
        can_tuple = can_tuple - already_tuple
        return can_tuple

    def maintain_lines72(self, lines72, tuple, color):
        lines72.row[tuple[0]][tuple[1]] = str(color)
        lines72.column[tuple[1]][tuple[0]] = str(color)
        if 4 <= tuple[0] + tuple[1] <= 2 * (self.chessboard_size - 5) + 4:
            x_r = tuple[0] + tuple[1] - 4
            y_r = tuple[1] if tuple[0] <= self.chessboard_size else 14 - tuple[0]
            lines72.right_up[x_r][y_r] = str(color)
            lines72.my_right_up_best[x_r] = self.check_line(''.join(lines72.right_up[x_r]), self.color)
            lines72.o_right_up_best[x_r] = self.check_line(''.join(lines72.right_up[x_r]), 1 if self.color == 2 else 2)
        if abs(tuple[0] - tuple[1]) <= (self.chessboard_size - 5):
            x_l = 10 - tuple[0] + tuple[1]
            y_l = tuple[0] if tuple[0] <= tuple[1] else tuple[1]
            lines72.left_up[x_l][y_l] = str(color)
            lines72.my_left_up_best[x_l] = self.check_line(''.join(lines72.left_up[x_l]), self.color)
            lines72.o_left_up_best[x_l] = self.check_line(''.join(lines72.left_up[x_l]), 1 if self.color == 2 else 2)
        lines72.my_row_best[tuple[0]] = self.check_line(''.join(lines72.row[tuple[0]]), self.color)
        lines72.my_column_best[tuple[1]] = self.check_line(''.join(lines72.column[tuple[1]]), self.color)
        lines72.o_row_best[tuple[0]] = self.check_line(''.join(lines72.row[tuple[0]]), 1 if self.color == 2 else 2)
        lines72.o_column_best[tuple[1]] = self.check_line(''.join(lines72.column[tuple[1]]),
                                                          1 if self.color == 2 else 2)

    def bool_win(self):
        if 8 <= max(self.lines72.my_row_best) or 8 <= max(self.lines72.my_column_best) or 8 <= max(
                self.lines72.my_right_up_best) or 8 <= max(self.lines72.my_left_up_best):
            return True
        return False

    def win(self):
        if 8 <= max(self.lines72.my_row_best):
            index = self.lines72.my_row_best.index(max(self.lines72.my_row_best))
            tuple = set(self.lines72.row_index[index]) & self.can_tuple
            for t in tuple:
                row_column_left_up_right_up = self.mod(self.last_board, t, 1 if self.color == 2 else 2)
                color = WHITE() if self.color == COLOR_WHITE else BLACK()
                for i in row_column_left_up_right_up:
                    for j in color.WIN:
                        if i.find(j) != -1:
                            return tuple
        if 8 <= max(self.lines72.my_column_best):
            index = self.lines72.my_column_best.index(max(self.lines72.my_column_best))
            tuple = set(self.lines72.column_index[index]) & self.can_tuple
            for t in tuple:
                row_column_left_up_right_up = self.mod(self.last_board, t, 1 if self.color == 2 else 2)
                color = WHITE() if self.color == COLOR_WHITE else BLACK()
                for i in row_column_left_up_right_up:
                    for j in color.WIN:
                        if i.find(j) != -1:
                            return tuple
        if 8 <= max(self.lines72.my_right_up_best):
            index = self.lines72.my_right_up_best.index(max(self.lines72.my_right_up_best))
            tuple = set(self.lines72.right_up_index[index]) & self.can_tuple
            for t in tuple:
                row_column_left_up_right_up = self.mod(self.last_board, t, 1 if self.color == 2 else 2)
                color = WHITE() if self.color == COLOR_WHITE else BLACK()
                for i in row_column_left_up_right_up:
                    for j in color.WIN:
                        if i.find(j) != -1:
                            return tuple
        if 8 <= max(self.lines72.my_left_up_best):
            index = self.lines72.my_left_up_best.index(max(self.lines72.my_left_up_best))
            tuple = set(self.lines72.left_up_index[index]) & self.can_tuple
            for t in tuple:
                row_column_left_up_right_up = self.mod(self.last_board, t, 1 if self.color == 2 else 2)
                color = WHITE() if self.color == COLOR_WHITE else BLACK()
                for i in row_column_left_up_right_up:
                    for j in color.WIN:
                        if i.find(j) != -1:
                            return tuple

    def bool_must_block(self):
        if 8 <= max(self.lines72.o_row_best) or 8 <= max(self.lines72.o_column_best) or 8 <= max(
                self.lines72.o_right_up_best) or 8 <= max(self.lines72.o_left_up_best):
            return True
        return False

    def must_block(self):
        if 8 <= max(self.lines72.o_row_best):
            index = self.lines72.o_row_best.index(max(self.lines72.o_row_best))
            tuple = set(self.lines72.row_index[index]) & self.can_tuple
            for t in tuple:
                row_column_left_up_right_up = self.mod(self.last_board, t, 1 if self.color == 2 else 2)
                color = BLACK() if self.color == COLOR_WHITE else WHITE()
                for i in row_column_left_up_right_up:
                    for j in color.WIN:
                        if i.find(j) != -1:
                            return tuple
        if 8 <= max(self.lines72.o_column_best):
            index = self.lines72.o_column_best.index(max(self.lines72.o_column_best))
            tuple = set(self.lines72.column_index[index]) & self.can_tuple
            for t in tuple:
                row_column_left_up_right_up = self.mod(self.last_board, t, 1 if self.color == 2 else 2)
                color = BLACK() if self.color == COLOR_WHITE else WHITE()
                for i in row_column_left_up_right_up:
                    for j in color.WIN:
                        if i.find(j) != -1:
                            return tuple
        if 8 <= max(self.lines72.o_right_up_best):
            index = self.lines72.o_right_up_best.index(max(self.lines72.o_right_up_best))
            tuple = set(self.lines72.right_up_index[index]) & self.can_tuple
            for t in tuple:
                row_column_left_up_right_up = self.mod(self.last_board, t, 1 if self.color == 2 else 2)
                color = BLACK() if self.color == COLOR_WHITE else WHITE()
                for i in row_column_left_up_right_up:
                    for j in color.WIN:
                        if i.find(j) != -1:
                            return tuple
        if 8 <= max(self.lines72.o_left_up_best):
            index = self.lines72.o_left_up_best.index(max(self.lines72.o_left_up_best))
            tuple = set(self.lines72.left_up_index[index]) & self.can_tuple
            for t in tuple:
                row_column_left_up_right_up = self.mod(self.last_board, t, 1 if self.color == 2 else 2)
                color = BLACK() if self.color == COLOR_WHITE else WHITE()
                for i in row_column_left_up_right_up:
                    for j in color.WIN:
                        if i.find(j) != -1:
                            return tuple

    def bool_will_win_HUO3_to_HUO4(self):
        if 7 == max(self.lines72.my_row_best) or 7 == max(self.lines72.my_column_best) or 7 == max(
                self.lines72.my_right_up_best) or 7 == max(self.lines72.my_left_up_best):
            return True
        return False

    def will_win_HUO3_to_HUO4(self):
        if 7 == max(self.lines72.my_row_best):
            index = self.lines72.my_row_best.index(max(self.lines72.my_row_best))
            tuple = set(self.lines72.row_index[index]) & self.can_tuple
            for t in tuple:
                row_column_left_up_right_up = self.mod(self.last_board, t, self.color)
                color = WHITE() if self.color == COLOR_WHITE else BLACK()
                for i in row_column_left_up_right_up:
                    for j in color.HUO4:
                        if i.find(j) != -1:
                            return tuple
        if 7 == max(self.lines72.my_column_best):
            index = self.lines72.my_column_best.index(max(self.lines72.my_column_best))
            tuple = set(self.lines72.column_index[index]) & self.can_tuple
            for t in tuple:
                row_column_left_up_right_up = self.mod(self.last_board, t, self.color)
                color = WHITE() if self.color == COLOR_WHITE else BLACK()
                for i in row_column_left_up_right_up:
                    for j in color.HUO4:
                        if i.find(j) != -1:
                            return tuple
        if 7 == max(self.lines72.my_right_up_best):
            index = self.lines72.my_right_up_best.index(max(self.lines72.my_right_up_best))
            tuple = set(self.lines72.right_up_index[index]) & self.can_tuple
            for t in tuple:
                row_column_left_up_right_up = self.mod(self.last_board, t, self.color)
                color = WHITE() if self.color == COLOR_WHITE else BLACK()
                for i in row_column_left_up_right_up:
                    for j in color.HUO4:
                        if i.find(j) != -1:
                            return tuple
        if 7 == max(self.lines72.my_left_up_best):
            index = self.lines72.my_left_up_best.index(max(self.lines72.my_left_up_best))
            tuple = set(self.lines72.left_up_index[index]) & self.can_tuple
            for t in tuple:
                row_column_left_up_right_up = self.mod(self.last_board, t, self.color)
                color = WHITE() if self.color == COLOR_WHITE else BLACK()
                for i in row_column_left_up_right_up:
                    for j in color.HUO4:
                        if i.find(j) != -1:
                            return tuple

    def bool_must_block_HUO3_to_HUO4(self):
        if 7 == max(self.lines72.o_row_best) or 7 == max(self.lines72.o_column_best) or 7 == max(
                self.lines72.o_right_up_best) or 7 == max(self.lines72.o_left_up_best):
            return True
        return False

    def must_block_HUO3_to_HUO4(self):
        find_best_tuple = []
        time = -1
        for k in [self.lines72.o_row_best, self.lines72.o_column_best, self.lines72.o_right_up_best,
                  self.lines72.o_left_up_best]:
            time += 1
            if 7 == max(k):
                temp_index = [self.lines72.row_index, self.lines72.column_index, self.lines72.right_up_index,
                              self.lines72.left_up_index]
                index = k.index(max(k))
                tuple = set(temp_index[time][index]) & self.can_tuple
                for t in tuple:
                    temp_point_score = []
                    temp_point_score.append(t)
                    row_column_left_up_right_up = self.mod(self.last_board, t, 1 if self.color == 2 else 2)
                    color = BLACK() if self.color == COLOR_WHITE else WHITE()
                    for i in row_column_left_up_right_up:
                        for j in color.HUO4:
                            if i.find(j) != -1:
                                for i_2 in row_column_left_up_right_up:
                                    for j_2 in color.CHONG4:
                                        if i_2.find(j_2) != -1:
                                            temp_point_score.append(10)
                                            return t
                                for i_2 in row_column_left_up_right_up:
                                    for j_2 in color.HUO3:
                                        if i_2.find(j_2) != -1:
                                            temp_point_score.append(10)
                                            return t
                                for i_2 in row_column_left_up_right_up:
                                    for j_2 in color.HUO2:
                                        if i_2.find(j_2) != -1:
                                            temp_point_score.append(6)
                                for i_2 in row_column_left_up_right_up:
                                    for j_2 in color.MIAN3:
                                        if i_2.find(j_2) != -1:
                                            temp_point_score.append(5)
                                for i_2 in row_column_left_up_right_up:
                                    for j_2 in color.HUO2:
                                        if i_2.find(j_2) != -1:
                                            temp_point_score.append(4)
                                for i_2 in row_column_left_up_right_up:
                                    for j_2 in color.MIAN2:
                                        if i_2.find(j_2) != -1:
                                            temp_point_score.append(3)
                                row_column_left_up_right_up = self.mod(self.last_board, t, self.color)
                                color = WHITE() if self.color == COLOR_WHITE else BLACK()
                                for i_2 in row_column_left_up_right_up:
                                    for j_2 in color.CHONG4:
                                        if i_2.find(j_2) != -1:
                                            temp_point_score.append(8.1)
                                for i_2 in row_column_left_up_right_up:
                                    for j_2 in color.HUO3:
                                        if i_2.find(j_2) != -1:
                                            temp_point_score.append(7.1)
                                for i_2 in row_column_left_up_right_up:
                                    for j_2 in color.HUO2:
                                        if i_2.find(j_2) != -1:
                                            temp_point_score.append(6.1)
                                for i_2 in row_column_left_up_right_up:
                                    for j_2 in color.MIAN3:
                                        if i_2.find(j_2) != -1:
                                            temp_point_score.append(5.1)
                                for i_2 in row_column_left_up_right_up:
                                    for j_2 in color.HUO2:
                                        if i_2.find(j_2) != -1:
                                            temp_point_score.append(4.1)
                                for i_2 in row_column_left_up_right_up:
                                    for j_2 in color.MIAN2:
                                        if i_2.find(j_2) != -1:
                                            temp_point_score.append(3.1)
                                find_best_tuple.append(temp_point_score)
                a_tuple = [find_best_tuple[i].pop(0) for i in range(len(find_best_tuple))]
                while len(a_tuple) > 1:
                    who_max = []
                    i = -1
                    for whatever in range(len(a_tuple)):
                        i += 1
                        if len(find_best_tuple[i]) == 0 and len(find_best_tuple) > 1:
                            find_best_tuple.pop(i)
                            a_tuple.pop(i)
                            i -= 1
                            continue
                        if len(find_best_tuple) == 1:
                            return a_tuple[0]
                        t3 = max(find_best_tuple[i])
                        t2 = find_best_tuple[i].index(t3)
                        t1 = find_best_tuple[i].pop(t2)
                        who_max.append(t1)
                    k = -1
                    m = range(len(who_max))
                    for mm in m:
                        k += 1
                        if who_max[k] != max(who_max):
                            find_best_tuple.pop(k)
                            a_tuple.pop(k)
                            who_max.pop(k)
                            k -= 1
                return a_tuple[0]

    def will_win_double_HUO3(self):
        i = -1
        for j in [self.lines72.my_row_best, self.lines72.my_column_best,
                  self.lines72.my_right_up_best, self.lines72.my_left_up_best]:
            i += 1
            if 5 <= max(j) <= 6:  # 死三 活二
                index = j.index(max(j))
                tuple = set([self.lines72.row_index[index], self.lines72.column_index[index],
                             self.lines72.right_up_index[index], self.lines72.left_up_index[index]][
                                i]) & self.can_tuple
                for t in tuple:
                    row_column_left_up_right_up = self.mod(self.last_board, t, self.color)
                    color = WHITE() if self.color == COLOR_WHITE else BLACK()
                    HUO3_time = 0
                    CHONG4_time = 0
                    for k in row_column_left_up_right_up:
                        for q in color.HUO3:
                            if k.find(q) != -1:
                                HUO3_time += 1
                                break
                        for q in color.CHONG4:
                            if k.find(q) != -1:
                                CHONG4_time += 1
                                break
                    if HUO3_time >= 2 or (HUO3_time >= 1 and CHONG4_time >= 1) or CHONG4_time >= 2:
                        return t

    def must_block_double_HUO3(self):
        i = -1
        for j in [self.lines72.o_row_best, self.lines72.o_column_best,
                  self.lines72.o_right_up_best, self.lines72.o_left_up_best]:
            i += 1
            if 5 <= max(j) <= 6:  # 死三 活二
                index = j.index(max(j))
                tuple = set([self.lines72.row_index[index], self.lines72.column_index[index],
                             self.lines72.right_up_index[index], self.lines72.left_up_index[index]][
                                i]) & self.can_tuple
                for t in tuple:
                    row_column_left_up_right_up = self.mod(self.last_board, t, 1 if self.color == 2 else 2)
                    color = BLACK() if self.color == COLOR_WHITE else WHITE()
                    HUO3_time = 0
                    CHONG4_time = 0
                    for k in row_column_left_up_right_up:
                        def temp_func():
                            nonlocal HUO3_time, CHONG4_time, k  # 加不加 k 貌似没区别
                            for q in color.HUO3:
                                if k.find(q) != -1:
                                    HUO3_time += 1
                                    return
                            for q in color.CHONG4:
                                if k.find(q) != -1:
                                    CHONG4_time += 1
                                    return

                        temp_func()
                    if HUO3_time >= 2 or (HUO3_time >= 1 and CHONG4_time >= 1) or CHONG4_time >= 2:
                        return t

    def check_line(self, line, color):
        color = WHITE() if color == COLOR_WHITE else BLACK()
        for j in color.WIN:  # 成五
            if line.find(j) != -1:
                return 10
        for j in color.HUO4:  # 活四
            if line.find(j) != -1:
                return 9
        for j in color.CHONG4:  # 死四
            if line.find(j) != -1:
                return 8
        for j in color.HUO3:  # 活三
            if line.find(j) != -1:
                return 7
        for j in color.HUO2:  # 活二
            if line.find(j) != -1:
                return 6
        for j in color.MIAN3:  # 死三
            if line.find(j) != -1:
                return 5
        for j in color.MIAN2:  # 死二
            if line.find(j) != -1:
                return 4
        return -1

    def data_clean(self, chessboard, num):  # 传引用 会改变self.can_tuple 和 self.already_tuple
        self.can_tuple = set()
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if chessboard[i, j] != 0:
                    self.already_tuple.add((i, j))
                    if chessboard[i, j] == -1:
                        chessboard[i, j] = 2
        for i in range(-num, num + 1):
            for j in range(-num, num + 1):
                self.can_tuple = self.can_tuple | {(ww[0] + i, ww[1] + j) for ww in self.already_tuple if
                                                   self.chessboard_size > ww[0] + i >= 0 and self.chessboard_size >
                                                   ww[1] + j >= 0}
        self.can_tuple = self.can_tuple - self.already_tuple
        # print(self.already_tuple)
        # print(self.can_tuple)
        return self.can_tuple

    def mod(self, chessboard, tuple, color):  # 创建米字九格
        chessboard[tuple] = color  # 若 tuple此位置 落color子
        row, column, left_up, right_up = "", "", "", ""
        for i in range(-4, 5):
            if 0 <= tuple[1] + i < self.chessboard_size:
                row = row + str(chessboard[tuple[0], tuple[1] + i])
                if 0 <= tuple[0] - i < self.chessboard_size:
                    right_up = right_up + str(chessboard[tuple[0] - i, tuple[1] + i])
            if 0 <= tuple[0] + i < self.chessboard_size:
                column = column + str(chessboard[tuple[0] + i, tuple[1]])
                if 0 <= tuple[1] + i < self.chessboard_size:
                    left_up = left_up + str(chessboard[tuple[0] + i, tuple[1] + i])
        chessboard[tuple] = 0  # 收color子
        return [row, column, left_up, right_up]
        # print(tuple, "row, column, left_up, right_up =", row, column, left_up, right_up)

    def evaluate(self, tuple, color, row_column_left_up_right_up):

        color = WHITE() if color == COLOR_WHITE else BLACK()

        # # 成五
        # for i in row_column_left_up_right_up:
        #     for j in color.WIN:
        #         if i.find(j) != -1:
        #             if self.current_point_score == 10:
        #                 self.best_point.add(tuple)
        #             else:
        #                 self.best_point.clear()
        #                 self.best_point.add(tuple)
        #                 self.current_point_score = 10
        #             return
        #
        # # 活四 / 双死4 / 死4活3
        # for i in row_column_left_up_right_up:
        #     for j in color.HUO4:
        #         if i.find(j) != -1:
        #             if self.current_point_score == 9:
        #                 self.best_point.add(tuple)
        #             elif self.current_point_score < 9:
        #                 self.best_point.clear()
        #                 self.best_point.add(tuple)
        #                 self.current_point_score = 9
        # CHONG4_time = 0
        # for i in row_column_left_up_right_up:
        #     for j in color.CHONG4:
        #         if i.find(j) != -1:
        #             if CHONG4_time >= 1:
        #                 if self.current_point_score == 9:
        #                     self.best_point.add(tuple)
        #                 elif self.current_point_score < 9:
        #                     self.best_point.clear()
        #                     self.best_point.add(tuple)
        #                     self.current_point_score = 9
        #             CHONG4_time += 1
        #             break
        #     for j in color.HUO3:
        #         if i.find(j) != -1:
        #             if CHONG4_time >= 1:
        #                 if self.current_point_score == 9:
        #                     self.best_point.add(tuple)
        #                 elif self.current_point_score < 9:
        #                     self.best_point.clear()
        #                     self.best_point.add(tuple)
        #                     self.current_point_score = 9
        #
        # # 双活三
        # HUO3_time = 0
        # for i in row_column_left_up_right_up:
        #     for j in color.HUO3:
        #         if i.find(j) != -1:
        #             if HUO3_time >= 1:
        #                 if self.current_point_score == 8:
        #                     self.best_point.add(tuple)
        #                 elif self.current_point_score < 8:
        #                     self.best_point.clear()
        #                     self.best_point.add(tuple)
        #                     self.current_point_score = 8
        #             HUO3_time += 1
        #             break

        # 死三活三

        HUO3_time = 0
        MIAN3_time = 0
        for i in row_column_left_up_right_up:
            for j in color.HUO3:
                if i.find(j) != -1:
                    if MIAN3_time >= 1:
                        if self.current_point_score == 7:
                            self.best_point.add(tuple)
                        elif self.current_point_score < 7:
                            self.best_point.clear()
                            self.best_point.add(tuple)
                            self.current_point_score = 7
                    HUO3_time += 1
                    break
            for j in color.MIAN3:
                if i.find(j) != -1:
                    if HUO3_time >= 1:
                        if self.current_point_score == 7:
                            self.best_point.add(tuple)
                        elif self.current_point_score < 7:
                            self.best_point.clear()
                            self.best_point.add(tuple)
                            self.current_point_score = 7
                    MIAN3_time += 1
                    break

        # 死四
        for i in row_column_left_up_right_up:
            for j in color.CHONG4:
                if i.find(j) != -1:
                    if self.current_point_score == 6:
                        self.best_point.add(tuple)
                    elif self.current_point_score < 6:
                        self.best_point.clear()
                        self.best_point.add(tuple)
                        self.current_point_score = 6

        # 活三
        for i in row_column_left_up_right_up:
            for j in color.HUO3:
                if i.find(j) != -1:
                    if self.current_point_score == 5:
                        self.best_point.add(tuple)
                    elif self.current_point_score < 5:
                        self.best_point.clear()
                        self.best_point.add(tuple)
                        self.current_point_score = 5

        # 双活二
        HUO2_time = 0
        for i in row_column_left_up_right_up:
            for j in color.HUO2:
                if i.find(j) != -1:
                    if HUO2_time >= 1:
                        if self.current_point_score == 4:
                            self.best_point.add(tuple)
                        elif self.current_point_score < 4:
                            self.best_point.clear()
                            self.best_point.add(tuple)
                            self.current_point_score = 4
                    HUO2_time += 1
                    break

        # 活二
        for i in row_column_left_up_right_up:
            for j in color.HUO2:
                if i.find(j) != -1:
                    if self.current_point_score == 3:
                        self.best_point.add(tuple)
                    elif self.current_point_score < 3:
                        self.best_point.clear()
                        self.best_point.add(tuple)
                        self.current_point_score = 3

        # 死三
        for i in row_column_left_up_right_up:
            for j in color.MIAN3:
                if i.find(j) != -1:
                    if self.current_point_score == 2:
                        self.best_point.add(tuple)
                    elif self.current_point_score < 2:
                        self.best_point.clear()
                        self.best_point.add(tuple)
                        self.current_point_score = 2

        # 死二
        for i in row_column_left_up_right_up:
            for j in color.MIAN2:
                if i.find(j) != -1:
                    if self.current_point_score == 2:
                        self.best_point.add(tuple)
                    elif self.current_point_score < 2:
                        self.best_point.clear()
                        self.best_point.add(tuple)
                        self.current_point_score = 2

    def process(self, chessboard):
        new_tuple = self.get_o_point(chessboard, self.last_board)
        if new_tuple is None:
            x = y = int((self.chessboard_size - 1) / 2)
            new_pos = (x, y)
            return new_pos
        else:
            self.last_board[new_tuple] = 1 if self.color == 2 else 2  # 更新last_board
            self.already_tuple.add(new_tuple)
            self.can_tuple = self.maintain_tuple(self.can_tuple, self.already_tuple, new_tuple)
            self.maintain_lines72(self.lines72, new_tuple, 1 if self.color == 2 else 2)

        if self.bool_win():
            new_pos = self.win()
            return new_pos

        if self.bool_must_block():
            new_pos = self.must_block()
            return new_pos

        if self.bool_will_win_HUO3_to_HUO4():
            new_pos = self.will_win_HUO3_to_HUO4()
            return new_pos

        if self.bool_must_block_HUO3_to_HUO4():
            new_pos = self.must_block_HUO3_to_HUO4()
            return new_pos

        t = self.will_win_double_HUO3()
        if t is not None:
            new_pos = t
            return new_pos

        t = self.must_block_double_HUO3()
        if t is not None:
            new_pos = t
            return new_pos

    def go(self, chessboard):
        self.candidate_list.clear()
        # ==================================================================
        new_pos = self.process(chessboard)
        if new_pos is None:
            set_tuple = self.data_clean(chessboard, 1)
            self.current_point_score = -1
            self.best_point.clear()
            for i in set_tuple:
                row_column_left_up_right_up = self.mod(chessboard, i, self.color)
                self.evaluate(i, self.color, row_column_left_up_right_up)
            my_score = self.current_point_score
            my_best_point = copy.deepcopy(self.best_point)
            o_color = 1 if self.color == 2 else 2
            self.current_point_score = -1
            self.best_point.clear()
            for i in set_tuple:
                row_column_left_up_right_up = self.mod(chessboard, i, o_color)
                self.evaluate(i, o_color, row_column_left_up_right_up)
            o_score = self.current_point_score
            o_best_point = copy.deepcopy(self.best_point)
            if len(set_tuple) == 0:
                x = y = int((self.chessboard_size - 1) / 2)
                new_pos = (x, y)
            elif my_score >= o_score:
                if my_score == -1:
                    for i in set_tuple:
                        my_new_pos = i
                        break
                else:
                    for i in my_best_point:
                        my_new_pos = i
                        break
                new_pos = my_new_pos
            elif my_score < o_score:
                for i in o_best_point:
                    o_new_pos = i
                    break
                new_pos = o_new_pos

        self.last_board[new_pos] = self.color
        self.already_tuple.add(new_pos)
        self.can_tuple = self.maintain_tuple(self.can_tuple, self.already_tuple, new_pos)
        self.maintain_lines72(self.lines72, new_pos, self.color)
        # ==============Find new pos========================================
        # print("new_pos[0], new_pos[1] = ", new_pos[0], new_pos[1])
        # print("chessboard[new_pos[0], new_pos[1]] = ", chessboard[new_pos[0], new_pos[1]])
        assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
        self.candidate_list.append(new_pos)


# start = time.time()
# run_time = (time.time() - start)

if __name__ == '__main__':
    color = 1
    ai = AI(15, color, 1)
    chessboard = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           ])
    # a = ai.get_o_point(chessboard, ai.last_board)
    # ai.last_board[a] = 1
    # ai.already_tuple.add(a)
    # ai.can_tuple = ai.maintain_tuple(ai.can_tuple, ai.already_tuple, a)
    # ai.maintain_lines72(ai.lines72, a, 1)
    # a = ai.get_o_point(chessboard, ai.last_board)
    # ai.last_board[a] = 1
    # ai.already_tuple.add(a)
    # ai.can_tuple = ai.maintain_tuple(ai.can_tuple, ai.already_tuple, a)
    # ai.maintain_lines72(ai.lines72, a, 1)
    # a = ai.get_o_point(chessboard, ai.last_board)
    # ai.last_board[a] = 1
    # ai.already_tuple.add(a)
    # ai.can_tuple = ai.maintain_tuple(ai.can_tuple, ai.already_tuple, a)
    # ai.maintain_lines72(ai.lines72, a, 1)
    for i in range(3):
        a = ai.get_o_point(chessboard, ai.last_board)
        ai.last_board[a] = 2
        ai.already_tuple.add(a)
        ai.can_tuple = ai.maintain_tuple(ai.can_tuple, ai.already_tuple, a)
        ai.maintain_lines72(ai.lines72, a, 2)
    # a = ai.get_o_point(chessboard, ai.last_board)
    # ai.last_board[a] = 1
    # ai.already_tuple.add(a)
    # ai.can_tuple = ai.maintain_tuple(ai.can_tuple, ai.already_tuple, a)
    # ai.maintain_lines72(ai.lines72, a, 1)

    print(ai.must_block_HUO3_to_HUO4())

    a = ai.data_clean(chessboard, 1)
    print("ai.data_clean = ", a)

    ai.maintain_tuple(ai.can_tuple, ai.already_tuple, (8, 8))
    for i in ai.already_tuple:
        ai.maintain_lines72(ai.lines72, i, color)

    while (1):
        start = time.time()
        ai.go(chessboard)
        run_time = (time.time() - start)
        print("run_time == ", run_time)
        print(ai.candidate_list[0])
        chessboard[ai.candidate_list[0]] = color
        print(chessboard)

        x = input(" x = ")
        y = input(" y = ")
        print("x, y = ", x, y)
        chessboard[(int(x), int(y))] = 2
        print(chessboard)

    # while (1):
    #     start = time.time()
    #     ai.go(chessboard)
    #     run_time = (time.time() - start)
    #     print("run_time == ", run_time)
    #     print(ai.candidate_list[0])
    #     chessboard[ai.candidate_list[0]] = color
    #     print(chessboard)
    #
    #     oai.go(chessboard)
    #     print(oai.candidate_list[0])
    #     chessboard[oai.candidate_list[0]] = 2
    #     print(chessboard)
