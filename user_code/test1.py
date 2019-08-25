import numpy as np
import random
import time

COLOR_BLACK = -1  # True hum
COLOR_WHITE = 1  # False com
COLOR_NONE = 0
MAX_DEPTH = 4
LIMIT = 20
THRESHOLD = 1.15

candidate_list = []
chessboard = np.zeros([15, 15], dtype=int)
com_scoreboard = np.zeros([15, 15], dtype=int)
hum_scoreboard = np.zeros([15, 15], dtype=int)
scoreboard = np.zeros([15, 15], dtype=int)
scoreboard_dir = np.zeros([15, 15, 4, 2], dtype=int)
chessSearch = [[7, 7],
               [7, 8],
               [6, 8],
               [6, 7],
               [6, 6],
               [7, 6],
               [8, 6],
               [8, 7],
               [8, 8],
               [8, 9],
               [7, 9],
               [6, 9],
               [5, 9],
               [5, 8],
               [5, 7],
               [5, 6],
               [5, 5],
               [6, 5],
               [7, 5],
               [8, 5],
               [9, 5],
               [9, 6],
               [9, 7],
               [9, 8],
               [9, 9],
               [9, 10],
               [8, 10],
               [7, 10],
               [6, 10],
               [5, 10],
               [4, 10],
               [4, 9],
               [4, 8],
               [4, 7],
               [4, 6],
               [4, 5],
               [4, 4],
               [5, 4],
               [6, 4],
               [7, 4],
               [8, 4],
               [9, 4],
               [10, 4],
               [10, 5],
               [10, 6],
               [10, 7],
               [10, 8],
               [10, 9],
               [10, 10],
               [10, 11],
               [9, 11],
               [8, 11],
               [7, 11],
               [6, 11],
               [5, 11],
               [4, 11],
               [3, 11],
               [3, 10],
               [3, 9],
               [3, 8],
               [3, 7],
               [3, 6],
               [3, 5],
               [3, 4],
               [3, 3],
               [4, 3],
               [5, 3],
               [6, 3],
               [7, 3],
               [8, 3],
               [9, 3],
               [10, 3],
               [11, 3],
               [11, 4],
               [11, 5],
               [11, 6],
               [11, 7],
               [11, 8],
               [11, 9],
               [11, 10],
               [11, 11],
               [11, 12],
               [10, 12],
               [9, 12],
               [8, 12],
               [7, 12],
               [6, 12],
               [5, 12],
               [4, 12],
               [3, 12],
               [2, 12],
               [2, 11],
               [2, 10],
               [2, 9],
               [2, 8],
               [2, 7],
               [2, 6],
               [2, 5],
               [2, 4],
               [2, 3],
               [2, 2],
               [3, 2],
               [4, 2],
               [5, 2],
               [6, 2],
               [7, 2],
               [8, 2],
               [9, 2],
               [10, 2],
               [11, 2],
               [12, 2],
               [12, 3],
               [12, 4],
               [12, 5],
               [12, 6],
               [12, 7],
               [12, 8],
               [12, 9],
               [12, 10],
               [12, 11],
               [12, 12],
               [12, 13],
               [11, 13],
               [10, 13],
               [9, 13],
               [8, 13],
               [7, 13],
               [6, 13],
               [5, 13],
               [4, 13],
               [3, 13],
               [2, 13],
               [1, 13],
               [1, 12],
               [1, 11],
               [1, 10],
               [1, 9],
               [1, 8],
               [1, 7],
               [1, 6],
               [1, 5],
               [1, 4],
               [1, 3],
               [1, 2],
               [1, 1],
               [2, 1],
               [3, 1],
               [4, 1],
               [5, 1],
               [6, 1],
               [7, 1],
               [8, 1],
               [9, 1],
               [10, 1],
               [11, 1],
               [12, 1],
               [13, 1],
               [13, 2],
               [13, 3],
               [13, 4],
               [13, 5],
               [13, 6],
               [13, 7],
               [13, 8],
               [13, 9],
               [13, 10],
               [13, 11],
               [13, 12],
               [13, 13],
               [13, 14],
               [12, 14],
               [11, 14],
               [10, 14],
               [9, 14],
               [8, 14],
               [7, 14],
               [6, 14],
               [5, 14],
               [4, 14],
               [3, 14],
               [2, 14],
               [1, 14],
               [0, 14],
               [0, 13],
               [0, 12],
               [0, 11],
               [0, 10],
               [0, 9],
               [0, 8],
               [0, 7],
               [0, 6],
               [0, 5],
               [0, 4],
               [0, 3],
               [0, 2],
               [0, 1],
               [0, 0],
               [1, 0],
               [2, 0],
               [3, 0],
               [4, 0],
               [5, 0],
               [6, 0],
               [7, 0],
               [8, 0],
               [9, 0],
               [10, 0],
               [11, 0],
               [12, 0],
               [13, 0],
               [14, 0],
               [14, 1],
               [14, 2],
               [14, 3],
               [14, 4],
               [14, 5],
               [14, 6],
               [14, 7],
               [14, 8],
               [14, 9],
               [14, 10],
               [14, 11],
               [14, 12],
               [14, 13],
               [14, 14]]
direction = [[0, 1], [1, -1], [1, 0], [1, 1]]
chessboard_size = 15
time_out = 1000
pattern_score = {"five": 10000000,
                 "four": 100000,
                 "blocked_four": 10000,
                 "three": 1000,
                 "blocked_three": 100, "two": 100,
                 "blocked_two": 10, "one": 10,
                 "blocked_one": 1}
MAX = 10 * pattern_score["five"]
MIN = -MAX


# don't change the class name
class Step:
    def __init__(self, p, value):
        self.p = p
        self.value = value


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

    # The input is current chessboard.
    def go(self, chessboard):
        # Clear candidate_list
        self.candidate_list.clear()
        start = time.time()
        # ==================================================================
        # Write your algorithm here
        # Here is the simplest sample:Random decision
        board_count = score_all(chessboard)
        # print(com_scoreboard)
        # print(hum_scoreboard)
        if self.color == -1:
            player = True
        else:
            player = False
        if board_count==2 and player:
            new_pos = opening(chessboard)
        else:
            # points = gen_candidate(player, chessboard, False)
            points = greed(player,chessboard)
            #print(points)
            if len(points) == 0:
                new_pos = [7, 7]
            else:
                # new_pos = deeping(player, points, chessboard, board_count)
                new_pos = points[0]
        assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
        self.candidate_list.append(new_pos)
        # ==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        # If not, return error.
        run_time = (time.time() - start)
        # print(run_time)
        # print(chessboard)
        # print(self.candidate_list[0])
        # Add your decision into candidate_list, Records the chess board


def score_all(chessboard):
    boardcount = 0
    for p in chessSearch:
        x, y = p
        if chessboard[x, y] == COLOR_NONE:
            if has_neighbour(x, y, 2, 2, chessboard):
                com_scoreboard[x, y] = evaluate_point(x, y, False, -1, chessboard)
                hum_scoreboard[x, y] = evaluate_point(x, y, True, -1, chessboard)
        elif chessboard[x, y] == COLOR_WHITE:
            boardcount += 1
            com_scoreboard[x, y] = evaluate_point(x, y, False, -1, chessboard)
            hum_scoreboard[x, y] = 0
        elif chessboard[x, y] == COLOR_BLACK:
            boardcount += 1
            hum_scoreboard[x, y] = evaluate_point(x, y, True, -1, chessboard)
            com_scoreboard[x, y] = 0
    return boardcount


def update(x, y, d, chessboard):
    if chessboard[x, y] != COLOR_BLACK:
        com_scoreboard[x, y] = evaluate_point(x, y, False, d, chessboard)
    else:
        com_scoreboard[x, y] = 0
    if chessboard[x, y] != COLOR_WHITE:
        hum_scoreboard[x, y] = evaluate_point(x, y, True, d, chessboard)
    else:
        com_scoreboard[x, y] = 0


def update_score(p, chessboard):
    for i in range(-4, 5):
        x = p[0]
        y = p[1] + i
        if y < 0:
            continue
        if y >= chessboard_size:
            break
        update(x, y, 0, chessboard)
    for i in range(-4, 5):
        x = p[0] + i
        y = p[1]
        if x < 0:
            continue
        if x >= chessboard_size:
            break
        update(x, y, 1, chessboard)
    for i in range(-4, 5):
        x = p[0] + i
        y = p[1] + i
        if x < 0 or y < 0:
            continue
        if x >= chessboard_size or y >= chessboard_size:
            break
        update(x, y, 2, chessboard)
    for i in range(-4, 5):
        x = p[0] + i
        y = p[1] - i
        if x < 0 or y < 0:
            continue
        if x >= chessboard_size or y >= chessboard_size:
            continue
        update(x, y, 3, chessboard)


def opening(chessboard):
    if chessboard[6,6]==COLOR_WHITE:
        return [6,8]
    elif chessboard[6,7]==COLOR_WHITE:
        return [6,8]
    elif chessboard[7,6]==COLOR_WHITE:
        return [6,6]
    elif chessboard[8,7]==COLOR_WHITE:
        return [8,6]
    elif chessboard[7,8]==COLOR_WHITE:
        return [8,8]
    elif chessboard[8,6]==COLOR_WHITE:
        return [6,6]
    elif chessboard[8,8]==COLOR_WHITE:
        return [8,6]
    elif chessboard[6,8]==COLOR_WHITE:
        return [8,8]
    while True:
        x = random.randint(3, 4) * 2
        y = random.randint(3, 4) * 2
        if chessboard[x,y]==COLOR_NONE:
            break
    return [x,y]

def negamax(points, player, depth, chessboard, alpha, beta, chess_count):
    step = []
    for p in points:
        x1 = p[0]
        y1 = p[1]
        chessboard[x1, y1] = (COLOR_BLACK if player else COLOR_WHITE)
        update_score(p, chessboard)
        v = -alpha_beta(-beta, -alpha, not player, depth - 1, 1, chessboard, chess_count + 1)
        scoreboard[x1, y1] = v
        chessboard[x1, y1] = COLOR_NONE
        update_score(p, chessboard)
        alpha = max(alpha, v)
        # print(p, v)
    return alpha


def deeping(player, points, chessboard, board_count):
    i = 2
    while i <= MAX_DEPTH:
        best_score = negamax(points, player, i, chessboard, MIN, MAX, board_count)
        if bigger_than(best_score, pattern_score["five"]) or equal(best_score, pattern_score["five"]):
            break
        i += 2
    # print(scoreboard)
    max = MIN
    step = []
    for p in points:
        if scoreboard[p[0], p[1]] > max:
            max = scoreboard[p[0], p[1]]
            step = p
    return step


def equal(a, b):
    if b == 0:
        b = 0.01
    if b >= 0:
        if b / THRESHOLD <= a <= b * THRESHOLD:
            return True
    else:
        if b / THRESHOLD >= a >= b * THRESHOLD:
            return True
    return False


def bigger_than(a, b):
    if b >= 0:
        if a >= (b + 0.1) * THRESHOLD:
            return True
    else:
        if a >= (b + 0.1) / THRESHOLD:
            return True
    return False


def smaller_than(a, b):
    if b >= 0:
        if a <= (b - 0.1) / THRESHOLD:
            return True
    else:
        if a <= (b - 0.1) * THRESHOLD:
            return True
    return False


def alpha_beta(alpha, beta, player, depth, step, chessboard, chess_count):
    result = evaluate(player, chessboard)
    end = result
    best = MIN
    if depth < 0 or bigger_than(result, pattern_score["five"]) or equal(result, pattern_score["five"]) or smaller_than(
            result, -pattern_score["five"]) or equal(result, -pattern_score["five"]):
        return end
    candidates = gen_candidate(player, chessboard, step > 1 if chess_count > 10 else step > 3)
    if len(candidates) == 0:
        return end
    for p in candidates:
        x1 = p[0]
        y1 = p[1]
        chessboard[x1, y1] = (COLOR_BLACK if player else COLOR_WHITE)
        update_score(p, chessboard)
        v = -alpha_beta(-beta, -alpha, not player, depth - 1, step + 1, chessboard, chess_count + 1)
        chessboard[x1, y1] = COLOR_NONE
        update_score(p, chessboard)
        if v > best:
            best = v
        alpha = max(best, alpha)
        if bigger_than(v, beta):
            v = MAX - 1
            return v
    return best


def max_score(elem):
    com_score = com_scoreboard[elem[0], elem[1]]
    hum_score = hum_scoreboard[elem[0], elem[1]]
    result = fixscore(max(com_score, hum_score))
    return result


def fixscore(score):
    if pattern_score["four"] > score >= pattern_score["blocked_four"]:
        if pattern_score["blocked_four"] <= score < pattern_score["blocked_four"] + pattern_score["three"]:
            return pattern_score["three"]
        elif pattern_score["blocked_four"] + pattern_score["three"] <= score < pattern_score["blocked_four"] * 2:
            return pattern_score["four"]
        else:
            return pattern_score["four"] * 2
    return score


def gen_candidate(player, chessboard, onlythree):
    humfives = []
    comfives = []
    comfours = []
    humfours = []
    comblockedfours = []
    humblockedfours = []
    comtwothrees = []
    humtwothrees = []
    comthrees = []
    humthrees = []
    comtwos = []
    humtwos = []
    neighbors = []
    temp = []
    result = []
    for p in chessSearch:
        x = p[0]
        y = p[1]
        if chessboard[x, y] == COLOR_NONE:
            if not (has_neighbour(x, y, 1, 1, chessboard) or has_neighbour(x, y, 2, 2, chessboard)):
                continue
            temp.append(p)
    # print(temp)
    for p in temp:
        com_score = fixscore(com_scoreboard[p[0], p[1]])
        hum_score = fixscore(hum_scoreboard[p[0], p[1]])
        if hum_score >= pattern_score["five"]:
            humfives.append(p)
        elif com_score >= pattern_score["five"]:
            comfives.append(p)
        elif hum_score >= pattern_score["four"]:
            humfours.append(p)
        elif com_score >= pattern_score["four"]:
            comfours.append(p)
        elif hum_score >= pattern_score["blocked_four"]:
            humblockedfours.append(p)
        elif com_score >= pattern_score["blocked_four"]:
            comblockedfours.append(p)
        elif hum_score >= pattern_score["three"] * 2:
            humtwothrees.append(p)
        elif com_score >= pattern_score["three"] * 2:
            comtwothrees.append(p)
        elif hum_score >= pattern_score["three"]:
            humthrees.append(p)
        elif com_score >= pattern_score["three"]:
            comthrees.append(p)
        elif hum_score >= pattern_score["two"]:
            humtwos.insert(0, p)
        elif com_score >= pattern_score["two"]:
            comtwos.insert(0, p)
        else:
            neighbors.append(p)
    fives = (humfives + comfives if player else comfives + humfives)
    if len(fives):
        return fives
    if player and len(humfours):
        return humfours
    if not player and len(comfours):
        return comfours
    if player and len(comfours) and not len(humblockedfours):
        return comfours
    if not player and len(humfours) and not len(comblockedfours):
        return humfours
    fours = (humfours + comfours if player else comfours + humfours)
    blockedfours = (humblockedfours + comblockedfours if player else comblockedfours + humblockedfours)
    if len(fours):
        return fours + blockedfours
    if player:
        result = humtwothrees + comtwothrees + humblockedfours + comblockedfours + humthrees + comthrees
    else:
        result = comtwothrees + humtwothrees + comblockedfours + humblockedfours + comthrees + humthrees
    if len(comtwothrees) or len(humtwothrees):
        return result
    if onlythree:
        return result
    if player:
        twos = humtwos + comtwos
    else:
        twos = comtwos + humtwos
    twos.sort(key=func, reverse=True)
    result += (twos if len(twos) else neighbors)
    if len(result) > LIMIT:
        result = result[0:LIMIT]
    return result


def greed(player,chessboard):
    temp = []
    for p in chessSearch:
        x = p[0]
        y = p[1]
        if chessboard[x, y] == COLOR_NONE:
            if not (has_neighbour(x, y, 1, 1, chessboard) or has_neighbour(x, y, 2, 2, chessboard)):
                continue
            temp.append(p)
    for i in range(len(temp)-1):
        for j in range(len(temp)-i-1):
            if smaller_than(max_score(temp[j]),max_score(temp[j+1])):
                temp[j],temp[j+1] = temp[j+1],temp[j]
            if equal(max_score(temp[j]),max_score(temp[j+1])):
                if (bigger_than(hum_scoreboard[temp[j+1][0],temp[j+1][1]],com_scoreboard[temp[j+1][0],temp[j+1][1]]) or equal(hum_scoreboard[temp[j+1][0],temp[j+1][1]],com_scoreboard[temp[j+1][0],temp[j+1][1]])) and player:
                    temp[j], temp[j + 1] = temp[j + 1], temp[j]
                if (bigger_than(com_scoreboard[temp[j+1][0],temp[j+1][1]],hum_scoreboard[temp[j+1][0],temp[j+1][1]]) or equal(com_scoreboard[temp[j+1][0],temp[j+1][1]],hum_scoreboard[temp[j+1][0],temp[j+1][1]])) and not player:
                    temp[j], temp[j + 1] = temp[j + 1], temp[j]
    return temp

def func(elem):
    com_score = com_scoreboard[elem[0], elem[1]]
    hum_score = hum_scoreboard[elem[0], elem[1]]
    return max(com_score, hum_score)


def has_neighbour(x, y, distance, count, chessboard):
    cnt = count
    for i in range(x - distance, x + distance + 1):
        if i < 0 or i >= chessboard_size:
            continue
        for j in range(y - distance, y + distance + 1):
            if j < 0 or j >= chessboard_size:
                continue
            if i == x and j == y:
                continue
            if chessboard[i, j] != COLOR_NONE:
                cnt -= 1
                if cnt <= 0:
                    return True
    return False


def evaluate_point(x1, y1, player, d, chessboard):
    result = 0
    if player:
        target = COLOR_BLACK
        role = 1
    else:
        target = COLOR_WHITE
        role = 0
    if d < 0 or d == 0:
        cnt = 1
        cnt1 = 0
        empty = -1
        block = 0
        i = y1 + 1
        while True:
            if i >= chessboard_size:
                block += 1
                break
            if chessboard[x1, i] == COLOR_NONE:
                if empty == -1 and i < chessboard_size - 1:
                    if chessboard[x1, i + 1] == target:
                        empty = cnt
                        i += 1
                        continue
                    else:
                        break
                else:
                    break
            if chessboard[x1, i] == target:
                cnt += 1
                i += 1
                continue
            else:
                block += 1
                break
        i = y1 - 1
        while True:
            if i < 0:
                block += 1
                break
            if chessboard[x1, i] == COLOR_NONE:
                if empty == -1 and i > 0:
                    if chessboard[x1, i - 1] == target:
                        empty = 0
                        i -= 1
                        continue
                    else:
                        break
                else:
                    break
            if chessboard[x1, i] == target:
                cnt1 += 1
                if empty != -1:
                    empty += 1
                i -= 1
                continue
            else:
                block += 1
                break
        cnt += cnt1
        scoreboard_dir[x1, y1, 0, role] = check_score(cnt, empty, block)
    result += scoreboard_dir[x1, y1, 0, role]
    if d < 0 or d == 1:
        cnt = 1
        cnt1 = 0
        empty = -1
        block = 0
        i = x1 + 1
        while True:
            if i >= chessboard_size:
                block += 1
                break
            if chessboard[i, y1] == COLOR_NONE:
                if empty == -1 and i < chessboard_size - 1:
                    if chessboard[i + 1, y1] == target:
                        empty = cnt
                        i += 1
                        continue
                    else:
                        break
                else:
                    break
            if chessboard[i, y1] == target:
                cnt += 1
                i += 1
                continue
            else:
                block += 1
                break

        i = x1 - 1
        while True:
            if i < 0:
                block += 1
                break
            if chessboard[i, y1] == COLOR_NONE:
                if empty == -1 and i > 0:
                    if chessboard[i - 1, y1] == target:
                        empty = 0
                        i -= 1
                        continue
                    else:
                        break
                else:
                    break
            if chessboard[i, y1] == target:
                cnt1 += 1
                if empty != -1:
                    empty += 1
                i -= 1
                continue
            else:
                block += 1
                break
        cnt += cnt1
        scoreboard_dir[x1, y1, 1, role] = check_score(cnt, empty, block)
    result += scoreboard_dir[x1, y1, 1, role]
    if d < 0 or d == 2:
        cnt = 1
        cnt1 = 0
        empty = -1
        block = 0
        x = x1 + 1
        y = y1 + 1
        while True:
            if x >= chessboard_size or y >= chessboard_size:
                block += 1
                break
            if chessboard[x, y] == COLOR_NONE:
                if empty == -1 and x < chessboard_size - 1 and y < chessboard_size - 1:
                    if chessboard[x + 1, y + 1] == target:
                        empty = cnt
                        x += 1
                        y += 1
                        continue
                    else:
                        break
                else:
                    break
            if chessboard[x, y] == target:
                cnt += 1
                x += 1
                y += 1
                continue
            else:
                block += 1
                break

        x = x1 - 1
        y = y1 - 1
        while True:
            if x < 0 or y < 0:
                block += 1
                break
            if chessboard[x, y] == COLOR_NONE:
                if empty == -1 and x > 0 and y > 0:
                    if chessboard[x - 1, y - 1] == target:
                        empty = 0
                        x -= 1
                        y -= 1
                        continue
                    else:
                        break
                else:
                    break
            if chessboard[x, y] == target:
                cnt1 += 1
                if empty != -1:
                    empty += 1
                x -= 1
                y -= 1
                continue
            else:
                block += 1
                break
        cnt += cnt1
        scoreboard_dir[x1, y1, 2, role] = check_score(cnt, empty, block)
    result += scoreboard_dir[x1, y1, 2, role]
    if d < 0 or d == 3:
        cnt = 1
        cnt1 = 0
        empty = -1
        block = 0
        x = x1 + 1
        y = y1 - 1
        while True:
            if y < 0 or x >= chessboard_size:
                block += 1
                break
            if chessboard[x, y] == COLOR_NONE:
                if empty == -1 and x < chessboard_size - 1 and y > 0:
                    if chessboard[x + 1, y - 1] == target:
                        empty = cnt
                        x += 1
                        y -= 1
                        continue
                    else:
                        break
                else:
                    break
            if chessboard[x, y] == target:
                cnt += 1
                x += 1
                y -= 1
                continue
            else:
                block += 1
                break
        x = x1 - 1
        y = y1 + 1
        while True:
            if x < 0 or y >= chessboard_size:
                block += 1
                break
            if chessboard[x, y] == COLOR_NONE:
                if empty == -1 and x > 0 and y < chessboard_size - 1:
                    if chessboard[x - 1, y + 1] == target:
                        empty = 0
                        x -= 1
                        y += 1
                        continue
                    else:
                        break
                else:
                    break
            if chessboard[x, y] == target:
                cnt1 += 1
                if empty != -1:
                    empty += 1
                x -= 1
                y += 1
                continue
            else:
                block += 1
                break
        cnt += cnt1
        scoreboard_dir[x1, y1, 3, role] = check_score(cnt, empty, block)
    result += scoreboard_dir[x1, y1, 3, role]
    return result


def evaluate(player, chessboard):
    hum_max = 0
    com_max = 0
    for pos in chessSearch:
        if chessboard[pos[0], pos[1]] == COLOR_BLACK:
            hum_max += fixscore(hum_scoreboard[pos[0], pos[1]])
        elif chessboard[pos[0], pos[1]] == COLOR_WHITE:
            com_max += fixscore(com_scoreboard[pos[0], pos[1]])
    result = (-1 if player else 1) * (com_max - hum_max)
    return result


def check_score(cnt, empty, block):
    if empty <= 0:
        if cnt >= 5:
            return pattern_score["five"]
        if block == 0:
            if cnt == 1:
                return pattern_score["one"]
            elif cnt == 2:
                return pattern_score["two"]
            elif cnt == 3:
                return pattern_score["three"]
            elif cnt == 4:
                return pattern_score["four"]
        elif block == 1:
            if cnt == 1:
                return pattern_score["blocked_two"]
            elif cnt == 2:
                return pattern_score["blocked_two"]
            elif cnt == 3:
                return pattern_score["blocked_three"]
            elif cnt == 4:
                return pattern_score["blocked_four"]
    elif empty == 1 or empty == cnt - 1:
        if cnt >= 6:
            return pattern_score["five"]
        if block == 0:
            if cnt == 2:
                return pattern_score["two"] / 2
            elif cnt == 3:
                return pattern_score["three"]
            elif cnt == 4:
                return pattern_score["blocked_four"]
            elif cnt == 5:
                return pattern_score["four"]
        elif block == 1:
            if cnt == 2:
                return pattern_score["blocked_two"]
            elif cnt == 3:
                return pattern_score["blocked_three"]
            elif cnt == 4:
                return pattern_score["blocked_four"]
            elif cnt == 5:
                return pattern_score["blocked_four"]
    elif empty == 2 or empty == cnt - 2:
        if cnt >= 7:
            return pattern_score["five"]
        if block == 0:
            if cnt == 3:
                return pattern_score["three"]
            elif cnt == 5:
                return pattern_score["blocked_four"]
            elif cnt == 6:
                return pattern_score["four"]
        elif block == 1:
            if cnt == 3:
                return pattern_score["blocked_three"]
            elif cnt == 4:
                return pattern_score["blocked_four"]
            elif cnt == 5:
                return pattern_score["blocked_four"]
            elif cnt == 6:
                return pattern_score["four"]
        elif block == 2:
            if cnt == 6:
                return pattern_score["blocked_four"]
    elif empty == 3 or empty == cnt - 3:
        if cnt >= 8:
            return pattern_score["five"]
        if block == 0:
            if cnt == 5:
                return pattern_score["three"]
            elif cnt == 6:
                return pattern_score["blocked_four"]
            elif cnt == 7:
                return pattern_score["four"]
        elif block == 1:
            if cnt == 6:
                return pattern_score["blocked_four"]
            elif cnt == 7:
                return pattern_score["four"]
        elif block == 2:
            if cnt == 7:
                return pattern_score["blocked_four"]
    elif empty == 4 or empty == cnt - 4:
        if cnt >= 9:
            return pattern_score["five"]
        if block == 0:
            if cnt == 8:
                return pattern_score["four"]
        elif block == 1:
            if cnt == 7:
                return pattern_score["blocked_four"]
            elif cnt == 8:
                return pattern_score["four"]
        elif block == 2:
            if cnt == 8:
                return pattern_score["blocked_four"]
    elif empty == 5 or empty == cnt - 5:
        return pattern_score["five"]
    return 0


def add(x, y, color, chessboard):
    chessboard[x, y] = color


