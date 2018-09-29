import ctypes
import imp
import inspect
import os
import signal
import sys
import threading
import time
import traceback

import numpy as np
import psutil
import timeout_decorator
from socketIO_client import SocketIO, BaseNamespace
from timeout_decorator import timeout

player_now=[0]

player_memory = {1: 0, -1: 0}




def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def get_mem():
    return psutil.Process(os.getpid()).memory_info().rss/(1024**2)


def deal_with_memory_out(size):
    white_mem = player_memory[1]
    black_mem = player_memory[-1]
    winner = 0
    failer = 0
    memory_message = ''
    if size>2*memory_size:
        winner = god.color_user_map[-player_now[0]]
        failer = god.color_user_map[player_now[0]]
        memory_message = 'Dear ' + str(failer) + ": You may get memory out with more than " + str(
            memory_size) + " MB."

    else:
        if black_mem > memory_size:
            winner = god.color_user_map[1]
            failer = god.color_user_map[-1]
            memory_message = 'Dear ' + str(failer) + ": You may get memory out with more than " + str(
                memory_size) + " MB."
            # print("winner: ",god.color_user_map[1])
        elif white_mem > memory_size:
            winner = god.color_user_map[-1]
            failer = god.color_user_map[1]
            memory_message = 'Dear ' + str(failer) + ": You may get memory out with more than " + str(
                memory_size) + " MB."
            # print("winner: ",god.color_user_map[-1])
        else:
            memory_message = 'Dear ' + str(god.color_user_map[1]) + " and " + str(
                god.color_user_map[-1]) + ": You may get memory out together." + "\n " + str(
                god.color_user_map[1]) + " use " + str(int(white_mem)) + " MB.\n " + str(
                god.color_user_map[-1]) + " use " + str(int(black_mem)) + " MB."
            # print("winner: ",god.color_user_map[0])

    finish_data = begin_data + [winner, failer]
    socketIO.emit("error", [player, memory_message])
    socketIO.emit("finish", finish_data)
    socketIO.wait(seconds=1)
    socketIO.disconnect()



def control():
    judge = True
    while judge:
        size = get_mem()
        if size > 2*memory_size or player_memory[1]>memory_size or player_memory[-1]>memory_size:
            deal_with_memory_out(size)
            my_pid = os.getpid()
            os.kill(my_pid, signal.SIGKILL)
            judge = False
        time.sleep(0.1)


class Namespace(BaseNamespace):
    def on_connect(selpif):
        print ('[Connected]')

    def on_finish (selpif, data):
        socketIO.disconnect()
        
    def on_self_go (selpif, data):
        god.self_update(data[0], data[1], data[2])
        if not god.finish:
            god.update(-data[2])
            if not god.error:
                go_data = god.begin + deal_go_data([god.last_pos[0], god.last_pos[1], -data[2]])
                socketIO.emit("go", go_data)
        if god.finish:
            if god.error:
                error_data = god.begin + [god.error]
                socketIO.emit("error", error_data)
            finish_data = god.begin + [god.color_user_map[god.winner], god.color_user_map[-god.winner]]
            socketIO.emit("self_finish", finish_data)
            socketIO.wait(seconds=1)
            socketIO.disconnect()

class God(object):
    def __init__ (self, file_dic, player, tag, white, black, chessboard_size, time_out):
    
        self.error = ""
        self.chessboard_size = chessboard_size
        self.time_out = time_out
        self.chessboard = np.zeros((chessboard_size, chessboard_size), dtype=np.int)
        self.finish = False
        self.winner = 0
        self.last_pos = (-1, -1)
        self.player = player
        self.tag = tag
        self.begin = [player, tag]
        white_path = os.path.join(file_dic, white + '.py')
        black_path = os.path.join(file_dic, black + '.py')
        try:
            if 'human' not in white:
                self.white = imp.load_source('AI', white_path).AI(self.chessboard_size, 1, self.time_out)
        except Exception:
            self.finish = True
            self.error = traceback.format_exc()
            self.winner = -1
    
        try:
            if 'human' not in black:
                self.black = imp.load_source('AI', black_path).AI(self.chessboard_size, -1, self.time_out)
        except Exception:
            self.finish = True
            self.error = traceback.format_exc()
            self.winner = 1
        self.user_color_map = {white: 1, black: -1}
        self.color_user_map = {1: white, -1: black, 0: 0}

    def check_chess(self, pos, color):
        if pos[0]<0 or pos[0]>=self.chessboard_size or pos[1]<0 or pos[1]>=self.chessboard_size:
            self.error = self.error +"Dear "+str(self.color_user_map[color])+ ' : your postion of last chess is out of bound.\n'
            self.finish = True
            return True

        if self.chessboard[pos[0], pos[1]] != 0:
            self.error = self.error + "Dear " + str(self.color_user_map[color]) + ' : your postion of last chess is not empty.\n'
            self.finish = True
            return True

    def check_chess_board (self, pos, color):
        def get_chess (chess_pos_list, size):
            pos_list = []
            for chess_pos in chess_pos_list:
                # print("pre",chess_pos)
                if chess_pos[0] >= 0 and chess_pos[0] < size and chess_pos[1] >= 0 and chess_pos[1] < size:
                    pos_list.append(chess_pos)
            return pos_list
    
        x, y = pos
        axis1 = get_chess([(x + i, y + i) for i in range(-4, 5)], self.chessboard_size)
        axis2 = get_chess([(x - i, y + i) for i in range(-4, 5)], self.chessboard_size)
        axis3 = get_chess([(x + i, y) for i in range(-4, 5)], self.chessboard_size)
        axis4 = get_chess([(x, y + i) for i in range(-4, 5)], self.chessboard_size)
        all_axis = [axis1, axis2, axis3, axis4]
        # all_pos_list = axis1 + axis2 + axis3 + axis4
        # print(all_axis)
        # canvas = np.ones_like(chessboard, dtype=np.uint8)
        # canvas = canvas * 125
        for axis in all_axis:
            count = 0
            for chess_pos in axis:
            
                if self.chessboard[chess_pos[0], chess_pos[1]] == color:
                    count += 1
                else:
                    count = 0
                # print('count', count, pos, color, chess_pos, chessboard[chess_pos[0], chess_pos[1]])
                if count == 5:
                    self.finish = True
                    self.winner = color
                    return
    
        if len(np.where(self.chessboard == 0)[0]) == 0:
            self.finish = True
            self.winner = 0

    def self_update(self, x, y, color):
        pos = (x, y)
        color = int(color)
        self.last_pos = pos
        assert self.chessboard[x, y] == 0
        self.chessboard[x, y] = color
        self.check_chess_board(pos, color)
        
    def update(self, color):
        assert self.chessboard.all()<2 and self.chessboard.all()>-2

        if color == 1:
            try:
                timeout(self.time_out)(self.white.go)(np.copy(self.chessboard))#timeout(god.time_out)(self.white.go)(self.last_pos)#--------------------------------------------------------
            except MemoryError:
                memory_error = traceback.format_exc()
                self.memory_fail(memory_error)
                return ''
            except timeout_decorator.timeout_decorator.TimeoutError:
                pass
            except Exception:
                self.fail_step(color=color)
                god.error = traceback.format_exc()
            tem_list = self.white.candidate_list
        else:
            try:
                timeout(self.time_out)(self.black.go)(np.copy(self.chessboard))#timeout(god.time_out)(self.black.go)(self.last_pos)#--------------------------------------------------------
            except MemoryError:
                memory_error = traceback.format_exc()
                self.memory_fail(memory_error)
                return ''
            except timeout_decorator.timeout_decorator.TimeoutError:
                pass
            except Exception:
                self.fail_step(color=color)
                god.error = traceback.format_exc()
            tem_list = self.black.candidate_list

        if len(tem_list) > 0:
            pos = tem_list[-1]
            self.check_chess(pos, color)
            if not self.finish:
                self.last_pos = pos
                assert self.chessboard[pos[0], pos[1]] == 0
                self.chessboard[pos[0], pos[1]] = color
                self.check_chess_board(pos, color)
            else:
                self.winner = -color
        else:
            self.error = self.error + "Dear " + str(self.color_user_map[color]) + ' : your candidate list of chess is empty.\n'
            self.fail_step(color=color)

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


def self_fight (first, begin_data):
    if first:
        #Black chess go first step
        god.update(-1)
        if not god.finish:
            go_data = begin_data + deal_go_data([god.last_pos[0], god.last_pos[1], -1])
            socketIO.emit("go", go_data)
    
    if god.error:
        error_data = begin_data + [god.error]
        socketIO.emit("error", error_data)
        finish_data = begin_data + [god.color_user_map[god.winner], god.color_user_map[-god.winner]]
        socketIO.emit("self_finish", finish_data)
        # print(error_data)


def fight (begin_data):
    while True:
        #--------------------------------
        tem_color = -1
        player_now[0] = tem_color

        memory_usage = get_mem()
        tem_mem = player_memory[tem_color]

        god.update(color=tem_color)

        after_step_memory = get_mem()
        player_memory[tem_color] = tem_mem + after_step_memory - memory_usage

        if god.finish: break
        go_data = begin_data + deal_go_data([god.last_pos[0], god.last_pos[1], tem_color])
        socketIO.emit("go", go_data)
        #print(go_data)

        #--------------------------------
        tem_color = 1
        player_now[0] = tem_color

        memory_usage = get_mem()
        tem_mem = player_memory[tem_color]

        god.update(color=tem_color)

        after_step_memory = get_mem()
        player_memory[tem_color] = tem_mem + after_step_memory - memory_usage

        if god.finish: break
        go_data = begin_data + deal_go_data([god.last_pos[0], god.last_pos[1], tem_color])
        socketIO.emit("go", go_data)
        #print(go_data)

    if god.error:
        error_data = begin_data + [god.error]
        socketIO.emit("error", error_data)
        #print(error_data)
    else:
        go_data = begin_data + deal_go_data([god.last_pos[0], god.last_pos[1], tem_color])
        #print(go_data)
        socketIO.emit("go", go_data)
    
    finish_data = begin_data + [god.color_user_map[god.winner], god.color_user_map[-god.winner]]
    socketIO.emit("finish", finish_data)



if __name__ == '__main__':
    def deal_go_data(go_data):
        for i, g in enumerate(go_data):
            go_data[i] = int(g)
        return go_data

    socketIO = SocketIO('localhost', 8080, Namespace)
    sys.stdout = open(os.devnull, 'w')
    arg_list = sys.argv
    file_dic = arg_list[1]
    white = arg_list[2]
    black = arg_list[3]
    size = int(arg_list[4])
    time_interval = float(arg_list[5])
    player = arg_list[6]
    tag = arg_list[7]

    memory_size = 100 * 1024 ** 2  # In bytes
    god = God(file_dic, player, tag, white, black, size, time_interval)
    begin_data = [player, tag]

    try:
        if 'human' in white or 'human' in black:
            first = False if 'human' in black else True
            socketIO.emit("self_register", begin_data)
            self_fight(first, begin_data)
        else:
            control_thread = threading.Thread(target=control)
            control_thread.start()
            fight(begin_data)


    except Exception:
        socketIO.emit("error", begin_data + [traceback.format_exc()])
        finish_data = begin_data + [0, 0]
        socketIO.emit("finish", finish_data)

    if god.finish:
        while True:
            try:
                stop_thread(control_thread)
                break
            except Exception:
                print(traceback.format_exc())
        socketIO.disconnect()

    socketIO.wait(seconds=600)
