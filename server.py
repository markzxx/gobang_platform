import asyncio
import base64
import hashlib
import imp
import os
import random
import subprocess
import time

import aiohttp_jinja2
import aiosqlite
import jinja2
import socketio
from aiohttp import web
from aiohttp_session import setup, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet

import mail

DB_NAME = "sqlite.db"
verify_map = {}
downinfo = {'can_play': True, 'message': ""}

class Http_handler:
    @aiohttp_jinja2.template('index.html')
    async def index(self, request):
        session = await get_session(request)
        if 'sid' in session:
            return {'sid': session['sid']}
        else:
            return aiohttp_jinja2.render_template('login.html', request, {})
    
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
            
        data = await request.post()
        session = await get_session(request)
        if data['pwd'] == str(hashlib.md5('123'.encode()).hexdigest()):
            return {'error': "Password too weak, please reset it."}

        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute("SELECT * FROM users where sid='{}'".format(data['sid']))
            row = await cursor.fetchone()
            await cursor.close()
        if row and row[1] != data['pwd']:
            return {'error': "Password wrong"}
        elif not row:
            return {'error': "Student Id not exist"}
        # elif not row:
        #     await db.execute("insert into users values({}, '{}', 0, 0, 0)".format(data['sid'], data['pwd']))
        #     await db.commit()
        else:
            session['sid'] = data['sid']
            return aiohttp_jinja2.render_template('index.html', request, {'sid': data['sid']})

    async def send_email (self, request):
        data = await request.post()
        sid = data['sid']
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute("SELECT * FROM users where sid='{}'".format(sid))
            row = await cursor.fetchone()
            await cursor.close()
        if not row:
            return web.Response(text="Error: StudentId not exist")
        verify_code = str(random.randint(100000, 1000000))
        verify_map[sid] = verify_code
        mail.send_verify_code(sid, verify_code)
        return web.Response(text="ok, please check your student email.")
    
    @aiohttp_jinja2.template('resetpwd.html')
    async def resetpwd(self, request):
        if request._method == "GET":
            return {}
        data = await request.post()
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute("SELECT * FROM users where sid='{}'".format(data['sid']))
            row = await cursor.fetchone()
            await cursor.close()
            if not row:
                return {'error': "Error: StudentId not exist."}
            if data['sid'] in verify_map and data['verify_code'] == verify_map[data['sid']]:
                await db.execute("UPDATE users set password='{}' where sid='{}'".format(data['newpwd'], data['sid']))
                await db.commit()
                del verify_map[data['sid']]
            else:
                return {'error': "Error: Wrong verify code."}
            raise web.HTTPFound('/login')
    
    @aiohttp_jinja2.template('index.html')
    async def upload(self, request):
        session = await get_session(request)
        if 'sid' not in session:
            raise web.HTTPFound('/login')
        sid = session['sid']
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
                if size > 1024**2:
                    return {'sid': sid, 'error': "Your code can not excess 1M."}

        #test code
        code_checker = imp.load_source('CodeCheck', 'code_check.py').CodeCheck('tem_code/{}.py'.format(sid), 15)
        # code_checker = CodeCheck('tem_code/{}.py'.format(sid))
        if not code_checker.check_code():
            return {'sid': sid, 'error': code_checker.errormsg}
        subprocess.Popen('mv tem_code/{}.py user_code/{}.py'.format(sid, sid), shell=True)
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute("SELECT * FROM users where sid='{}' and submit_time != 0".format(sid))
            row = await cursor.fetchone()
            await cursor.close()
            if row:
                await db.execute("update users set last_update=CURRENT_TIMESTAMP where sid='{}'".format(sid))
            else:
                await db.execute("update users set submit_time=CURRENT_TIMESTAMP, last_update=CURRENT_TIMESTAMP where sid='{}'".format(sid))
            await db.commit()
        await update_all_list()
        return {'sid': sid, 'error': "Upload success, usability test pass."}

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
                web.post('/upload', handler.upload, name='upload'),
                web.post('/resetpwd', handler.resetpwd, name='reset'),
                web.get('/resetpwd', handler.resetpwd, name='reset'),
                web.post('/send_email', handler.send_email, name='send_email')])
fernet_key = fernet.Fernet.generate_key()
secret_key = base64.urlsafe_b64decode(fernet_key)
setup(app, EncryptedCookieStorage(secret_key))

rank_info = []
score_info = {}
max_game_id = 0
games = {}
players = {}

def score(row):
    sid = row[0]
    score_info = row[1]*10-row[2]*10
    return {'score': score_info, 'rand': random.random(), 'sid': sid}

def find_rank(sid):
    idx = -1
    for i, info in enumerate(rank_info):
        if sid == info['sid']:
            idx = i
            break
    return idx

async def add_game_log (white, black):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("insert into game_log(white_sid, black_sid, start_time, end_time, winner, loser) "
                                  "values('{}', '{}', datetime({}, 'unixepoch', 'localtime'), 0, 0, 0)".format(white, black,
                                                                                                           int(time.time())))
        await db.commit()
        id = cursor.lastrowid
        await cursor.close()
    return id

async def update_game_log (game_id, winner, loser):
    # print("update_game_log", game_id, winner, loser)
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "update game_log set winner='{}', loser='{}', end_time=datetime({}, 'unixepoch', 'localtime') where id={}".format(
                winner, loser, int(time.time()), game_id))
        await db.commit()
    # print("update_game_log success")

async def update_chess_log (game_id):
    # print("update_chess_log", games[game_id]['chess_log'])
    async with aiosqlite.connect(DB_NAME) as db:
        await db.executemany("insert into chess_log values(?,?,?,?,datetime(?, 'unixepoch', 'localtime'))",
                             games[game_id]['chess_log'])
        await db.commit()
    # print("update_chess_log success")
    
@sio.on('connect')
async def connect(soid, environ):
    print("connect ", soid)

@sio.on('message')
async def message (soid, msg):
    print(soid, "msg ", msg)

async def push_game(player, soid=None):
    if player in players:
        await sio.emit('push_game', games[players[player]], room=soid if soid else player)
        
@sio.on('watch')
async def message(soid, room):
    room = str(room)
    if len(sio.rooms(soid)) > 1:
        sio.leave_room(soid, sio.rooms(soid)[1])
    sio.enter_room(soid, room)
    await push_game(room, soid)

@sio.on('self_play')
async def self_play(soid, data):
    if not downinfo['can_play']:
        await sio.emit('error', {'type': 3, 'info': downinfo['message']}, soid)
        return
    player = str(data['player'])
    AI = str(data['AI'])
    color = int(data['color'])
    print(player, 'self_play')
    if player in players:
        await sio.emit('error', {'type': 1, 'info': "You are in an unfinished game."}, soid)
    else:
        idx = find_rank(AI)
        if idx == -1:
            await sio.emit('error', {'type': 3, 'info': "No valid code."}, soid)
            return
        if color == 1:
            await self_begin(player, AI, 'human-' + player)
        else:
            await self_begin(player, 'human-' + player, AI)

async def self_begin(player, white, black):
    game_id = 0
    while game_id in games:
        game_id = random.randint(1000000, 10000000)
    print("self_begin", white, black, game_id)
    players[player] = game_id
    games[game_id] = {'white': white, 'black': black, "chess_log": []}
    await push_game(player)
    subprocess.Popen('python god.py user_code {} {} {} {} {}'.format(white, black, 15, 1, player), stdout=open('output_god', 'w+'), stderr=open('error_god', 'w+'), shell=True)
    
@sio.on('self_register')
async def self_register(soid, player):
    print('register',player,soid)
    player = str(player)
    if player in players:
        game_id = players[player]
        games[game_id]['god'] = soid
        await sio.emit('register', 0, room=player)

@sio.on('self_go')
async def self_go(soid, data):  #data[player1, x, y, color]
    player = str(data[0])
    if player in players:
        # print(data)
        game_id = players[player]
        games[game_id]['chess_log'].append((game_id, data[1], data[2], data[3], int(time.time())))
        god = games[game_id]['god']
        await sio.emit('self_go', data[1:], god)
        await sio.emit('go', data[1:], room=player)

@sio.on('self_finish')
async def self_finish (soid, data):
    if data[0] in players:
        game_id = players[data[0]]
        del games[game_id]
        del players[data[0]]
        await sio.emit('finish', data[1], room=data[0])
        time.sleep(0.2)
        
@sio.on('play')
async def play(soid, player):
    if not downinfo['can_play']:
        await sio.emit('error', {'type': 3, 'info': downinfo['message']}, soid)
        return
    player = str(player)
    print(player, "play")
    if player in players:
        await sio.emit('error', {'type': 1, 'info': "You are in an unfinished game."}, soid)
    else:
        idx = find_rank(player)
        if idx == -1:
            await sio.emit('error', {'type': 3, 'info': "You have not uploaded user_code."}, soid)
            return
        elif idx == 0:
            player2 = player
        else:
            player2 = rank_info[idx-1]['sid']
        player1 = player
        if random.random() > 0.5:
            await begin(player, player1, player2)
        else:
            await begin(player, player2, player1)
        # await begin(player2, player1)
    
async def begin(player1, white, black):
    game_id = await add_game_log(white, black)
    print("begin", white, black, game_id)
    players[player1] = game_id
    games[game_id] = {'white': white, 'black': black, "chess_log": []}
    await push_game(player1)
    subprocess.Popen('python god.py user_code {} {} {} {} {}'.format(white, black, 15, 1, player1), stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'), shell=True)

@sio.on('go')
async def go(soid, data):  #data[player1, 0, x, y, color]
    # print("go", data)
    if data[0] in players:
        game_id = players[data[0]]
        games[game_id]['chess_log'].append((game_id, data[1], data[2], data[3], int(time.time())))
        await sio.emit('go', data[1:], room=data[0])
        
@sio.on('finish')
async def finish(soid, data):
    if data[0] in players:
        game_id = players[data[0]]
        await update_game_log(game_id, data[1], data[2])
        # await update_chess_log(game_id)
        await update_all_list()
        if 'god' in games[game_id]:
            await sio.emit('finish', 0, games[game_id]['god'])
        del games[game_id]
        del players[data[0]]
        await sio.emit('finish', data[1], room=data[0])
        time.sleep(0.2)
        
@sio.on('error_finish')
async def error_finish(soid, player):
    player = str(player)
    if player in players:
        game_id = players[player]
        await update_game_log(game_id, 0, 0)
        # await update_chess_log(game_id)
        # await update_all_list()
        if 'god' in games[game_id]:
            await sio.emit('finish', 0, games[game_id]['god'])
        del games[game_id]
        del players[player]
        await sio.emit('error_finish', 0, room=player)

@sio.on('error')
async def error(soid, data):
    await sio.emit('error', {'type': 2, 'info': data[1]}, room=data[0])

@sio.on('check_games')
async def check_games (soid, data):
    await sio.emit('check_games', games, soid)
    
@sio.on('downtime')
async def downtime (soid, data):
    downinfo['can_play'] = data['can_play']
    downinfo['message'] = data['message']
    await sio.emit('error', {'type': 3, 'info': data['message']})

@sio.on('test_go')
async def go(soid, data):
    print("test_go", data)
    game_id = players[data[0]]
    await sio.emit('go', data[1:], room=games[game_id]['white'])
    await sio.emit('go', data[1:], room=games[game_id]['black'])


async def update_all_list(sid=None, data=None):
    global rank_info, score_info, max_game_id
    
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT sid FROM users WHERE submit_time!=0")
        users = await cursor.fetchall()
        await cursor.close()
    for row in users:
        if row[0] not in score_info:
            score_info[row[0]] = 0

    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT id, winner, loser FROM game_log WHERE id>?", [max_game_id])
        logs = await cursor.fetchall()
        await cursor.close()
    for row in logs:
        winner = str(row[1])
        loser = str(row[2])
        max_game_id = row[0]
        if winner == loser:
            continue
        if winner in score_info:
            score_info[winner] += 5
        if loser in score_info:
            if score_info[loser] >= 5:
                score_info[loser] -= 5
            else:
                score_info[loser] = 0
    
    rank_info = [{'sid': k, 'score': v} for k, v in score_info.items()]
    rank_info.sort(key=lambda x: (x['score'], random.random()), reverse=True)
    await sio.emit('update_list', rank_info)

@sio.on('update_list')
async def update_one_list(soid, data):
    await sio.emit('update_list', rank_info, room=soid)
    
@sio.on('disconnect')
def disconnect(soid):
    print('disconnect ', soid)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_all_list())
    web.run_app(app)
