import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)
# don't change the class name

import numpy as np


class Evaluation():
    def __init__(self):
        self.board = np.zeros((15, 15), dtype=np.int)
        self.strategy = []
        Black_Lian_wu = [[-1, -1, -1, -1, -1]]
        Black_Huo_si = [[0, -1, -1, -1, -1, 0], [0, -1, 0, -1, -1, -1, 0], [0, -1, -1, 0, -1, -1, 0],
                        [0, -1, -1, -1, 0, -1, 0]]
        Black_Chong_si = [[0, -1, -1, -1, -1, 1], [0, -1, -1, -1, 0, -1, 1], [0, -1, -1, -1, 0, -1, 1],
                          [0, -1, -1, 0, -1, -1, 1],
                          [0, -1, 0, -1, -1, -1, 1],
                          [1, -1, -1, -1, -1, 0], [1, -1, 0, -1, -1, -1, 0], [1, -1, -1, 0, -1, -1, 0],
                          [1, -1, -1, -1, 0, -1, 0]]
        Black_Huo_san = [[0, -1, -1, -1, 0], [0, -1, -1, 0, -1, 0], [0, -1, 0, -1, -1, 0]]
        Black_Mian_san = [[1, -1, -1, -1, 0], [1, -1, 0, -1, -1, 0], [1, -1, -1, 0, -1, 0],
                          [0, -1, -1, -1, 1], [0, -1, 0, -1, -1, 1], [0, -1, -1, 0, -1, 1]]
        Black_Huo_er = [[0, -1, -1, 0], [0, -1, 0, -1, 0]]
        Black_Mian_er = [[1, -1, -1, 0], [1, -1, 0, -1, 0], [0, -1, -1, 1], [0, -1, 0, -1, 1]]

        White_Lian_wu = [[1, 1, 1, 1, 1]]
        White_Huo_si = [[0, 1, 1, 1, 1, 0], [0, 1, 0, 1, 1, 1, 0], [0, 1, 1, 0, 1, 1, 0],
                        [0, 1, 1, 1, 0, 1, 0]]
        White_Chong_si = [[0, 1, 1, 1, 1, -1], [0, 1, 1, 1, 0, 1, -1], [0, 1, 1, 1, 0, 1, -1],
                          [0, 1, 1, 0, 1, 1, -1],
                          [0, 1, 0, 1, 1, 1, -1],
                          [-1, 1, 1, 1, 1, 0], [-1, 1, 0, 1, 1, 1, 0], [-1, 1, 1, 0, 1, 1, 0],
                          [-1, 1, 1, 1, 0, 1, 0]]
        White_Huo_san = [[0, 1, 1, 1, 0], [0, 1, 1, 0, 1, 0], [0, 1, 0, 1, 1, 0]]
        White_Mian_san = [[-1, 1, 1, 1, 0], [-1, 1, 0, 1, 1, 0], [-1, 1, 1, 0, 1, 0],
                          [0, 1, 1, 1, -1], [0, 1, 0, 1, 1, -1], [0, 1, 1, 0, 1, -1]]
        White_Huo_er = [[0, 1, 1, 0], [0, 1, 0, 1, 0]]
        White_Mian_er = [[-1, 1, 1, 0], [-1, 1, 0, 1, 0], [0, 1, 1, -1], [0, 1, 0, 1, -1]]





        self.Black_strategy = []
        self.Black_strategy.append(Black_Lian_wu)
        self.Black_strategy.append(Black_Huo_si)
        self.Black_strategy.append(Black_Chong_si)
        self.Black_strategy.append(Black_Huo_san)
        self.Black_strategy.append(Black_Mian_san)
        self.Black_strategy.append(Black_Huo_er)
        self.Black_strategy.append(Black_Mian_er)

        self.White_strategy = []
        self.White_strategy.append(White_Lian_wu)
        self.White_strategy.append(White_Huo_si)
        self.White_strategy.append(White_Chong_si)
        self.White_strategy.append(White_Huo_san)
        self.White_strategy.append(White_Mian_san)
        self.White_strategy.append(White_Huo_er)
        self.White_strategy.append(White_Mian_er)

        self.strategy_bcount = [0, 0, 0, 0, 0, 0, 0]
        self.strategy_wcount = [0, 0, 0, 0, 0, 0, 0]

        # def matching(self,ptr,str):

        # 行,ptr就像目标字符串，str就是我们固定的字符串
        '''
        res=0
        for i in range(len(str)):
            for j in str:
                print(j[0])
                for k in range(len(ptr)-len(str)+1):
                    print(ptr)
                    if ptr[k]==j[0]:
                        cnt=1
                        while cnt+k<len(ptr) and cnt<len(str) and ptr[k+cnt] == str[cnt]:
                            cnt+=1
                        if cnt==len(str):
                            res+=1
        return res
        '''

    # 对传进来的str 也就是strategy，里面有很多个类型，对每个类型

    def reset(self):
        for i in range(7):
            self.strategy_bcount[i] = 0
            self.strategy_wcount[i] = 0


    def _mathcing(self, ptr, str):
        res = 0

        for i in range(len(ptr) - len(str) + 1):
            '''
            if ptr[i] == str[0]:
                cnt = 1
                while cnt + i < len(ptr) and cnt < len(str) and ptr[i + cnt] == str[cnt]:
                    cnt += 1
                if cnt == len(str):
                    res += 1
            '''
            if ptr[i] == str[0] and ptr[i+1] == str[1]:
                cnt = 2
                while cnt + i < len(ptr) and cnt < len(str) and ptr[i + cnt] == str[cnt]:
                    cnt += 1
                if cnt == len(str):
                    res += 1

        return res

    # 对于i在策略名单里，我们有strategy,对每个strategy，我们去数他有几个
    def _evaluate_line(self, line):
        # print(line)
        for i in range(len(self.Black_strategy)):
            for strategy in self.Black_strategy[i]:
                self.strategy_bcount[i] += self._mathcing(line, strategy)

        for i in range(len(self.White_strategy)):
            for strategy in self.White_strategy[i]:
                self.strategy_wcount[i] += self._mathcing(line, strategy)

    def cal(self, chessboard):
        # 横向计数


        for i in range(15):
            self._evaluate_line(chessboard[i])
            # self._evaluate_line(chessboard[i])
        # 纵向计数
        for i in range(15):
            line = []
            for j in range(15):
                line.append(chessboard[j, i])
            self._evaluate_line(line)
            # self._evaluate_line(chessboard[i])
        # 对角线
        for i in range(15):
            line = []
            x = i
            y = 0
            while x < 15 and y < 15:
                line.append(chessboard[x, y])
                x += 1
                y += 1
            self._evaluate_line(line)
            # self._evaluate_line(line, self.White_strategy)

        for i in range(14):
            line = []
            x = i
            y = 14
            while x >= 0 and y > 0:
                line.append(chessboard[x, y])
                x -= 1
                y -= 1
            self._evaluate_line(line)

            # second diagonal line analysis
        # 对角线

        for i in range(15):
            line = []
            x = 14 - i
            y = 0
            while x >= 0 and y < 15:
                line.append(chessboard[x, y])
                x -= 1
                y += 1
            self._evaluate_line(line)

        for i in range(14):
            line = []
            x = 14
            y = 14 - i
            while x >= 0 and y < 15:
                line.append(chessboard[x, y])
                x -= 1
                y += 1
            self._evaluate_line(line)
            # self._evaluate_line(line, self.White_strategy)




    def _evaluate(self, color):

        score = 0
        # print(self.strategy_bcount)

        if color == -1:
            if self.strategy_bcount[0] > 0:
                score += 20000
                return score
            if self.strategy_bcount[1] > 0:
                score += 5000
                #return score
            if self.strategy_bcount[2] > 1:
                score += 15000
            elif self.strategy_bcount[2] > 0:
                score += 10000
            if self.strategy_bcount[3] > 1:
                score += 3000
            elif self.strategy_bcount[3] > 0:
                score += 1500
            score += (self.strategy_bcount[4]) * 10
            score += (self.strategy_bcount[5]) * 4
            score += (self.strategy_bcount[6])

            if self.strategy_wcount[0] > 0:
                score -= 21000
            if self.strategy_wcount[1] > 0:
                score -= 6000
            if self.strategy_wcount[2] > 1:
                score -= 16000
            elif self.strategy_wcount[2] > 0:
                score -= 11000
            if self.strategy_wcount[3] > 1:
                score -= 3000
            elif self.strategy_wcount[3] > 0:
                score -= 1500
            score -= (self.strategy_wcount[4]) * 11
            score -= (self.strategy_wcount[5]) * 5
            score -= (self.strategy_wcount[6]) * 2

        if color == 1:
            if self.strategy_wcount[0] > 0:
                score += 20000
                return score
            if self.strategy_wcount[1] > 0:
                score += 5000
                #return score
            if self.strategy_wcount[2] > 1:
                score += 15000
            elif self.strategy_wcount[2] > 0:
                score += 10000
            if self.strategy_wcount[3] > 1:
                score += 3000
            elif self.strategy_wcount[3] > 0:
                score += 1500
            score += (self.strategy_wcount[4]) * 10
            score += (self.strategy_wcount[5]) * 4
            score += (self.strategy_wcount[6])

            if self.strategy_bcount[0] > 0:
                score -= 21000
            if self.strategy_bcount[1] > 0:
                score -= 6000
            if self.strategy_bcount[2] > 1:
                score -= 16000
            elif self.strategy_bcount[2] > 0:
                score -= 11000
            if self.strategy_bcount[3] > 1:
                score -= 3100
            elif self.strategy_bcount[3] > 0:
                score -= 1500
            score -= (self.strategy_bcount[4]) * 11
            score -= (self.strategy_bcount[5]) * 5
            score -= (self.strategy_bcount[6]) * 2

        #print(score)
        return score

    def evaluate(self, chessboard, color):
        # self.board = chessboard
        self.reset()
        self.cal(chessboard)

        # self.board = copy.deepcopy(board)
        # dcolor = -1 if color == 1 else 1
        myScore = self._evaluate(color)
        # self.board = copy.deepcopy(board)
        # dScore = self._evaluate(dcolor)
        # return myScore - dScore * 1.1
        return myScore


def max_min_search(chessboard, color, chessboard_size, depth=3, alpha=-1e9 + 7, beta=1e9 + 7):
    evaluation = Evaluation()

    score = evaluation.evaluate(chessboard, color)

    for x in range(chessboard_size):
        for y in range(chessboard_size):
            # for x,y in chessboard:
            if chessboard[x, y] != 0:
                continue
            chessboard[x, y] = color

            if color == 1:
                dcolor = -1
            else:
                dcolor = 1

            score, x, y = max_min_search(chessboard, dcolor, chessboard_size, depth - 1, -beta, -alpha)
            # score = self.max_min_search(chessboard, color, chessboard_size, depth , alpha, beta)
            chessboard[x, y] = 0

            if score > alpha:
                alpha = score
                # bestmove = (x, y)
                n_x = x
                n_y = y
                if alpha >= beta:
                    break
    if depth == 3:
        n_x = x
        n_y = y
    # print(n_x,n_y)

    # (x, y) = bestmove
    return alpha, n_x, n_y


def search(chessboard, chessboard_size, color, depth=3):
    # evaluation = Evaluation()
    # score = evaluation.evaluate(chessboard, color)

    score, x, y = max_min_search(chessboard, color, chessboard_size)

    # print((x, y))
    return x, y


def search2(chessboard, chessboard_size, color, max=-1e9 + 1):
    evaluation = Evaluation()
    score = evaluation.evaluate(chessboard, color)
    n_x = -1
    n_y = -1
    for x in range(15):
        for y in range(15):
            if chessboard[x, y] != 0:
                continue

            if x >=1 and x < 14 and y >=1 and y<14 :
                if chessboard[x, y + 1] == 0 and chessboard[x, y - 1] == 0 and chessboard[x - 1, y] == 0 and chessboard[
                    x + 1, y] == 0 and chessboard[x + 1, y + 1] == 0 and chessboard[x + 1, y - 1] == 0 and chessboard[
                    x - 1, y + 1] == 0 and chessboard[x - 1, y - 1] == 0:
                    continue


            chessboard[x, y] = color
            score = evaluation.evaluate(chessboard, color)
            chessboard[x, y] = 0
            if (score > max):
                max = score
                n_x = x
                n_y = y
            if score>=9999:
                break
        if score>=9999:
            break
    return n_x, n_y



'''
def search2(chessboard, color, max=-1e9 + 1):
    evaluation = Evaluation()
    score = evaluation.evaluate(chessboard, color)
    n_x = -1
    n_y = -1
    min = 1e9+1
    #score = evaluation.evaluate(chessboard, color)
    for x in range(15):
        for y in range(15):
            if chessboard[x, y] == 0:
                chessboard[x, y] = color
                score = evaluation.evaluate(chessboard, color)
                if score > max:
                    max = score
                    n_x = x
                    n_y = y
                #score_ai = evaluation.evaluate(chessboard, -color)
    return n_x, n_y
'''


class AI(object):
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.time_out = time_out
        self.candidate_list = []

    def go(self, chessboard):
        self.candidate_list.clear()

        my_color = self.color

        '''
        chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[0, 0:4] = -1
        chessboard[1, 0:4] = 1
        '''


        x, y = search2(chessboard, 15, my_color)
        print(x,y)
        # n_x, n_y = search(chessboard, self.chessboard_size, my_color,depth=3)
        # score,x,y=self.search.max_min_search()
        self.candidate_list.append((x, y))


        #print(chessboard)


'''
chessboard = np.zeros((15, 15))
e=Evaluation()

chessboard[1,1]=-1
chessboard[2,2]=1
chessboard[3,3]=1
chessboard[4,4]=1
chessboard[5,5]=1

chessboard[1,10]=-1
chessboard[2,10]=-1
chessboard[3,10]=-1



ai=AI(15,-1,5)
ai.go(chessboard)
'''