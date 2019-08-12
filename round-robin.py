import asyncio
import aiomysql
import subprocess
import numpy as np
from socketIO_client import SocketIO, BaseNamespace

concurrency_num = 10
send = 0
rev = 0
game_log = {}
gaming_set = set()
pool = None
loop = asyncio.get_event_loop()

class Namespace(BaseNamespace):
    def on_connect(selpif):
        print ('[Connected]')
    def on_finish(selpif, data):
        global total_game
        total_game += 1
        print('finish', data, 'total game:', total_game)
        game_log[data['white']].add(data['black'])
        gaming_set.remove(data['white'])
        gaming_set.remove(data['black'])
        start_new_game()
            
async def init_pool ():
    global pool
    pool = await aiomysql.create_pool(host='10.20.96.148', port=3307, user='chess', password='chess123456', db='chess', loop=loop, autocommit=True, minsize=1, maxsize=100)

async def clear():
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("update users set last_update = null")
            print('clear')
            
async def get_list():
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("select sid from users where last_update is not null ")
            return await cursor.fetchall()

async def get_game_log():
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("select white_sid, black_sid from game_log where start_time>'2018-10-27 16:00:00' and end_time is not null ")
            return await cursor.fetchall()

def start_new_game():
    while True:
        white, black = game_list.pop()
        if black in game_log[white] or white == black:
            continue
        if white in gaming_set or black in gaming_set:
            game_list.insert(0, (white, black))
        else:
            gaming_set.add(white)
            gaming_set.add(black)
            socketIO.emit('round_play', {'player1': white, 'player2': black, 'tag': 1})
            break

loop.run_until_complete(init_pool())

# with open('students.txt', 'r') as f:
#     lines = f.readlines()
#     for sid in lines:
#         print(sid)
#         wait = subprocess.Popen("python code_check_test.py tem_code {}".format(sid), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#         wait.wait()

socketIO = SocketIO('10.20.96.148', 8080, Namespace)

all_user = loop.run_until_complete(get_list())
players = [i[0] for i in all_user]
for player in players:
    game_log[player] = set()

all_game = loop.run_until_complete(get_game_log())
total_game = len(all_game)
for game in all_game:
    game_log[game[0]].add(game[1])

game_list = []
for i in players:
    for j in players:
        game_list.append((i, j))
np.random.shuffle(game_list)
for i in range(concurrency_num):
    start_new_game()


socketIO.wait()