import numpy as np
import random
import time

COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0
random.seed(0)
#don't change the class name
class AI(object):
    shape_evalue =[(50, (0, 1, 1, 0, 0)),
                   (50, (0, 0, 1, 1, 0)),
                   (200, (1, 1, 0, 1, 0)),
                   (200, (0, 1, 1, 0, 1)),
                   (500, (0, 0, 1, 1, 1)),
                   (500, (1, 1, 1, 0, 0)),
                   (500, (2, 1, 1, 1, 0)),
                   (500,( 0, 1, 1, 1, 2)),
                   (5000, (0, 1, 1, 1, 0)),
                   (5000, (0, 1, 0, 1, 1, 0)),
                   (5000, (0, 1, 1, 0, 1, 0)),
                   (5000, (1, 1, 1, 0, 1)),
                   (5000, (1, 1, 0, 1, 1)),
                   (5000, (1, 0, 1, 1, 1)),
                   (5000, (1, 1, 1, 1, 0)),
                   (5000, (0, 1, 1, 1, 1)),
                   (50000, (0, 1, 1, 1, 1, 0)),
                   (99999999, (1, 1, 1, 1, 1))]
    my_pos=[]
    enemy_pos=[]
    whole_pos=[]
    all_pos=[]
    decide_pos=[0,0]
    enemy_color=""
    #chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        #You are white or black
        self.color = color
        self.enemy_color = -self.color
        #the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your decision .
        self.candidate_list = []
        for i in range(0, self.chessboard_size):
            for j in range(0, self.chessboard_size):
                self.all_pos.append((i,j))


# If your are the first, this function will be used.
    def first_chess(self):
        assert self.color == COLOR_BLACK
        self.candidate_list.clear()
        self.candidate_list.append(((self.chessboard_size/2) - 1,(self.chessboard_size/2)-1))
        self.my_pos.append(((self.chessboard_size/2)-1,(self.chessboard_size/2)-1))
        self.whole_pos.append(((self.chessboard_size/2)-1,(self.chessboard_size/2)-1))

# The input is current chessboard.
    def go(self, chessboard):
# Clear candidate_list
        start = time.time()
        self.candidate_list.clear()
        if self.whole_pos :
            self.first_chess()
        else:
            new_enemy_list = []
            new_my_list = []
            chess_array1 = np.argwhere(chessboard == self.enemy_color).tolist()
            for i in range(0, len(chess_array1)):
                new_enemy_list.append((chess_array1[i][0], chess_array1[i][1]))

            chess_array2 = np.argwhere(chessboard == self.color).tolist()
            for i in range(0, len(chess_array2)):
                new_my_list.append((chess_array2[i][0], chess_array2[i][1]))

            for pos in new_my_list:
                if pos not in self.my_pos:
                    self.my_pos.append(pos)
                if pos not in self.whole_pos:
                    self.whole_pos.append(pos)
            for pos in new_enemy_list:
                if pos not in self.enemy_pos:
                    self.enemy_pos.append(pos)
                if pos not in self.whole_pos:
                    self.whole_pos.append(pos)
            self.ai()
            assert chessboard[self.decide_pos[0], self.decide_pos[1]] == 0
            self.candidate_list.append((self.decide_pos[0], self.decide_pos[1]))
        run_time = (time.time() - start)
        print(run_time)
#==================================================================
#To write your algorithm here
#Here is the simplest sample:Random decision

    def ai(self):
        self.max_min(True, 1, -99999999, 99999999)
        self.my_pos.append((self.decide_pos[0],self.decide_pos[1]))
        self.whole_pos.append((self.decide_pos[0],self.decide_pos[1]))

    def max_min(self, ai_round, depth, alpha, beta):
        if self.game_win(self.my_pos) or self.game_win(self.enemy_pos) or depth == 0:
            return self.evaluation(ai_round)
        blank_list = list(set(self.all_pos).difference(set(self.whole_pos)))
        print(blank_list)
        last_pt = self.whole_pos[-1]
        for item in blank_list:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    if (last_pt[0] + i, last_pt[1] + j) in blank_list:
                        blank_list.remove((last_pt[0] + i, last_pt[1] + j))
                        blank_list.insert(0, (last_pt[0] + i, last_pt[1] + j))

        for next_step in blank_list:

            if not self.has_neighbour(next_step):
                continue

            if ai_round:
                self.my_pos.append(next_step)
            else:
                self.enemy_pos.append(next_step)
            self.whole_pos.append(next_step)

            value = -self.max_min(not ai_round, depth - 1, -beta, -alpha)
            print("choice: ",next_step," Value: ",value," Depth: ",depth," Alaph: ",alpha," Beta: ",beta)

            if ai_round:
                self.my_pos.remove(next_step)
            else:
                self.enemy_pos.remove(next_step)
            self.whole_pos.remove(next_step)

            if value > alpha:
                if depth == 1:
                    self.decide_pos[0] = next_step[0]
                    self.decide_pos[1] = next_step[1]
                # alpha + beta剪枝点
                if value >= beta:
                    return beta
                alpha = value
        return alpha

    def game_win(self, list):
        column = self.chessboard_size
        row = self.chessboard_size
        for m in range(column):
            for n in range(row):
                if n < row - 4 and (m, n) in list and (m, n + 1) in list and (m, n + 2) in list and (m, n + 3) in list and (m, n + 4) in list:
                    return True
                elif m < row - 4 and (m, n) in list and (m + 1, n) in list and (m + 2, n) in list and (m + 3, n) in list and (m + 4, n) in list:
                    return True
                elif m < row - 4 and n < row - 4 and (m, n) in list and (m + 1, n + 1) in list and (m + 2, n + 2) in list and (m + 3, n + 3) in list and (m + 4, n + 4) in list:
                    return True
                elif m < row - 4 and n > 3 and (m, n) in list and (m + 1, n - 1) in list and (m + 2, n - 2) in list and (m + 3, n - 3) in list and (m + 4, n - 4) in list:
                    return True
            return False

    # def gen(self,list):

    def evaluation(self,ai_round):
        total_score = 0
        if ai_round:
            my_list = self.my_pos
            enemy_list = self.enemy_pos
        else:
            my_list = self.enemy_pos
            enemy_list = self.my_pos

        score_all_arr = []
        my_score = 0
        for pt in my_list:
            m = pt[0]
            n = pt[1]
            my_score += self.cal_score(m, n, 0, 1, enemy_list, my_list, score_all_arr)
            print("lescore: ",my_score,"pt :",pt)
            my_score += self.cal_score(m, n, 1, 0, enemy_list, my_list, score_all_arr)
            print("lescore: ",my_score,"pt :",pt)
            my_score += self.cal_score(m, n, 1, 1, enemy_list, my_list, score_all_arr)
            print("lescore: ", my_score,"pt :",pt)
            my_score += self.cal_score(m, n, -1, 1, enemy_list, my_list, score_all_arr)
            print("lescore: ", my_score,"pt :",pt)
        print("myscore: !!!!!!!!!!!!!!!!!!",my_score)
        #  算敌人的得分， 并减去
        score_all_arr_enemy = []
        enemy_score = 0
        for pt in enemy_list:
            m = pt[0]
            n = pt[1]
            enemy_score += self.cal_score(m, n, 0, 1, my_list, enemy_list, score_all_arr_enemy)
            print("lescore: ", enemy_score,"pt :",pt)
            enemy_score += self.cal_score(m, n, 1, 0, my_list, enemy_list, score_all_arr_enemy)
            print("lescore: ", enemy_score,"pt :",pt)
            enemy_score += self.cal_score(m, n, 1, 1, my_list, enemy_list, score_all_arr_enemy)
            print("lescore: ", enemy_score,"pt :",pt)
            enemy_score += self.cal_score(m, n, -1, 1, my_list, enemy_list, score_all_arr_enemy)
            print("lescore: ", enemy_score,"pt :",pt)
        print("escore: ??????????????????", enemy_score)
        total_score = my_score - enemy_score*0.1
        return total_score

    def cal_score(self, m, n, x_decrict, y_derice, enemy_list, my_list, score_all_arr):

        add_score = 0  # 加分项
        # 在一个方向上， 只取最大的得分项
        max_score_shape = (0, None)


        # 如果此方向上，该点已经有得分形状，不重复计算
        for item in score_all_arr:
            for pt in item[1]:
                if m == pt[0] and n == pt[1] and x_decrict == item[2][0] and y_derice == item[2][1]:
                    return 0

        # 在落子点 左右方向上循环查找得分形状
        for offset in range(-5, 1):
            pos = []
            for i in range(0, 6):
                if (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in enemy_list:
                    pos.append(2)
                elif (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in my_list:
                    pos.append(1)
                elif m + (i + offset) * x_decrict>=self.chessboard_size or m + (i + offset) * x_decrict < 0 or n + (i + offset) * y_derice>= self.chessboard_size or n + (i + offset) * y_derice < 0 :
                    pos.append(2)
                else:
                    pos.append(0)
            tmp_shap5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
            tmp_shap6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])
            print(tmp_shap5)
            print(tmp_shap6)
            for (score, shape) in self.shape_evalue:
                if tmp_shap5 == shape or tmp_shap6 == shape:
                    print("equal: ",shape)
                    if score > max_score_shape[0]:
                        max_score_shape = (score, ((m + (0 + offset) * x_decrict, n + (0 + offset) * y_derice),
                                                   (m + (1 + offset) * x_decrict, n + (1 + offset) * y_derice),
                                                   (m + (2 + offset) * x_decrict, n + (2 + offset) * y_derice),
                                                   (m + (3 + offset) * x_decrict, n + (3 + offset) * y_derice),
                                                   (m + (4 + offset) * x_decrict, n + (4 + offset) * y_derice)),
                                           (x_decrict, y_derice))
        if max_score_shape[1] is not None:
            for item in score_all_arr:
                for pt1 in item[1]:
                    for pt2 in max_score_shape[1]:
                        if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                            print("pt1: ",pt1," pt2: ",pt2)
                            add_score += item[0] + max_score_shape[0]

            score_all_arr.append(max_score_shape)
        print("addscore: ",add_score," maxscoreshape: ",max_score_shape[0])
        return add_score + max_score_shape[0]

    def has_neighbour(self,pt):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if (pt[0] + i, pt[1] + j) in self.whole_pos:
                    return True
        return False

        #==============Find new pos========================================
# Make sure that the position of your decision in chess board is empty.
#If not, return erro