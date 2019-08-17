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

async def get_game_logs(pool, start_time=0):
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            if start_time:
                await cursor.execute("SELECT * FROM game_log where start_time > '{}'".format(start_time))
            else:
                await cursor.execute("SELECT * FROM game_log")
            logs = await cursor.fetchall()
    return logs