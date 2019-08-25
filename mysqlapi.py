import aiomysql
async def get_user(pool, sid):
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("SELECT * FROM users where sid='{}'".format(sid))
            row = await cursor.fetchone()
    return row

async def get_users(pool, update=False):
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            if update:
                await cursor.execute("SELECT * FROM users where last_update is not null")
            else:
                await cursor.execute("SELECT * FROM users")
            users = await cursor.fetchall()
    return users

async def set_pwd(pool, sid , pwd):
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("UPDATE users set password='{}' where sid='{}'".format(pwd, sid))


async def add_game_log(pool, white, black):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("insert into game_log(white_sid, black_sid, start_time, end_time, winner, loser) "
                                 "values('%s', '%s', current_timestamp, null, 0, 0)" % (white, black))
            return cursor.lastrowid


async def update_game_log(pool, game_id, winner, loser):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "update game_log set winner='%s', loser='%s', end_time=current_timestamp where id=%d" % (
                winner, loser, game_id))


async def get_game_logs(pool, start_time=0):
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            if start_time:
                await cursor.execute("SELECT * FROM game_log where start_time > '{}'".format(start_time))
            else:
                await cursor.execute("SELECT * FROM game_log")
            logs = await cursor.fetchall()
    return logs

async def set_update_time(pool, sid, update_times):
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            if update_times==1:
                await cursor.execute("UPDATE users set submit_time=current_timestamp, last_update=current_timestamp, update_times={} where sid='{}'".format(int(update_times), sid))
            else:
                await cursor.execute("UPDATE users set last_update=current_timestamp, update_times={} where sid='{}'".format(int(update_times), sid))
