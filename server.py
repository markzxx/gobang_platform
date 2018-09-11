import aiohttp_jinja2
import jinja2
from aiohttp import web
import asyncio
import socketio
import aiosqlite
import random
import os
import time
import base64
from cryptography import fernet
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

DB_NAME = "sqlite.db"
class Http_handler:
    @aiohttp_jinja2.template('index')
    async def index(self, request):
        session = await get_session(request)
        if 'sid' in session:
            context = {'sid': session['sid']}
            response = aiohttp_jinja2.render_template('index.html', request, context)
            return response
        else:
            return aiohttp_jinja2.render_template('login.html', request, {})

    @aiohttp_jinja2.template('login')
    async def login(self, request):
        if request._method == "GET":
            return aiohttp_jinja2.render_template('login.html', request, {})
            
        data = await request.post()
        session = await get_session(request)
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute('SELECT * FROM users where sid={}'.format(data['sid']))
            row = await cursor.fetchone()
            await cursor.close()
            if row and row[1] != data['pwd']:
                raise self.redirect(request.app.router, 'login')
            elif not row:
                await db.execute("insert into users values({}, '{}', 0, 0, 0)".format(data['sid'], data['pwd']))
                await db.commit()
        session['sid'] = data['sid']
        raise self.redirect(request.app.router, 'index')
        
    async def upload(self, request):
        session = await get_session(request)
        sid = session['sid']
        reader = await request.multipart()
        field = await reader.next()
        assert field.name == 'code'
        size = 0
        if not os.path.exists("code/"):
            os.mkdir("code/")
        with open(os.path.join('code/{}.py'.format(sid)), 'wb') as f:
            while True:
                chunk = await field.read_chunk()
                if not chunk:
                    break
                size += len(chunk)
                f.write(chunk)
                
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute('SELECT * FROM users where sid={}'.format(sid))
            row = await cursor.fetchone()
            await cursor.close()
            if row[2]:
                await db.execute("update users set last_update=CURRENT_TIMESTAMP where sid={}".format(sid))
            else:
                await db.execute("update users set submit_time=CURRENT_TIMESTAMP, last_update=CURRENT_TIMESTAMP where sid={}".format(sid))
                await update_all_list()
            await db.commit()
        
        raise self.redirect(request.app.router, 'index')

    def redirect (self, router, route_name):
        location = router[route_name].url_for()
        return web.HTTPFound(location)

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('template'))

handler = Http_handler()
app.router.add_static('/static', 'template')
app.add_routes([web.get('/', handler.index, name='index'),
                web.get('/login', handler.login, name='login'),
                web.post('/login', handler.login, name='login'),
                web.post('/upload', handler.upload, name='upload')])
fernet_key = fernet.Fernet.generate_key()
secret_key = base64.urlsafe_b64decode(fernet_key)
setup(app, EncryptedCookieStorage(secret_key))

watchDict = {}
watchingDic = {}
rank_info = []
games = {}
players = {}

def score(row):
    sid = row[0]
    score_info = row[1]*10-row[2]*10
    # if score_info < 0:
    #     score_info = 0
    return {'score':score_info, 'rand':random.random(), 'sid':sid}

def find_rank(sid):
    idx = 0
    find = False
    for i, info in enumerate(rank_info):
        if sid == info['sid']:
            idx = i
            find = True
            break
    return find, idx

async def add_game_log (white, black):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("insert into game_log(white_sid, black_sid, start_time, end_time, winner, loser) "
                                  "values({}, {}, datetime({}, 'unixepoch', 'localtime'), 0, 0, 0)".format(white, black,
                                                                                                           int(time.time())))
        await db.commit()
        id = cursor.lastrowid
        await cursor.close()
    return id

async def update_game_log (game_id, winner, loser):
    # print("update_game_log", game_id, winner, loser)
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "update game_log set winner={}, loser={}, end_time=datetime({}, 'unixepoch', 'localtime') where id={}".format(
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

async def push_game(player, soid=None):
    if player in players:
        await sio.emit('push_game', games[players[player]], room=soid if soid else player)
        
@sio.on('watch')
async def message(soid, data):
    data = int(data)
    print('watch', data)
    if len(sio.rooms(soid)) > 1:
        sio.leave_room(soid, sio.rooms(soid)[1])
    sio.enter_room(soid, data)
    await push_game(data, soid)

@sio.on('play')
async def play(soid, data):
    print(data)
    if data['sid'] in players:
        await sio.emit('reply', "You are in an unfinished game", soid)
    else:
        find, idx = find_rank(data['sid'])
        if not find:
            await sio.emit('reply', "You have not uploaded code.", room=soid)
            return
        elif idx == 0:
            player2 = data['sid']
        else:
            player2 = rank_info[idx-1]['sid']
        player1 = data['sid']
        await begin(player1, player1, player2)
        # await begin(player2, player1)
    
async def begin(player1, white, black):
    game_id = await add_game_log(white, black)
    print("begin", white, black, game_id)
    players[player1] = game_id
    games[game_id] = {'white': white, 'black': black, "chess_log": []}
    await push_game(player1)
    t = os.popen('python god.py code {} {} {} {} {}'.format(white, black, 15, 1, player1))

@sio.on('go')
async def go(soid, data):
    # print("go", data)
    game_id = players[data[0]]
    games[game_id]['chess_log'].append((game_id, data[2], data[3], data[4], int(time.time())))
    await sio.emit('go', data[2:], room=data[0])

@sio.on('finish')
async def finish(soid, data):
    game_id = players[data[0]]
    await update_game_log(game_id, data[4], data[5])
    await update_chess_log(game_id)
    await update_all_list()
    del games[game_id]
    del players[data[0]]
    await sio.emit('finish', data[4], room=data[0])

@sio.on('error')
async def finish(soid, data):
    await sio.emit('error', data[2], room=data[0])

@sio.on('test_go')
async def go(soid, data):
    print("test_go", data)
    game_id = players[data[0]]
    await sio.emit('go', data[1:], room=games[game_id]['white'])
    await sio.emit('go', data[1:], room=games[game_id]['black'])

async def update_all_list(sid=None, data=None):
    global rank_info
    rank_info = []
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("select * from rank")
        rows = await cursor.fetchall()
        await cursor.close()
        for row in rows:
            rank_info.append(score(row))
    rank_info = sorted(rank_info, key=lambda x: (x['score'],x['rand']), reverse=True)
    await sio.emit('update_list', rank_info)

@sio.on('update_list')
async def update_one_list(soid, data):
    print(rank_info)
    await sio.emit('update_list', rank_info, room=soid)
    
@sio.on('disconnect')
def disconnect(soid):
    print('disconnect ', soid)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_all_list())
    web.run_app(app)