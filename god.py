import imp
import numpy as np
from timeout_decorator import timeout
import time
import sys

from socketIO_client import SocketIO, BaseNamespace

class Namespace(BaseNamespace):
    def on_connect(selpif):
        print ('[Connected]')

    def on_reply (selpif, data):
        for d in data:
            print(d)


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
    def __init__(self, white_path, black_path, chessboard_size, time_out):

        self.chessboard_size = chessboard_size
        self.time_out = time_out
        self.chessboard = np.zeros((chessboard_size, chessboard_size), dtype=np.int)
        self.finish = False
        self.winner = 0
        self.last_pos = (-1,-1)
        self.white = imp.load_source('AI', white_path).AI(self.chessboard_size, 1, self.time_out)
        self.black = imp.load_source('AI', black_path).AI(self.chessboard_size, -1, self.time_out)
        self.user_color_map = {white_path.split("/")[-1].split(".")[0]: 1, black_path.split("/")[-1].split(".")[0]: -1}
        self.color_user_map = {1: int(white_path.split("/")[-1].split(".")[0]), -1: int(black_path.split("/")[-1].split(".")[0]), 0: 0}
        self.start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.end_time = -1
        self.begin = (self.color_user_map[1], self.color_user_map[-1])
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


    def update(self, color):
        assert self.chessboard.all()<2 and self.chessboard.all()>-2
        pos = (-1,-1)
        tem_list = []

        if color ==1:
            try:
                timeout(self.time_out)(self.white.go)(self.chessboard)#timeout(god.time_out)(self.white.go)(self.last_pos)#--------------------------------------------------------
            except Exception:
                pass
            tem_list = self.white.candidate_list
        else:
            try:
                timeout(self.time_out)(self.black.go)(self.chessboard)#timeout(god.time_out)(self.black.go)(self.last_pos)#--------------------------------------------------------
            except Exception:
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

if __name__ == '__main__':
    def deal_go_data(go_data):
        for i in range(2,5):
            go_data[i] = int(go_data[i])
        return go_data

    socketIO = SocketIO('localhost', 8080, Namespace)


    arg_list = sys.argv
    color_map = {-1:1, 1:0}
    file_dic = arg_list[1]
    white_path = file_dic+'/'+arg_list[2]+'.py'#'./11610999.py'
    black_path = file_dic+'/'+arg_list[3]+'.py'#'./11610999.py'
    size = int(arg_list[4])
    time_interval = float(arg_list[5])
    player = int(arg_list[6])

    god = God(white_path, black_path, size, time_interval)

    #begin_data = god.begin
    begin_data = (player,0)
    go_data = [begin_data[0], begin_data[1], -1, -1, 0]


    #print(go_data)

    tem_color = -1
    while not god.finish:
        tem_color = -1
        god.update(color=tem_color)
        if god.finish: break
        go_data[2] = god.last_pos[0]
        go_data[3] = god.last_pos[1]
        go_data[4] = color_map[tem_color]
        socketIO.emit("go", deal_go_data(go_data))
        #print(go_data)


        tem_color = 1
        god.update(color=tem_color)
        if god.finish: break
        go_data[2] = god.last_pos[0]
        go_data[3] = god.last_pos[1]
        go_data[4] = color_map[tem_color]
        socketIO.emit("go", deal_go_data(go_data))
        #print(go_data)


    god.end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    if god.error:
        error_data = (begin_data[0], begin_data[1], god.error)
        socketIO.emit("error", error_data)
        #print(error_data)
    else:
        go_data[2] = god.last_pos[0]
        go_data[3] = god.last_pos[1]
        go_data[4] = color_map[tem_color]
        #print(go_data)

        socketIO.emit("go", deal_go_data(go_data))

    finish_data = (begin_data[0], begin_data[1], god.start_time, god.end_time, god.color_user_map[god.winner],
                   god.color_user_map[-god.winner])
    socketIO.emit("finish", finish_data)
    #print(finish_data)

    time.sleep(1)





