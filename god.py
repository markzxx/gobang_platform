import imp
import numpy as np
from timeout_decorator import timeout
import time
import sys
import resource
import traceback
import timeout_decorator
from socketIO_client import SocketIO, BaseNamespace
import os

class Namespace(BaseNamespace):
    def on_connect(selpif):
        print ('[Connected]')
        
    def on_self_go (selpif, data):
        god.self_update(data[0], data[1], data[2])
        if not god.finish:
            god.update(-data[2])
            if not god.error:
                go_data = [god.player, god.last_pos[0], god.last_pos[1], -data[2]]
                socketIO.emit("go", deal_go_data(go_data))
        if god.finish:
            if god.error:
                error_data = (god.player, god.error)
                socketIO.emit("error", error_data)
            finish_data = (god.player, god.color_user_map[god.winner], god.color_user_map[-god.winner])
            socketIO.emit("self_finish", finish_data)
            socketIO.wait(seconds=1)
            socketIO.disconnect()

def limit_memory(maxsize):
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (maxsize, hard))

def check_chess_board(chessboard,chessboard_size,pos,color):
    winner = 0
    def get_chess(chess_pos_list, size):
        pos_list = []
        for chess_pos in chess_pos_list:
            # print("pre",chess_pos)
            if chess_pos[0] >= 0 and chess_pos[0] < size and chess_pos[1] >= 0 and chess_pos[1] < size:
                pos_list.append(chess_pos)
        return pos_list

    result = False
    if len(np.where(chessboard == 0)[0]) == 0:
        result = True
        winner = 0
    else:
        x, y = pos
        axis1 = get_chess([(x + i, y + i) for i in range(-4, 5)], chessboard_size)
        axis2 = get_chess([(x - i, y + i) for i in range(-4, 5)], chessboard_size)
        axis3 = get_chess([(x + i, y) for i in range(-4, 5)], chessboard_size)
        axis4 = get_chess([(x, y + i) for i in range(-4, 5)], chessboard_size)
        all_axis = [axis1, axis2, axis3, axis4]
        all_pos_list = axis1 + axis2 + axis3 + axis4
        # print(all_axis)
        canvas = np.ones_like(chessboard, dtype=np.uint8)
        canvas = canvas * 125

        for axis in all_axis:

            count = 0
            for chess_pos in axis:

                if chessboard[chess_pos[0], chess_pos[1]] == color:
                    count += 1
                else:
                    count = 0
                if count == 5:
                    result = True
                    #print(count, result)
                    break

            if result:
                winner = color
                break
    return result, winner

class God(object):
    def __init__(self, file_dic, player, white, black, chessboard_size, time_out):

        self.chessboard_size = chessboard_size
        self.time_out = time_out
        self.chessboard = np.zeros((chessboard_size, chessboard_size), dtype=np.int)
        self.finish = False
        self.winner = 0
        self.last_pos = (-1, -1)
        self.player = player
        white_path = os.path.join(file_dic, white + '.py')
        black_path = os.path.join(file_dic, black + '.py')
        if white != 'human':
            self.white = imp.load_source('AI', white_path).AI(self.chessboard_size, 1, self.time_out)
        if black != 'human':
            self.black = imp.load_source('AI', black_path).AI(self.chessboard_size, -1, self.time_out)
        self.user_color_map = {white: 1, black: -1}
        self.color_user_map = {1: white, -1: black, 0: 0}
        self.error = ""


    def check_chess(self,pos, color):
        if pos[0]<0 or pos[0]>=self.chessboard_size or pos[1]<0 or pos[1]>=self.chessboard_size:
            self.error = self.error +"Dear "+str(self.color_user_map[color])+ ' : your postion of last chess is out of bound.\n'
            self.finish = True
            return True

        if self.chessboard[pos[0], pos[1]]!=0:
            self.error = self.error + "Dear " + str(self.color_user_map[color]) + ' : your postion of last chess is not empty.\n'
            self.finish = True
            return True

    def self_update(self, x, y, color):
        pos = (x, y)
        self.last_pos = pos
        assert self.chessboard[pos[0], pos[1]] == 0
        self.chessboard[pos[0], pos[1]] = color
        self.finish = self.judge(pos, color)
        if god.finish:
            self.winner = color
            
    def update(self, color):
        assert self.chessboard.all()<2 and self.chessboard.all()>-2

        if color == 1:
            try:
                timeout(self.time_out)(self.white.go)(self.chessboard)#timeout(god.time_out)(self.white.go)(self.last_pos)#--------------------------------------------------------
            except MemoryError:
                memory_error = traceback.format_exc()
                self.memory_fail(memory_error)
                return ''
            except timeout_decorator.timeout_decorator.TimeoutError:
                pass
            tem_list = self.white.candidate_list
        else:
            try:
                timeout(self.time_out)(self.black.go)(self.chessboard)#timeout(god.time_out)(self.black.go)(self.last_pos)#--------------------------------------------------------
            except MemoryError:
                memory_error = traceback.format_exc()
                self.memory_fail(memory_error)
                return ''
            except timeout_decorator.timeout_decorator.TimeoutError:
                pass
            tem_list = self.black.candidate_list

        if len(tem_list)>0:
            pos = tem_list[-1]
            self.finish = self.check_chess(pos, color)
            if not self.finish:
                self.last_pos = pos
                assert self.chessboard[pos[0], pos[1]] == 0
                self.chessboard[pos[0], pos[1]] = color
                self.finish = self.judge(pos, color)
            else:
                self.winner = -color
        else:
            self.error = self.error + "Dear " + str(self.color_user_map[color]) + ' : your candidate list of chess is empty.\n'
            self.fail_step(color=color)


    def judge(self, pos, color):

        if len(np.where(self.chessboard == 0)[0]) == 0:
            result = True
            self.winner = 0
        else:
            result, winner = check_chess_board(self.chessboard, self.chessboard_size, pos, color)
            self.finish = result
            self.winner = winner
        return result

    def fail_step(self, color):
        self.winner = -color
        self.finish = True

    def memory_fail(self, message):
        self.finish = True
        p1 = str(self.color_user_map[-1])
        p2 = str(self.color_user_map[1])
        wrong_play = ''
        winner_play = ''
        if p1 in message and p2 not in message:
            wrong_play = p1
            winner_play = p2
        elif p2 in message and p1 not in message:
            wrong_play = p2
            winner_play = p1
        elif p2 not in message and p1 not in message:
            self.error+= " Memory error message error in trackback MemoryError"
        else:
            self.error +=" Other error in trackback MemoryError"

        if wrong_play or winner_play:
            assert winner_play and wrong_play
            self.error += " Dear " + wrong_play + ": Memory out"
            self.winner = self.user_color_map[winner_play]

def self_fight(file_dic, white, black, size, time_interval, player):
    global god
    god = God(file_dic, player, white, black, size, time_interval)

    begin_data = player
    
    AI_color = 1 if white != 'human' else -1
    socketIO.emit("self_register", player)
    
    if AI_color == -1:
        #Black chess go first step
        god.update(AI_color)
        if not god.finish:
            go_data = [begin_data, god.last_pos[0], god.last_pos[1], AI_color]
            socketIO.emit("go", deal_go_data(go_data))
    
    if god.error:
        error_data = (begin_data, god.error)
        socketIO.emit("error", error_data)
        finish_data = (begin_data, god.color_user_map[god.winner], god.color_user_map[-god.winner])
        socketIO.emit("finish", finish_data)
        # print(error_data)
        

def fight(file_dic, white, black, size, time_interval, player):
    god = God(file_dic, player, white, black, size, time_interval)

    #begin_data = god.begin
    begin_data = player

    tem_color = -1
    while not god.finish:
        tem_color = -1
        god.update(color=tem_color)
        if god.finish: break
        go_data = [begin_data, god.last_pos[0], god.last_pos[1], tem_color]
        socketIO.emit("go", deal_go_data(go_data))
        #print(go_data)

        tem_color = 1
        god.update(color=tem_color)
        if god.finish: break
        go_data = [begin_data, god.last_pos[0], god.last_pos[1], tem_color]
        socketIO.emit("go", deal_go_data(go_data))
        #print(go_data)

    if god.error:
        error_data = (begin_data, god.error)
        socketIO.emit("error", error_data)
        #print(error_data)
    else:
        go_data = [begin_data, god.last_pos[0], god.last_pos[1], tem_color]
        #print(go_data)
        socketIO.emit("go", deal_go_data(go_data))

    finish_data = (begin_data, god.color_user_map[god.winner], god.color_user_map[-god.winner])
    socketIO.emit("finish", finish_data)



if __name__ == '__main__':
    def deal_go_data(go_data):
        for i in range(1,4):
            go_data[i] = int(go_data[i])
        return go_data

    socketIO = SocketIO('localhost', 8080, Namespace)

    arg_list = sys.argv
    file_dic = arg_list[1]
    white = arg_list[2]
    black = arg_list[3]
    size = int(arg_list[4])
    time_interval = float(arg_list[5])
    player = arg_list[6]

    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    
    memory_size = 10*1024**2 # In bytes
    limit_memory(memory_size)

    try:
        if white == 'human' or black == 'human':
            self_fight(file_dic, white, black, size, time_interval, player)
        else:
            fight(file_dic, white, black, size, time_interval, player)

    except Exception:
        socketIO.emit("error", [player, traceback.format_exc()])
        finish_data = (player, 0, 0)
        socketIO.emit("finish", finish_data)

    socketIO.wait(seconds=200)








