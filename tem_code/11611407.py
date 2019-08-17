import numpy as np
import datetime as dt

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
FIVE = 100000
FOUR = DOUBLE_DIE_FOUR = DIE_FOUR_THREE = 10000
DOUBLE_THREE = 5000
DIE_THREE_THREE = 1000
DIE_FOUR = 500
LOW_DIE_FOUR = 400
SINGLE_THREE = 100
JUMP_THREE = 90
TWO = 10
LOW_TWO = 9
DIE_THREE = LOWW_TWO = 5
DIE_TWO = 2
direction = np.array([[0, 1], [1, 0], [1, 1], [1, -1]], dtype=int)


class AI(object):
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit. 17
        self.time_out = time_out

        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your decision
        self.candidate_list = []

        # The input is current chessboard.
    def go(self, chessboard):
        self.candidate_list.clear()     # Clear candidate_list
        # ==================================================================
        # Write your algorithm here
        # Here is the simplest sample:Random decision
        a = np.where(chessboard != 0)
        b = np.where(chessboard == 0)
        c = self.nodelist(chessboard, 1, self.color)
        Color = self.color
        if a[0].size == 0:
            self.candidate_list.append([7, 7])
        elif len(b[0]) == 1:
            self.candidate_list.append([b[0][0], b[1][0]])
        elif c[0][2]*self.color >= 100000:
            self.candidate_list.append([c[0][0], c[0][1]])
        else:
            self.minimax(chessboard, 0, Color, 1000000 * Color)
        # ==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        # If not, return error.
        # assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
        # Add your decision into candidate_list, Records the chess board
        # self.candidate_list.append(new_pos)

    def isinside(self, node):
        if (node[0] < self.chessboard_size) & (node[0] >= 0) & (node[1] < self.chessboard_size) & (node[1] >= 0):
            return 1
        else:
            return 0

    def evaluate(self, board, node, role):
        score = 0
        die_four = 0
        three = 0
        jump_three = 0
        die_three = 0
        sc = 0
        for dir in direction:
            sc = 0
            count = 0
            border = []
            for d in (1, -1):
                dir *= d
                next = node + dir
                temp = next
                while self.isinside(next):
                    if board[next[0], next[1]] == role:
                        count += 1
                        next = next + dir
                        temp = next
                    else:
                        border.append(next)
                        break
                else:  # 超出边界，则记为对手�?
                    border.append(temp)
            count += 1
            l = np.array(border[0])
            r = np.array(border[1])
            l1 = l - dir
            r1 = r + dir
            l2 = l1 - dir
            r2 = r1 + dir
            l3 = l2 - dir
            r3 = r2 + dir
            left = board[l[0], l[1]] if self.isinside(l) else -role
            right = board[r[0], r[1]] if self.isinside(r) else -role
            left1 = board[l1[0], l1[1]] if self.isinside(l1) else -role
            right1 = board[r1[0], r1[1]] if self.isinside(r1) else -role
            left2 = board[l2[0], l2[1]] if self.isinside(l2) else -role
            right2 = board[r2[0], r2[1]] if self.isinside(r2) else -role
            left3 = board[l3[0], l3[1]] if self.isinside(l3) else -role
            right3 = board[r3[0], r3[1]] if self.isinside(r3) else -role
            if count >= 5:
                sc = FIVE
            elif count == 4:
                if (left == 0) & (right == 0):
                    sc = FOUR
                elif (left == 0) | (right == 0):
                    sc = DIE_FOUR
            elif count == 3:
                if (left == 0) & (right == 0):
                    if (left1 == -role) & (right1 == -role):    # 2011102
                        sc = DIE_THREE
                    elif (left1 == role) | (right1 == role):    # 101110
                        sc = LOW_DIE_FOUR
                    elif (left1 == 0) | (right1 == 0):          # 001110
                        sc = SINGLE_THREE
                elif (left == 0) | (right == 0):
                    if left == -role:
                        if right1 == 0:                         # 211100
                            sc = DIE_THREE
                        elif right1 == role:                    # 211101
                            sc = LOW_DIE_FOUR
                    elif right == -role:
                        if left1 == 0:                          # 001112
                            sc = DIE_THREE
                        elif left1 == role:                     # 101112
                            sc = LOW_DIE_FOUR
            elif count == 2:
                if (left == 0) & (right == 0):
                    if ((right1 == 0) & (right2 == role)) | ((left1 == 0) & (left2 == role)):
                        sc = DIE_THREE                          # 011001
                    elif (left1 == 0) & (right1 == 0):
                        sc = TWO                                # 001100
                    elif ((right1 == role) & (right2 == -role)) | ((left1 == role) & (left2 == -role)):
                        sc = DIE_THREE                          # 011012
                    elif ((right1 == role) & (right2 == role)) | ((left1 == role) & (left2 == role)):
                        sc = LOW_DIE_FOUR                       # 011011
                    elif ((right1 == role) & (right2 == 0)) | ((left1 == role) & (left2 == 0)):
                        sc = JUMP_THREE                         # 011010
                elif (left == 0) | (right == 0):
                    if left == -role:
                        if (right1 == 0) & (right2 == 0):
                            sc = DIE_TWO                        # 211000
                        elif (right1 == role) & (right2 == role):
                            sc = LOW_DIE_FOUR                   # 211011
                        elif ((right1 == role) & (right2 == 0)) | ((right2 == role) & (right1 == 0)):
                            sc = DIE_THREE                      # 21101
                    elif right == -role:
                        if (left1 == 0) & (left2 == 0):
                            sc = DIE_TWO
                        elif (left1 == role) & (left2 == role):
                            sc = LOW_DIE_FOUR
                        elif ((left1 == role) & (left2 == 0)) | ((left2 == role) & (left1 == 0)):
                            sc = DIE_THREE
            elif count == 1:
                if (left == 0) & (left1 == role) & (left2 == role) & (left3 == role):
                    sc = LOW_DIE_FOUR           # 11101
                elif (right == 0) & (right1 == role) & (right2 == role) & (right3 == role):
                    sc = LOW_DIE_FOUR
                elif (left == 0) & (left1 == role) & (left2 == role) & (left3 == 0) & (right == 0):
                    sc = JUMP_THREE             # 011010
                elif (right == 0) & (right1 == role) & (right2 == role) & (right3 == 0) & (left == 0):
                    sc = JUMP_THREE
                elif (left == 0) & (left1 == role) & (left2 == role) & (left3 == -role) & (right == 0):
                    sc = DIE_THREE              # 211010
                elif (right == 0) & (right1 == role) & (right2 == role) & (right3 == -role) & (left == 0):
                    sc = DIE_THREE
                elif (left == 0) & (left1 == 0) & (left2 == role) & (left3 == role):
                    sc = DIE_THREE              # 11001
                elif (right == 0) & (right1 == 0) & (right2 == role) & (right3 == role):
                    sc = DIE_THREE
                elif (left == 0) & (left1 == role) & (left2 == 0) & (left3 == role):
                    sc = DIE_THREE              # 10101
                elif (right == 0) & (right1 == role) & (right2 == 0) & (right3 == role):
                    sc = DIE_THREE
                elif (left == 0) & (left1 == role) & (left2 == 0) & (left3 == 0) & (right == 0):
                    sc = LOW_TWO                # 001010
                elif (right == 0) & (right1 == role) & (right2 == 0) & (right3 == 0) & (left == 0):
                    sc = LOW_TWO
                elif (left == 0) & (left1 == 0) & (left2 == role) & (left3 == 0) & (right == 0):
                    sc = LOW_TWO                # 010010
                elif (right == 0) & (right1 == 0) & (right2 == role) & (right3 == 0) & (left == 0):
                    sc = LOW_TWO
            score += sc
            if sc >= 500:
                die_four += 1
            elif (sc == 100) | (sc == 90):
                three += 1
            elif sc == 5:
                die_three += 1
        if die_four > 1:
            score = score + DOUBLE_DIE_FOUR - die_four * 500
        elif (die_four > 0) & (three > 0):
            score = score + DIE_FOUR_THREE - die_four * 500 - three * 100
        elif three > 1:
            score = score + DOUBLE_THREE - three * 100
        elif (die_three > 0) & (three > 0):
            score = score + DIE_THREE_THREE - die_three * 5 - three * 100
        return score

    def defenseEvaluate(self, board, node, role):
        score = 0
        right = -role
        right1 = -role
        right2 = -role
        right3 = -role
        for dir in direction:
            sc = 0
            for d in (1, -1):
                count = 0
                border = []
                dir *= d
                next = node + dir
                temp = next
                while self.isinside(next):
                    if board[next[0], next[1]] == role:
                        count += 1
                        next = next + dir
                        temp = next
                    else:
                        border.append(next)
                        break
                else:  # 超出边界，则记为对手�?
                    border.append(temp)
                if count > 0:
                    l = np.array(border[0])
                    # r = np.array(border[1])
                    l1 = l + dir
                    # r1 = r + dir
                    l2 = l1 + dir
                    # r2 = r1 + dir
                    l3 = l2 + dir
                    # r3 = r2 + dir
                    left = board[l[0], l[1]] if self.isinside(l) else -role
                    left1 = board[l1[0], l1[1]] if self.isinside(l1) else -role
                    left2 = board[l2[0], l2[1]] if self.isinside(l2) else -role
                    left3 = board[l3[0], l3[1]] if self.isinside(l3) else -role
                    if count >= 5:
                        sc = FIVE
                    elif count == 4:
                        if (left == 0) & (right == 0):
                            sc = FOUR
                        elif (left == 0) | (right == 0):
                            sc = DIE_FOUR
                    elif count == 3:
                        if (left == 0) & (right == 0):
                            if (left1 == -role) & (right1 == -role):
                                sc = DIE_THREE
                            elif (left1 == role) | (right1 == role):
                                sc = LOW_DIE_FOUR
                            elif (left1 == 0) | (right1 == 0):
                                sc = SINGLE_THREE
                        elif (left == 0) | (right == 0):
                            if left == -role:
                                if right1 == 0:
                                    sc = DIE_THREE
                                elif right1 == role:
                                    sc = LOW_DIE_FOUR
                            elif right == -role:
                                if left1 == 0:
                                    sc = DIE_THREE
                                elif left1 == role:
                                    sc = LOW_DIE_FOUR
                    elif count == 2:
                        if (left == 0) & (right == 0):
                            if ((right1 == 0) & (right2 == role)) | ((left1 == 0) & (left2 == role)):
                                sc = DIE_THREE
                            elif (left1 == 0) & (right1 == 0):
                                sc = TWO
                            elif ((right1 == role) & (right2 == -role)) | ((left1 == role) & (left2 == -role)):
                                sc = DIE_THREE
                            elif ((right1 == role) & (right2 == role)) | ((left1 == role) & (left2 == role)):
                                sc = LOW_DIE_FOUR
                            elif ((right1 == role) & (right2 == 0)) | ((left1 == role) & (left2 == 0)):
                                sc = JUMP_THREE
                        elif (left == 0) | (right == 0):
                            if left == -role:
                                if (right1 == 0) & (right2 == 0):
                                    sc = DIE_TWO
                                elif (right1 == role) & (right2 == role):
                                    sc = LOW_DIE_FOUR
                                elif ((right1 == role) & (right2 == 0)) | ((right2 == role) & (right1 == 0)):
                                    sc = DIE_THREE
                            elif right == -role:
                                if (left1 == 0) & (left2 == 0):
                                    sc = DIE_TWO
                                elif (left1 == role) & (left2 == role):
                                    sc = LOW_DIE_FOUR
                                elif ((left1 == role) & (left2 == 0)) | ((left1 == role) & (left2 == 0)):
                                    sc = DIE_THREE
                    elif count == 1:
                        if (left == 0) & (left1 == role) & (left2 == role) & (left3 == role):
                            sc = LOW_DIE_FOUR
                        elif (right == 0) & (right1 == role) & (right2 == role) & (right3 == role):
                            sc = LOW_DIE_FOUR
                        elif (left == 0) & (left1 == role) & (left2 == role) & (left3 == 0) & (right == 0):
                            sc = JUMP_THREE
                        elif (right == 0) & (right1 == role) & (right2 == role) & (right3 == 0) & (left == 0):
                            sc = JUMP_THREE
                        elif (left == 0) & (left1 == role) & (left2 == role) & (left3 == -role) & (right == 0):
                            sc = DIE_THREE
                        elif (right == 0) & (right1 == role) & (right2 == role) & (right3 == -role) & (left == 0):
                            sc = DIE_THREE
                        elif (left == 0) & (left1 == 0) & (left2 == role) & (left3 == role):
                            sc = DIE_THREE
                        elif (right == 0) & (right1 == 0) & (right2 == role) & (right3 == role):
                            sc = DIE_THREE
                        elif (left == 0) & (left1 == role) & (left2 == 0) & (left3 == role):
                            sc = DIE_THREE
                        elif (right == 0) & (right1 == role) & (right2 == 0) & (right3 == role):
                            sc = DIE_THREE
                        elif (left == 0) & (left1 == role) & (left2 == 0) & (left3 == 0) & (right == 0):
                            sc = LOW_TWO
                        elif (right == 0) & (right1 == role) & (right2 == 0) & (right3 == 0) & (left == 0):
                            sc = LOW_TWO
                        elif (left == 0) & (left1 == 0) & (left2 == role) & (left3 == 0) & (right == 0):
                            sc = LOW_TWO                # 010010
                        elif (right == 0) & (right1 == 0) & (right2 == role) & (right3 == 0) & (left == 0):
                            sc = LOW_TWO
                    score += sc
        sc = score * role
        return sc

    def minimax(self, board, depth, max_min, bestv):
        c1 = self.nodelist(board, 1, max_min)  # 跳过
        if depth == 3:
            board[c1[0][0], c1[0][1]] = max_min
            score = self.boardEvaluate(board)
            board[c1[0][0], c1[0][1]] = 0
            return score

        bestvalue = -100000000 if max_min == 1 else 100000000

        list = []
        if len(c1) == 0:
            return bestvalue
        else:
            list.append([c1[0][0], c1[0][1]])
        for i in range(6):
            if i < len(c1):
                board[c1[i][0], c1[i][1]] = max_min
                if len(c1) < 4:
                    value = self.minimax(board, 5-len(c1), -max_min, bestvalue)  # 走下�?
                else:
                    value = self.minimax(board, depth + 1, -max_min, bestvalue)  # 走下�?
                if max_min == 1:
                    if (value >= bestv):
                        board[c1[i][0], c1[i][1]] = 0
                        return value
                    elif value > bestvalue:
                        bestvalue = value
                        board[c1[i][0], c1[i][1]] = 0
                        if depth == 0:
                            list.clear()
                            list.append((c1[i][0], c1[i][1]))
                    elif value == bestvalue:
                        board[c1[i][0], c1[i][1]] = 0
                        if self.evaluate(board, np.array([c1[i][0], c1[i][1]]), max_min) > self.evaluate(board, np.array([list[0][0], list[0][1]]), max_min):
                            list.clear()
                            list.append((c1[i][0], c1[i][1]))
                elif max_min == -1:
                    if (value <= bestv):
                            board[c1[i][0], c1[i][1]] = 0
                            return value
                    elif value < bestvalue:
                        bestvalue = value
                        board[c1[i][0], c1[i][1]] = 0
                        if depth == 0:
                            list.clear()
                            list.append((c1[i][0], c1[i][1]))
                    elif value == bestvalue:
                        board[c1[i][0], c1[i][1]] = 0
                        if self.evaluate(board, np.array([c1[i][0], c1[i][1]]), max_min) < self.evaluate(board, np.array([list[0][0], list[0][1]]), max_min):
                            list.clear()
                            list.append((c1[i][0], c1[i][1]))
                board[c1[i][0], c1[i][1]] = 0
            else:
                if depth == 0:
                    self.candidate_list.append(list[len(list) - 1])
                return bestvalue
        if depth == 0:
            self.candidate_list.append(list[len(list)-1])
        return bestvalue

    def nextNode(self, board, width):
        nodes = np.array(np.where(board == 0)).transpose()
        nextnodes = []
        for node in nodes:
            x1 = node[0] - width if (node[0] - width >= 0) else 0
            x2 = node[0] + 1 + width if (node[0] + 1 + width < self.chessboard_size) else self.chessboard_size-1
            y1 = node[1] - width if (node[1] - width >= 0) else 0
            y2 = node[1] + 1 + width if (node[1] + 1 + width < self.chessboard_size) else self.chessboard_size-1
            x = board[x1:x2, y1:y2]
            y = np.where(x != 0)
            if y[0].size > 0:
                nextnodes.append(node)
        nodes = np.array(nextnodes)
        return nodes

    def nodelist(self, board, width, color):
        finallist = []
        nodes = self.nextNode(board, width)
        if nodes.size > 0:
            alist = []
            blist = []
            for node in nodes:
                a = self.evaluate(board, node, color)
                b = self.evaluate(board, node, -color)
                alist.append((node[0], node[1], a))
                blist.append((node[0], node[1], b))
            aarray = np.array(alist)
            barray = np.array(blist)
            amax = aarray[np.lexsort(-aarray.T)]
            bmax = barray[np.lexsort(-barray.T)]
            i = 0
            while bmax[i][2] > amax[0][2]:
                finallist.append(bmax[i])
                i += 1
            j = 0
            finallist.append(amax[0])
            while amax[j][2] == amax[j+1][2]:
                finallist.append(amax[j+1])
                j += 1
            while bmax[i][2] == amax[0][2]:
                finallist.append(bmax[i])
                i += 1
            cmax = amax[j+1: , ]
            final = np.concatenate((finallist, cmax), axis=0)
        return final

    def boardEvaluate(self, board):
        boardscore = 0
        for role in (1, -1):
            die_four = 0
            three = 0
            jump_three = 0
            die_three = 0
            nodes = np.array(np.where(board == role)).transpose()
            searcheddir = np.zeros((15, 15, 4))
            score = 0
            for node in nodes:
                sc = 0
                for i in range(4):
                    if searcheddir[node[0], node[1], i] == 0:
                        dir = direction[i]
                        sc = 0
                        count = 0
                        border = []
                        for d in (1, -1):
                            dir *= d
                            next = node + dir
                            temp = next
                            while self.isinside(next):
                                if board[next[0], next[1]] == role:
                                    searcheddir[next[0], next[1], i] = 1
                                    count += 1
                                    next = next + dir
                                    temp = next
                                else:
                                    border.append(next)
                                    break
                            else:  # 超出边界，则记为对手�?
                                border.append(temp)
                        count += 1
                        l = np.array(border[0])
                        r = np.array(border[1])
                        l1 = l - dir
                        r1 = r + dir
                        l2 = l1 - dir
                        r2 = r1 + dir
                        l3 = l2 - dir
                        r3 = r2 + dir
                        left = board[l[0], l[1]] if self.isinside(l) else -role
                        right = board[r[0], r[1]] if self.isinside(r) else -role
                        left1 = board[l1[0], l1[1]] if self.isinside(l1) else -role
                        right1 = board[r1[0], r1[1]] if self.isinside(r1) else -role
                        left2 = board[l2[0], l2[1]] if self.isinside(l2) else -role
                        right2 = board[r2[0], r2[1]] if self.isinside(r2) else -role
                        left3 = board[l3[0], l3[1]] if self.isinside(l3) else -role
                        right3 = board[r3[0], r3[1]] if self.isinside(r3) else -role
                        if count >= 5:
                            sc = FIVE
                        elif count == 4:
                            if (left == 0) & (right == 0):
                                sc = FOUR
                            elif (left == 0) | (right == 0):
                                sc = DIE_FOUR
                        elif count == 3:
                            if (left == 0) & (right == 0):
                                if (left1 == -role) & (right1 == -role):  # 2011102
                                    sc = DIE_THREE
                                elif (left1 == role) | (right1 == role):  # 101110
                                    sc = LOW_DIE_FOUR
                                elif (left1 == 0) | (right1 == 0):  # 001110
                                    sc = SINGLE_THREE
                            elif (left == 0) | (right == 0):
                                if left == -role:
                                    if right1 == 0:  # 211100
                                        sc = DIE_THREE
                                    elif right1 == role:  # 211101
                                        sc = LOW_DIE_FOUR
                                elif right == -role:
                                    if left1 == 0:  # 001112
                                        sc = DIE_THREE
                                    elif left1 == role:  # 101112
                                        sc = LOW_DIE_FOUR
                        elif count == 2:
                            if (left == 0) & (right == 0):
                                if ((right1 == 0) & (right2 == role)) | ((left1 == 0) & (left2 == role)):
                                    sc = DIE_THREE  # 011001
                                elif (left1 == 0) & (right1 == 0):
                                    sc = TWO  # 001100
                                elif ((right1 == role) & (right2 == -role)) | ((left1 == role) & (left2 == -role)):
                                    sc = DIE_THREE  # 011012
                                elif ((right1 == role) & (right2 == role)) | ((left1 == role) & (left2 == role)):
                                    sc = LOW_DIE_FOUR  # 011011
                                elif ((right1 == role) & (right2 == 0)) | ((left1 == role) & (left2 == 0)):
                                    sc = JUMP_THREE  # 011010
                            elif (left == 0) | (right == 0):
                                if left == -role:
                                    if (right1 == 0) & (right2 == 0):
                                        sc = DIE_TWO  # 211000
                                    elif (right1 == role) & (right2 == role):
                                        sc = LOW_DIE_FOUR  # 211011
                                    elif ((right1 == role) & (right2 == 0)) | ((right2 == role) & (right1 == 0)):
                                        sc = DIE_THREE  # 21101
                                elif right == -role:
                                    if (left1 == 0) & (left2 == 0):
                                        sc = DIE_TWO
                                    elif (left1 == role) & (left2 == role):
                                        sc = LOW_DIE_FOUR
                                    elif ((left1 == role) & (left2 == 0)) | ((left2 == role) & (left1 == 0)):
                                        sc = DIE_THREE
                        elif count == 1:
                            if (left == 0) & (left1 == role) & (left2 == role) & (left3 == role):
                                sc = LOW_DIE_FOUR  # 11101
                            elif (right == 0) & (right1 == role) & (right2 == role) & (right3 == role):
                                sc = LOW_DIE_FOUR
                            elif (left == 0) & (left1 == role) & (left2 == role) & (left3 == 0) & (right == 0):
                                sc = JUMP_THREE  # 011010
                            elif (right == 0) & (right1 == role) & (right2 == role) & (right3 == 0) & (left == 0):
                                sc = JUMP_THREE
                            elif (left == 0) & (left1 == role) & (left2 == role) & (left3 == -role) & (right == 0):
                                sc = DIE_THREE  # 211010
                            elif (right == 0) & (right1 == role) & (right2 == role) & (right3 == -role) & (left == 0):
                                sc = DIE_THREE
                            elif (left == 0) & (left1 == 0) & (left2 == role) & (left3 == role):
                                sc = DIE_THREE  # 11001
                            elif (right == 0) & (right1 == 0) & (right2 == role) & (right3 == role):
                                sc = DIE_THREE
                            elif (left == 0) & (left1 == role) & (left2 == 0) & (left3 == role):
                                sc = DIE_THREE  # 10101
                            elif (right == 0) & (right1 == role) & (right2 == 0) & (right3 == role):
                                sc = DIE_THREE
                            elif (left == 0) & (left1 == role) & (left2 == 0) & (left3 == 0) & (right == 0):
                                sc = LOW_TWO  # 001010
                            elif (right == 0) & (right1 == role) & (right2 == 0) & (right3 == 0) & (left == 0):
                                sc = LOW_TWO
                            elif (left == 0) & (left1 == 0) & (left2 == role) & (left3 == 0) & (right == 0):
                                sc = LOW_TWO  # 010010
                            elif (right == 0) & (right1 == 0) & (right2 == role) & (right3 == 0) & (left == 0):
                                sc = LOW_TWO
                        score += sc
                        if sc >= 500:
                            die_four += 1
                        elif (sc == 100) | (sc == 90):
                            three += 1
                        elif sc == 5:
                            die_three += 1
            if die_four > 1:
                score = score + DOUBLE_DIE_FOUR - die_four * 500
            elif die_four + three > 1:
                score = score + DIE_FOUR_THREE - die_four * 500 - three * 100
            elif three > 1:
                score = score + DOUBLE_THREE - three * 100
            elif die_three + three > 1:
                score = score + DIE_THREE_THREE - die_three * 5 - three * 100
            sc = score * role
            boardscore += sc
        return boardscore


'''
chessboard = np.zeros((15, 15), dtype=np.int)
chessboard[1, 1] = 1
chessboard[2, 2] = 1
chessboard[3, 3] = 1
chessboard[1, 10] = -1
chessboard[2, 10] = -1
chessboard[2, 11] = -1
chessboard[2, 12] = -1
ai = AI(15, -1, 1)
b = ai.defenseEvaluate(chessboard, np.array([1, 8]), 1)
c = ai.nodelist(chessboard, 1, 1)
d = ai.boardEvaluate(chessboard)
time1 = dt.datetime.now().strftime('%H:%M:%S.%f')
ai.go(chessboard)
time2 = dt.datetime.now().strftime('%H:%M:%S.%f')
print(ai.candidate_list)
print(time1)
print(time2)
chessboard[7, 7] = -1
chessboard[8, 8] = 1
chessboard[8, 7] = -1
chessboard[6, 7] = 1
chessboard[6, 8] = -1
chessboard[5, 9] = 1
chessboard[7, 6] = -1
chessboard[6, 5] = 1
chessboard[7, 8] = -1
chessboard[7, 5] = 1
chessboard[6, 9] = -1
chessboard[5, 10] = 1
chessboard[7, 10] = -1
chessboard[7, 9] = 1
chessboard[5, 8] = -1
chessboard[4, 7] = 1
chessboard[9, 6] = -1
chessboard[10, 5] = 1
chessboard[9, 5] = -1
chessboard[8, 6] = 1
chessboard[8, 11] = -1
chessboard[9, 12] = 1
chessboard[9, 7] = -1
chessboard[9, 8] = 1
chessboard[10, 7] = -1
chessboard[11, 7] = 1
chessboard[9, 4] = -1
chessboard[9, 3] = 1
chessboard[4, 8] = -1
chessboard[3, 8] = 1
chessboard[7, 4] = -1
chessboard[8, 5] = 1
chessboard[8, 4] = -1
chessboard[5, 5] = 1
chessboard[4, 5] = -1
chessboard[6, 4] = 1
chessboard[5, 3] = -1
chessboard[2, 9 ] =1
chessboard[5, 6] = -1
chessboard[6, 6] = 1
chessboard[6, 3] = -1
chessboard[2, 7] = 1
chessboard[10, 4] = -1
chessboard[11, 4] = 1


'''
'''
ai = AI(15, 1, 1)
Board = np.zeros(225, dtype=int).reshape((15, 15))
Board[7, 7] = 1
Board[8, 8] = -1
Board[7, 8] = 1
Board[7, 6] = -1
Board[8, 7] = 1
Board[6, 7] = -1
Board[6, 9] = 1
Board[9, 6] = -1
Board[5, 10] = 1
Board[4, 11] = -1
Board[5, 8] = 1
Board[10, 6] = -1
Board[8, 6] = 1
Board[5, 9] = -1
Board[9, 7] = 1
Board[11, 7] = -1
Board[9, 5] = 1
Board[10, 4] = -1
Board[10, 8] = 1
Board[7, 5] = -1
Board[11, 9] = 1
Board[12, 10] = -1
Board[7, 10] = 1
Board[8, 11] = -1
Board[7, 9] = 1
Board[7, 11] = -1
Board[4, 7] = 1
Board[3, 6] = -1
Board[6, 11] = 1
Board[10, 3] = -1
Board[10, 5] = 1
Board[9, 4] = -1
Board[8, 5] = 1
Board[8, 4] = -1
ai.go(Board)
c = ai.candidate_list'''
