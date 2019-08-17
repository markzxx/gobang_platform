import numpy as np


class Robot(object):

    def __init__(self, _board, size, wait_list):
        self.board = _board
        self.size = size
        self.wait_list = wait_list

    def value_points(self, player, enemy, board):
        points = []
        aa = [0, 0, 0]
        cnt = 0
        for x in range(self.size):
            for y in range(self.size):
                hen_list = []  # 横排
                shu_list = []  # 竖排
                zuoxie_list = []  # 左下-右上斜对角线
                youxie_list = []  # 左上-右下斜对角线
                current_value = -1
                if self.board[x][y] == 0:
                    cnt += 1
                    if cnt == 1:
                        aa = [x, y, 0]
                    for m in range(x - 4, x + 5):
                        if 0 <= m < 15:
                            hen_list.append(board[m, y])
                        else:
                            hen_list.append(2)

                    for m in range(y - 4, y + 5):
                        if 0 <= m < 15:
                            shu_list.append(board[x, m])
                        else:
                            shu_list.append(2)

                    for m, n in zip(range(x - 4, x + 5), range(y - 4, y + 5)):
                        if 0 <= m < 15 and 0 <= n < 15:
                            zuoxie_list.append(board[m, n])
                        else:
                            zuoxie_list.append(2)

                    for m, n in zip(range(x - 4, x + 5), range(y + 4, y - 5, -1)):
                        if 0 <= m < 15 and 0 <= n < 15:
                            youxie_list.append(board[m, n])
                        else:
                            youxie_list.append(2)
                    me_value = self.calculate_value(player, enemy, hen_list, shu_list, zuoxie_list, youxie_list)
                    fan_value = self.calculate_value(enemy, player, hen_list, shu_list, zuoxie_list, youxie_list)
                    value = me_value + fan_value * 0.9
                    if value > 0:
                        points.append([x, y, value])
                    if value > current_value:
                        points.append([x, y, value])
                        self.wait_list.append([x, y])
                        current_value = value
        # print(points)
        return points

    def max_value_point(self, player, enemy):
        points = self.value_points(player, enemy, self.board)
        flag = -1
        max_point = []
        for p in points:
            if p[2] > flag:
                max_point = p
                flag = p[2]
        return [max_point[0], max_point[1]]

    def calculate_value(self, player, enemy, hen_list, shu_list, zuoxie_list, youxie_list):
        flag = 0
        flag += self.lian_wu(player, hen_list) + self.lian_wu(player, shu_list) + self.lian_wu(player,
                                                                                               zuoxie_list) + self.lian_wu(
            player, youxie_list)
        flag += self.huo_si(player, hen_list) + self.huo_si(player, shu_list) + self.huo_si(player,
                                                                                            zuoxie_list) + self.huo_si(
            player, youxie_list)
        flag += self.mian_si(player, enemy, hen_list) + self.mian_si(player, enemy, shu_list) + self.mian_si(player,
                                                                                                             enemy,
                                                                                                             zuoxie_list) + self.mian_si(
            player, enemy, youxie_list)
        flag += self.huo_san(player, hen_list) + self.huo_san(player, shu_list) + self.huo_san(player,
                                                                                               zuoxie_list) + self.huo_san(
            player, youxie_list)
        flag += self.mian_san(player, enemy, hen_list) + self.mian_san(player, enemy, shu_list) + self.mian_san(player,
                                                                                                                enemy,
                                                                                                                zuoxie_list) + self.mian_san(
            player, enemy, youxie_list)
        flag += self.huo_er(player, enemy, hen_list) + self.huo_er(player, enemy, shu_list) + self.huo_er(player, enemy,
                                                                                                          zuoxie_list) + self.huo_er(
            player, enemy, youxie_list)
        flag += self.mian_er(player, enemy, hen_list) + self.mian_er(player, enemy, shu_list) + self.mian_er(player,
                                                                                                             enemy,
                                                                                                             zuoxie_list) + self.mian_er(
            player, enemy, youxie_list)
        return flag

    @staticmethod
    def lian_wu(player, checklist):
        checklist[4] = player
        pattern = [player, player, player, player, player]
        flag = False
        for i in range(5):
            if checklist[i:i + 5] == pattern:
                flag = True
        checklist[4] = 0
        if flag:
            return 15000
        else:
            return 0

    @staticmethod
    def huo_si(player, checklist):
        checklist[4] = player
        huo_si_pattern = [0, player, player, player, player, 0]
        flag = False
        for i in range(4):
            if checklist[i:i + 6] == huo_si_pattern:
                flag = True
        checklist[4] = 0
        if flag:
            return 10000
        else:
            return 0

    @staticmethod
    def mian_si(player, enemy, checklist):
        checklist[4] = player
        pattern1 = [[0, player, player, player, player, enemy],
                    [enemy, player, player, player, player, 0]]
        pattern2 = [[player, player, 0, player, player],
                    [player, 0, player, player, player],
                    [player, player, player, 0, player]]
        flag1 = False
        for i in range(4):
            if checklist[i:i + 6] in pattern1:
                flag1 = True
        flag2 = False
        for i in range(5):
            if checklist[i:i + 5] in pattern2:
                flag2 = True
        checklist[4] = 0
        if flag1:
            return 5000
        elif flag2:
            return 2900
        else:
            return 0

    @staticmethod
    def huo_san(player, checklist):
        checklist[4] = player
        pattern1 = [[0, 0, player, player, player, 0], [0, player, player, player, 0, 0]]
        pattern2 = [[0, player, player, 0, player, 0], [0, player, 0, player, player, 0]]
        flag1 = False
        flag2 = False
        for i in range(4):
            if checklist[i:i + 6] in pattern1:
                flag1 = True
            if checklist[i:i + 6] in pattern2:
                flag2 = True
        checklist[4] = 0
        if flag1:
            return 3400
        elif flag2:
            return 3000
        else:
            return 0

    @staticmethod
    def mian_san(player, enemy, checklist):
        checklist[4] = player
        flag1 = False
        flag2 = False
        pattern1 = [[enemy, player, player, player, 0, 0], [0, 0, player, player, player, enemy]]

        pattern2 = [[enemy, 0, player, player, player, 0, enemy],
                    [enemy, player, 0, player, player, 0, enemy],
                    [enemy, player, player, 0, player, 0, enemy]]

        pattern3 = [[player, player, 0, 0, player, enemy],
                    [enemy, player, player, 0, 0, player],
                    [player, 0, 0, player, player, enemy],
                    [enemy, player, 0, 0, player, player],
                    [0, player, player, 0, player, enemy],
                    [0, player, 0, player, player, enemy],
                    [player, 0, player, 0, player, enemy],
                    [enemy, player, 0, player, 0, player]
                    ]

        for i in range(4):
            if checklist[i:i + 6] in pattern1:
                flag1 = True
            if checklist[i:i + 6] in pattern3:
                flag2 = True

        for i in range(3):
            if checklist[i:i + 7] in pattern2:
                flag2 = True

        checklist[4] = 0
        if flag1:
            return 1350
        elif flag2:
            return 1300
        else:
            return 0

    @staticmethod
    def huo_er(player, enemy, checklist):
        checklist[4] = player
        pattern1 = [0, 0, player, player, 0, 0]
        pattern2 = [[0, 0, 0, player, player, 0, enemy], [enemy, 0, player, player, 0, 0, 0]]
        flag = False
        for i in range(4):
            if checklist[i:i + 6] == pattern1:
                flag = True

        for i in range(3):
            if checklist[i:i + 7] in pattern2:
                flag = True
        checklist[4] = 0

        if flag:
            return 399
        else:
            return 0

    @staticmethod
    def mian_er(player, enemy, checklist):
        checklist[4] = player
        pattern1 = [[enemy, player, player, 0, 0, 0],
                    [0, 0, 0, player, player, enemy],
                    [0, player, 0, 0, player, enemy],
                    [0, 0, player, 0, player, enemy],
                    [enemy, player, 0, player, 0, 0],
                    [enemy, player, 0, 0, player, 0]]
        pattern2 = [[enemy, 0, 0, player, player, 0, enemy],
                    [enemy, 0, player, player, 0, 0, enemy],
                    [enemy, 0, player, 0, player, 0, enemy]]
        flag = False
        for i in range(4):
            if checklist[i:i + 6] in pattern1:
                flag = True

        for i in range(3):
            if checklist[i:i + 7] in pattern2:
                flag = True
        checklist[4] = 0

        if flag:
            return 95
        else:
            return 0


COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0


# don't change the class name
class AI(object):
    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your decision .
        self.candidate_list = []

    # # If your are the first, this function will be used.
    # def first_chess(self, chessboard):
    #     assert self.color == COLOR_BLACK
    #     self.candidate_list.clear()
    #     # ==================================================================
    #     # Here you can put your first piece
    #     # for example, you can put your piece on sun（天元）
    #     self.candidate_list.append((self.chessboard_size // 2, self.chessboard_size // 2))
    #     chessboard[self.candidate_list[-1][0], self.candidate_list[-1][0]] = self.color

    # The input is current chessboard.
    def go(self, chessboard):
        robot = Robot(chessboard, self.chessboard_size, self.candidate_list)
        # Clear candidate_list
        self.candidate_list.clear()
        new_pos = (0, 0)
        # ==================================================================
        # To write your algorithm here
        # Here is the simplest sample:Random decision
        if (chessboard == np.zeros((self.chessboard_size, self.chessboard_size))).all() and self.color == COLOR_BLACK:
            new_pos = [self.chessboard_size // 2, self.chessboard_size // 2]
            self.candidate_list.append(new_pos)
        else:
            new_pos = robot.max_value_point(self.color, - self.color)
        # ==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        # If not, return error.
        assert chessboard[new_pos[0], new_pos[1]] == 0
        chessboard[new_pos[0], new_pos[1]] = self.color
        # Add your decision into candidate_list, Records the chess board
        self.candidate_list.append(new_pos)

# broad = zeros((17, 17), dtype=int)
# chessboard = np.zeros((15, 15))
# ai1 = AI(15, -1, 1000)
# ai2 = AI(15, 1, 1000)
# a = 1
# # print(chessboard)
# while a > 0:
#     ai1.go(chessboard)
#     print(ai1.candidate_list[-1])
#     # ai2.go(chessboard)
#     a = a - 1
#     # print(chessboard)
#     print()
