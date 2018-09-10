import aiosqlite
import asyncio
import logging
import os
import sys
import traceback
import hashlib
import random

DB_NAME = "sqlite.db"

def cleanup():
    if os.path.exists(DB_NAME):
        os.unlink(DB_NAME)
        
async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "create table users "
            "(sid int primary key, password varchar(32) NOT NULL, submit_time time, last_update time, update_times int default 0)"
        )
        
        test_users = [(123, "123"), (456, "456"), (789, "789")]
        for user in test_users:
            await db.execute("insert into users values ({}, '{}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0)".format(user[0], str(hashlib.md5(user[1].encode()).hexdigest())))
        await db.commit()
        
        await db.execute(
            "create table game_log "
            "(id INTEGER primary key autoincrement, white_sid int, black_sid int, start_time time,"
            "end_time time, winner int, loser int, "
            "FOREIGN KEY(white_sid) REFERENCES users(sid), FOREIGN KEY(black_sid) REFERENCES users(sid),"
            "UNIQUE(white_sid, black_sid, start_time))"
        )
        
        test_game_log = [(123, 789, 123, 789), (123, 789, 123, 789), (456, 798, 456, 798), (798, 456, 0, 0)]
        for i, log in enumerate(test_game_log):
            await db.execute("insert into game_log(white_sid, black_sid, start_time, end_time, winner, loser)"
                             " values ({}, {}, CURRENT_TIMESTAMP-{}, CURRENT_TIMESTAMP, {}, {})".format(log[0], log[1], i*100, log[2], log[3]))
        await db.commit()
        
        await db.execute(
            "create table chess_log "
            "(game_id int, x int, y int, color int, chess_time time,"
            "FOREIGN KEY(game_id) REFERENCES game_log(id), UNIQUE (game_id, x, y))"
        )

        await db.execute(
            "create view rank as "
            "select sid, sum(tem_win) as win, sum(tem_lose) as lose, count(sid) as total, submit_time "
            "from(select sid, submit_time, g.start_time satrt, g.end_time end, case when g.winner=sid then 1 ELSE 0 end as tem_win, case when g.loser=sid then 1 ELSE 0 end as tem_lose"
            " FROM users left JOIN game_log g ON (users.sid = g.white_sid or users.sid = g.black_sid)) a where submit_time != 0 "
            "GROUP BY sid"
        )
      
if __name__ == "__main__":
    cleanup()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    loop.close()
