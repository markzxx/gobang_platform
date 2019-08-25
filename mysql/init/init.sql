use chess;

-- 建用户表
create table users
(sid varchar(12) primary key, name varchar(12), password varchar(32) NOT NULL, submit_time TIMESTAMP, last_update TIMESTAMP, update_times int DEFAULT 0);

-- 插入数据
INSERT INTO users(sid, name, password) VALUES ('test1','test1',md5('888'));
INSERT INTO users(sid, name, password) VALUES ('test2','test2',md5('888'));
INSERT INTO users(sid, name, password) VALUES ('test3','test3',md5('888'));
INSERT INTO users(sid, name, password) VALUES ('test4','test4',md5('888'));


-- 建比赛表
create table game_log
(id INTEGER primary key AUTO_INCREMENT, white_sid varchar(12), black_sid varchar(12),
start_time TIMESTAMP, end_time TIMESTAMP, winner varchar(12), loser varchar(12),
FOREIGN KEY(white_sid) REFERENCES users(sid), FOREIGN KEY(black_sid) REFERENCES users(sid));

-- 插入数据
INSERT INTO game_log(white_sid, black_sid, start_time, end_time, winner, loser) VALUES ('test1', 'test1', 0, 0, 'test1', 'test1')