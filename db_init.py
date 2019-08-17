import asyncio
import aiomysql
import hashlib
import config

async def init_db ():
    pool = await aiomysql.create_pool(host=config.host, port=config.port, user=config.db_user, password=config.db_password, db=config.db_name, loop=loop, autocommit=True)
    
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            # 创建user表
            await cur.execute(
            "create table if not exists users "
            "(sid varchar(12) primary key, name varchar(12), password varchar(32) NOT NULL, submit_time TIMESTAMP, last_update TIMESTAMP, update_times int default 0)"
            )
            
            
            # 创建测试账号和学生账号
            test_users = ['test1', "test2", "test3", 'test4']
            # with open('students.txt', 'r') as f:
            #     for line in f.readlines():
            #         test_users.append(line.strip('\n'))
            for user in test_users:
                await cur.execute("insert ignore into users values ('%s', '%s', '%s', 0, 0, 0)"%(user, user, str(hashlib.md5('888'.encode()).hexdigest())))

            # 创建比赛记录表
            await cur.execute(
            "create table if not exists game_log "
            "(id INTEGER primary key AUTO_INCREMENT, white_sid varchar(12), black_sid varchar(12), "
            "start_time TIMESTAMP, end_time TIMESTAMP, winner varchar(12), loser varchar(12), "
            "FOREIGN KEY(white_sid) REFERENCES users(sid), FOREIGN KEY(black_sid) REFERENCES users(sid))"
            )
        
            # 添加模拟比赛信息
            test_game_log = [('test1', 'test2', 'test1', 'test2'), ('test3', 'test1', 'test3', 'test1'), ('test2', 'test3', 'test2', 'test3'), ('test2', 'test3', 0, 0)]
            for i, log in enumerate(test_game_log):
                await cur.execute("insert into game_log(white_sid, black_sid, start_time, end_time, winner, loser)"
                                 " values ('{}', '{}', now(), now(), '{}', '{}')".format(log[0], log[1], i*100, log[2], log[3]))

        #     await cur.execute(
        #     "create table if not exists chess_log "
        #     "(game_id int, x int, y int, color int, chess_time time,"
        #     "FOREIGN KEY(game_id) REFERENCES game_log(id), UNIQUE (game_id, x, y))"
        #       )

        #     await cur.execute(
        #     "create view rank as "
        #     "select sid, sum(tem_win) as win, sum(tem_lose) as lose, count(sid) as total, submit_time "
        #     "from(select sid, submit_time, g.start_time satrt, g.end_time end, case when g.winner=sid then 1 ELSE 0 end as tem_win, case when g.loser=sid then 1 ELSE 0 end as tem_lose "
        #     "FROM users left JOIN game_log g ON (users.sid = g.white_sid or users.sid = g.black_sid)) a where submit_time != 0 "
        #     "GROUP BY sid"
        #       )
        
loop = asyncio.get_event_loop()
loop.run_until_complete(init_db())