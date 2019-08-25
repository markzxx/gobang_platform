import asyncio
import base64
import hashlib
import os
import random
import subprocess
from asyncio import sleep
from collections import defaultdict

import aiohttp_jinja2
import jinja2
import socketio
from aiohttp import web
from aiohttp_session import setup, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet

import config, mail
from mysqlapi import *

pool = None
verify_map = {}
downinfo = {'can_play': True, 'can_upload': True, 'message': "All race finish. Platform is close now."}


class Http_handler:
    @aiohttp_jinja2.template('index.html')
    async def index(self, request):
        session = await get_session(request)
        if 'sid' in session:
            return {'sid': session['sid']}
        else:
            session['sid'] = "test1"  # 测试
            return {'sid': session['sid']}
            raise web.HTTPFound('/login')

    @aiohttp_jinja2.template('login.html')
    async def logout(self, request):
        session = await get_session(request)
        if 'sid' in session:
            del session['sid']
        return {}

    @aiohttp_jinja2.template('login.html')
    async def login(self, request):
        if request._method == "GET":
            return {}
        session = await get_session(request)
        data = await request.post()
        user = await get_user(pool, data['sid'])
        if not user:
            return {'error': "Student Id not exist"}
        elif user['password'] != data['pwd']:
            return {'error': "Password wrong"}
        else:
            if data['pwd'] == str(hashlib.md5('123'.encode()).hexdigest()):
                return {'error': "Cannot use init password, please reset it."}
            else:
                session['sid'] = data['sid']
                raise web.HTTPFound('/')

    async def send_email(self, request):
        data = await request.post()
        sid = data['sid']
        user = await get_user(pool, data['sid'])
        if not user:
            return web.Response(text="Error: StudentId not exist")
        verify_code = str(random.randint(100000, 1000000))
        verify_map[sid] = verify_code
        await mail.send_verify_code(sid, verify_code)
        return web.Response(text="ok, please check your student email.")

    @aiohttp_jinja2.template('resetpwd.html')
    async def resetpwd(self, request):
        if request._method == "GET":
            return {}
        data = await request.post()
        user = await get_user(pool, data['sid'])
        if not user:
            return {'error': "Error: StudentId not exist."}
        if data['sid'] in verify_map and data['verify_code'] == verify_map[data['sid']]:
            await set_pwd(pool, data['sid'], data['newpwd'])
            del verify_map[data['sid']]
        else:
            return {'error': "Error: Wrong verify code."}
        raise web.HTTPFound('/login')

    async def upload(self, request):
        session = await get_session(request)
        if 'sid' not in session:
            raise web.HTTPFound('/login')
        sid = session['sid']
        if not downinfo['can_upload']:
            await upload_test(0, {'sid': sid, 'info': downinfo['message'], 'is_pass': False})
            return {}
        reader = await request.multipart()
        field = await reader.next()
        assert field.name == 'code'
        size = 0
        if not os.path.exists("user_code/"):
            os.mkdir("user_code/")
        if not os.path.exists("tem_code/"):
            os.mkdir("tem_code/")
        with open(os.path.join('tem_code/{}.py'.format(sid)), 'wb') as f:
            while True:
                chunk = await field.read_chunk()
                if not chunk:
                    break
                size += len(chunk)
                f.write(chunk)
                if size > config.MAX_CODE_SIZE:
                    return {'sid': sid, 'error': "Your code can not excess 1M."}

        # test code
        subprocess.Popen("python code_check.py tem_code {}".format(sid), stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, shell=True)
        raise web.HTTPFound('/')

    @aiohttp_jinja2.template('full_rank.html')
    async def full_rank(self, request):
        return {'rank': rank_info}

    @aiohttp_jinja2.template('rank.html')
    async def rank(self, request):
        return {'rank': rank_info}


sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('template'))

handler = Http_handler()
app.router.add_static('/static', 'template')
app.add_routes([web.get('/', handler.index, name='index'),
                web.get('/login', handler.login, name='login'),
                web.post('/login', handler.login, name='login'),
                web.get('/logout', handler.logout, name='logout'),
                web.get('/full_rank', handler.full_rank, name='full_rank'),
                web.get('/rank', handler.rank, name='rank'),
                web.post('/upload', handler.upload, name='upload'),
                web.post('/resetpwd', handler.resetpwd, name='reset'),
                web.post('/send_email', handler.send_email, name='send_email')])
fernet_key = fernet.Fernet.generate_key()
secret_key = base64.urlsafe_b64decode(fernet_key)
setup(app, EncryptedCookieStorage(secret_key))

rank_info = []
score_info = {}
max_game_id = 0
rounder = None
games = defaultdict(dict)
watching_room = set()
players = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))


def score(row):
    sid = row[0]
    score_info = row[1] * 10 - row[2] * 10
    return {'score': score_info, 'rand': random.random(), 'sid': sid}


def find_rank(sid):
    idx = -1
    for i, info in enumerate(rank_info):
        if sid == info['sid']:
            idx = i
            break
    return idx


async def push_game(player, tag, soid=None):
    if soid or ((player + str(tag)) in watching_room):
        await sio.emit('push_game', games[players[player][tag]['id']], room=soid if soid else player + str(tag))


@sio.on('connect')
async def connect(soid, environ):
    print("connect ", soid)


@sio.on('message')
async def message(soid, msg):
    print(soid, "msg ", msg)


@sio.on('upload_test')
async def upload_test(soid, data):
    sid, info, is_pass = str(data['sid']), data['info'], int(data['is_pass'])
    print(data)
    if is_pass:
        subprocess.Popen('mv tem_code/{}.py user_code/{}.py'.format(sid, sid), shell=True)
        row = await get_user(pool, sid)
        await set_update_time(pool, sid, int(row['update_times'])+1)
        if int(row['update_times'])==0:
            global score_info
            score_info[sid]['score'] = -10
        await update_all_list()
    # 发送测试结果推送
    await sio.emit('error', {'type': 3, 'info': info}, room=sid + str(1))
    await sio.emit('error', {'type': 3, 'info': info}, room=sid + str(-1))


@sio.on('watch')
async def watch(soid, data):
    player = str(data['player'])
    tag = int(data['tag'])
    new_room = player + str(tag)
    while len(sio.rooms(soid)) > 1:
        old_room = sio.rooms(soid)[1]
        sio.leave_room(soid, old_room)
        if old_room in watching_room:
            watching_room.remove(old_room)
    sio.enter_room(soid, new_room)
    watching_room.add(new_room)
    await push_game(player, tag)


@sio.on('self_play')
async def self_play(soid, data):
    if not downinfo['can_play']:
        await sio.emit('error', {'type': 3, 'info': downinfo['message']}, soid)
        return
    player = str(data['player'])
    AI = str(data['AI'])
    tag = int(data['tag'])
    print(player, 'self_play', AI)
    if players[player][tag]['status'] and players[player][tag]['id'] >= 10 ** 10:
        await error_finish(soid, {'player': player, 'tag': tag, 'new_game': 1})

    idx = find_rank(AI)
    if rank_info[idx]['score'] == -20:
        await sio.emit('error', {'type': 3, 'info': "This code has error."}, soid)
        return
    if tag > 0:
        await self_begin(player, tag, AI, 'human-' + player)
    else:
        await self_begin(player, tag, 'human-' + player, AI)


async def self_begin(player, tag, white, black):
    old_game_id = players[player][tag]['id']
    if old_game_id in games:
        del games[old_game_id]

    game_id = 10 ** 10
    while game_id in games:
        game_id = random.randint(10 ** 10, 2 * 10 ** 10)
    players[player][tag]['id'] = game_id
    players[player][tag]['status'] = 1
    games[game_id] = {'white': white, 'black': black, "chess_log": [], 'game_id': game_id, "type": 2}
    await push_game(player, tag)
    print(white, black, player, tag)
    subprocess.Popen('python god.py user_code {} {} {} {} {} {} 0'.format(white, black, 15, 1, player, tag),
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)


@sio.on('self_register')
async def self_register(soid, data):
    player = str(data[0])
    tag = int(data[1])
    print('register', player, tag, soid)
    if players[player][tag]['status']:
        game_id = players[player][tag]['id']
        games[game_id]['god'] = soid
        if player + str(tag) in watching_room:
            await sio.emit('register', 0, room=player + str(tag))


@sio.on('self_go')
async def self_go(soid, data):  # data[player1, tag, x, y, color]
    player = str(data[0])
    tag = int(data[1])
    if players[player][tag]['status']:
        # print(data)
        game_id = players[player][tag]['id']
        games[game_id]['chess_log'].append((game_id, data[2], data[3], data[4]))
        god = games[game_id]['god']
        await sio.emit('self_go', data[2:], god)
        if player + str(tag) in watching_room:
            await sio.emit('go', data[2:], room=player + str(tag))


@sio.on('self_finish')
async def self_finish(soid, data):  # data[player, tag, type, winner, loser]
    player = str(data[0])
    tag = int(data[1])
    if players[player][tag]['status']:
        game_id = players[player][tag]['id']
        games[game_id]['winner'] = data[3]
        players[player][tag]['status'] = 0
        if player + str(tag) in watching_room:
            await sio.emit('finish', {'winner': data[3], 'game_id': game_id}, room=player + str(tag))


@sio.on('test_play')
async def play(soid, data):
    if not downinfo['can_play']:
        await sio.emit('error', {'type': 3, 'info': downinfo['message']}, soid)
        return
    player1 = str(data['player'])
    tag = int(data['tag'])
    player2 = str(data['opponent'])
    print(player1, 'test play', player2)
    idx1 = find_rank(player1)
    idx2 = find_rank(player2)
    if idx1 == -1 or idx2 == -1:
        await sio.emit('error', {'type': 3, 'info': "One of you have no valid code"}, soid)
        return
    await begin(player1, -tag, player1, player2, 0)
    # await begin(player1, tag, player2, player1, 0)


@sio.on('round_play')
async def round_play(soid, data):
    global rounder
    rounder = soid
    player1 = str(data['player1'])
    tag = int(data['tag'])
    player2 = str(data['player2'])
    print(player1, 'round play', player2)
    await round_begin(player1, tag, player1, player2, 1)


@sio.on('play')
async def play(soid, data):
    if not downinfo['can_play']:
        await sio.emit('error', {'type': 3, 'info': downinfo['message']}, soid)
        return
    player = str(data['player'])
    tag = int(data['tag'])
    print(player, "play")
    if players[player][tag]['status'] and players[player][tag]['id'] < 10 ** 10 or players[player][-tag]['status'] and \
            players[player][-tag]['id'] < 10 ** 10:
        await sio.emit('error', {'type': 1, 'info': 'Another color is not finished yet.'}, soid)
        return
    else:
        await error_finish(soid, {'player': player, 'tag': tag, 'new_game': 1})
        await error_finish(soid, {'player': player, 'tag': -tag, 'new_game': 1})
    idx = find_rank(player)
    if rank_info[idx]['score'] == -20:
        await sio.emit('error', {'type': 3, 'info': "You have not uploaded your code."}, soid)
        return
    elif idx == 0:
        player2 = player
    else:
        player2 = rank_info[idx - 1]['sid']
    player1 = player
    await begin(player, -tag, player1, player2, 1)
    await begin(player, tag, player2, player1, 1)


async def begin(player, tag, white, black, type):
    old_game_id = players[player][tag]['id']
    if old_game_id in games:
        del games[old_game_id]

    game_id = await add_game_log(pool, white, black)
    print("begin", white, black, game_id)
    players[player][tag]['id'] = game_id
    players[player][tag]['status'] = 1
    games[game_id] = {'white': white, 'black': black, "chess_log": [], 'game_id': game_id, "type": 1}
    await push_game(player, tag)
    subprocess.Popen('python god.py user_code {} {} {} {} {} {} {}'.format(white, black, 15, 1, player, tag, type),
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)


async def round_begin(player, tag, white, black, type):
    game_id = await add_game_log(pool, white, black)
    print("begin", white, black, game_id)
    players[white][tag]['id'] = game_id
    players[white][tag]['status'] = 1
    players[black][-tag]['id'] = game_id
    players[black][-tag]['status'] = 1
    games[game_id] = {'white': white, 'black': black, "chess_log": [], 'game_id': game_id, "type": 1}
    await push_game(white, tag)
    await push_game(black, -tag)
    subprocess.Popen('python god.py user_code {} {} {} {} {} {} {}'.format(white, black, 15, 1, player, tag, type),
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)


@sio.on('go')
async def go (soid, data):  # data[player, tag, x, y, color]
    player = str(data[0])
    tag = int(data[1])
    x = data[3]
    y = data[4]
    color = data[5]
    if players[player][tag]['status']:
        game_id = players[player][tag]['id']
        games[game_id]['chess_log'].append((game_id, x, y, color))
        if player + str(tag) in watching_room:
            await sio.emit('go', data[3:], room=player + str(tag))


@sio.on('finish')
async def finish(soid, data):  # data[player, tag, winner, loser]
    player = str(data[0])
    tag = int(data[1])
    type = int(data[2])
    winner = str(data[3])
    loser = str(data[4])
    print(data)
    if players[player][tag]['status']:
        game_id = players[player][tag]['id']
        game = games[game_id]
        if type == 1:  #type==1代表是正式比赛，test play的type为0，不计积分
            await update_game_log(pool, game_id, winner, loser)
            await update_all_list(winner, loser)
        if 'god' in game:
            await sio.emit('finish', 0, game['god'])
        if rounder:
            await sio.emit('finish', {'white': game['white'], 'black': game['black']}, rounder)
        game['winner'] = winner
        players[player][tag]['status'] = 0
        await sio.emit('finish', {'winner': winner, 'game_id': game_id}, room=player + str(tag))

# 一方代码有问题，停止对战
@sio.on('error_finish')
async def d_error_finish(soid, data):
    player = str(data['player'])
    tag = int(data['tag'])
    await error_finish(soid, {'player': player, 'tag': tag})
    await error_finish(soid, {'player': player, 'tag': -tag})


async def error_finish(soid, data):
    player = str(data['player'])
    tag = int(data['tag'])
    if players[player][tag]['status']:
        print(data)
        game_id = players[player][tag]['id']
        if games[game_id]['type'] == 1:
            await update_game_log(pool, game_id, 0, 0)
        if 'god' in games[game_id]:
            await sio.emit('finish', 0, games[game_id]['god'])
        games[game_id]['winner'] = 0
        players[player][tag]['status'] = 0
        if 'new_game' not in data:
            print('error')
            if player + str(tag) in watching_room:
                await sio.emit('error_finish', 0, room=player + str(tag))


@sio.on('error')
async def error(soid, data):  # data[player, tag, type, msg]
    sleep(0.3)
    await sio.emit('error', {'type': 2, 'info': data[3]}, room=str(data[0]) + str(data[1]))


# 远程发送控制命令，可以刷新榜单，停服维护等
@sio.on('order')
async def order(soid, data):
    order = data['order']
    params = data['params']
    if order == 'down':
        downinfo['can_play'] = params['can_play']
        downinfo['message'] = params['message']
        await sio.emit('error', {'type': 3, 'info': params['message']})
    elif order == 'check_games':
        await sio.emit('check_games', games, soid)
    elif order == 'check_players':
        await sio.emit('check_players', players, soid)
    elif order == 'update_rank':
        await round_init_list()


# 更新榜单
async def update_all_list(winner='0', loser='0'):
    global rank_info
    if winner != loser:
        score_info[winner]['score'] += 5
        if score_info[loser]['score'] > 0:
            score_info[loser]['score'] -= 5
    rank_info = [{'sid': k, 'name': v['name'], 'score': v['score']} for k, v in score_info.items()]
    rank_info.sort(key=lambda x: (x['score'], random.random()), reverse=True)
    await sio.emit('update_list', rank_info)


# 初始化榜单
async def init_list():
    global score_info
    score_info = {}
    users = await get_users(pool)
    for row in users:
        if row['sid'] not in score_info:
            score_info[row['sid']] = {'name': row['name'], 'score': -10 if int(row['update_times']) else -20}

    logs = await get_game_logs(pool)
    for row in logs:
        winner = str(row['winner'])
        loser = str(row['loser'])
        if winner == loser:
            continue
        if winner in score_info:
            score_info[winner]['score'] += 5
        if loser in score_info:
            if score_info[loser]['score'] > 0:
                score_info[loser]['score'] -= 5
    await update_all_list()


# 循环赛初始化榜单
async def round_init_list():
    global score_info
    score_info = {}
    users = await get_users(pool, update=True)
    for row in users:
        if row['sid'] not in score_info:
            score_info[row['sid']] = {'name': row['name'], 'score': 0}

    logs = await get_game_logs(pool, config.round_start_time)
    for row in logs:
        winner = row['winner']
        loser = row['loser']
        if winner == loser:
            continue
        if winner in score_info:
            score_info[winner]['score'] += 5
        if loser in score_info:
            score_info[loser]['score'] -= 5
    await update_all_list()


# 获取新榜单
@sio.on('update_list')
async def update_one_list(soid, data):
    await sio.emit('update_list', rank_info, room=soid)


@sio.on('disconnect')
def disconnect(soid):
    print('disconnect ', soid)


async def init_pool():
    global pool
    pool = await aiomysql.create_pool(host=config.host, port=config.port, user=config.db_user,
                                      password=config.db_password, db=config.db_name, loop=loop, autocommit=True,
                                      minsize=1, maxsize=100)
    await init_list()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_pool())
    web.run_app(app)
