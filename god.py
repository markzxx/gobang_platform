import imp
import numpy as np
# import cv2
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




    def first_chess(self):

        try:
            timeout(god.time_out)(self.black.first_chess)() #--------------------------------------------------------
        except Exception:
            pass

        if len(self.black.candidate_list)>0:
            pos = self.black.candidate_list[-1]
            self.finish = self.check_chess(pos,color=-1)

            if not self.finish:
                self.last_pos = pos
                self.chessboard[pos[0], pos[1]] = -1
                self.finish = self.judge(pos, -1)
            else:
                self.winner = 1
        else:
            self.error = self.error + "Dear " + str(self.color_user_map[-1]) + ' : your candidate list of chess is empty.\n'
            self.fail_step(color=-1)


    def update(self, color):
        pos = (-1,-1)
        tem_list = []

        if color ==1:
            try:
                timeout(god.time_out)(self.white.go)(self.last_pos)#--------------------------------------------------------
            except Exception:
                pass
            tem_list = self.white.candidate_list
        else:
            try:
                timeout(god.time_out)(self.black.go)(self.last_pos)#--------------------------------------------------------
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

        def get_chess(chess_pos_list):
            result = []
            for chess_pos in chess_pos_list:
                #print("pre",chess_pos)
                if chess_pos[0]>=0 and chess_pos[0]<self.chessboard_size and chess_pos[1]>=0 and chess_pos[1]<self.chessboard_size:
                    result.append(self.chessboard[chess_pos[0], chess_pos[1]])
                    #print("add", chess_pos)
            return result

        result = False
        if len(np.where(self.chessboard == 0)[0]) == 0:
            result = True
            self.winner = 0
        else:
            x, y = pos
            axis1 = get_chess([(x + i,y + i) for i in range(-5, 5)])
            axis2 = get_chess([(x - i,y + i) for i in range(-5, 5)])
            axis3 = get_chess([(x + i,y) for i in range(-5, 5)])
            axis4 = get_chess([(x,y + i) for i in range(-5, 5)])
            all_axis = [axis1, axis2, axis3, axis4]
            #print(all_axis)

            for axis in all_axis:
                count = 0
                for chess_color in axis:
                    if count == 5:
                        result = True
                        break
                    else:
                        if chess_color == color:
                            count += 1
                        else:
                            count = 0
                if result:
                    self.winner = color
                    break
        self.finish = result
        return result

    def fail_step(self, color):
        self.winner = -color
        self.finish = True

if __name__ == '__main__':

    socketIO = SocketIO('localhost', 8080, Namespace)

    '''
    win_name = 'test'
    cv2.namedWindow(win_name,0 )
    cv2.resizeWindow(win_name, 400,400)
    def see(array):
        image = np.zeros((array.shape[0], array.shape[1]),dtype=np.uint8)
        idx0 = np.where(array==0)
        idx1 = np.where(array==1)
        image[idx0] = 125
        image[idx1] = 255
        cv2.imshow(win_name, image)
        cv2.waitKey(1000)
    '''
    arg_list = sys.argv
    color_map = {-1:1, 1:0}
    file_dic = arg_list[1]
    white_path = file_dic+'/'+arg_list[2]+'.py'#'./test_AI.py'
    black_path = file_dic+'/'+arg_list[3]+'.py'#'./test_AI.py'
    size = int(arg_list[4])
    time_interval = float(arg_list[5])

    god = God(white_path ,black_path ,size , time_interval)

    begin_data = god.begin
    go_data = [begin_data[0], begin_data[1], -1, -1, 0]

    god.first_chess()
    go_data[2] = god.last_pos[0]
    go_data[3] = god.last_pos[1]
    go_data[4] = color_map[-1]
    socketIO.emit("go", go_data)
    socketIO.wait(seconds=1)
    #print(go_data)

    #see(god.chessboard)
    while not god.finish:
        god.update(color= 1)
        if god.finish: break
        go_data[2] = god.last_pos[0]
        go_data[3] = god.last_pos[1]
        go_data[4] = color_map[1]
        socketIO.emit("go", go_data)
        socketIO.wait(seconds=1)
        #print(go_data)
        #see(god.chessboard)

        god.update( color=-1)
        if god.finish: break
        go_data[2] = god.last_pos[0]
        go_data[3] = god.last_pos[1]
        go_data[4] = color_map[-1]
        socketIO.emit("go", go_data)
        socketIO.wait(seconds=1)
        #print(go_data)
        #see(god.chessboard)

    god.end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    if god.error:
        error_data = (begin_data[0], begin_data[1], god.error)
        socketIO.emit("error", error_data)
        socketIO.wait(seconds=1)
        #print(error_data)

    finish_data = (begin_data[0], begin_data[1], god.start_time, god.end_time, god.color_user_map[god.winner], god.color_user_map[-god.winner])
    socketIO.emit("finish", finish_data)
    socketIO.wait(seconds=1)
    #print(finish_data)

    #see(god.chessboard)




