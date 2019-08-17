-- �������ݿ�
create database `chess` default character set utf8 collate utf8_general_ci;

use chess;

-- ���û���
create table if not exists users
(sid varchar(12) primary key, name varchar(12), password varchar(32) NOT NULL, submit_time TIMESTAMP, last_update TIMESTAMP, update_times int DEFAULT 0);

-- ��������
INSERT INTO users(sid, name, password) VALUES ('test1','test1',md5('888'));

-- ��������
create table if not exists game_log
(id INTEGER primary key AUTO_INCREMENT, white_sid varchar(12), black_sid varchar(12),
start_time TIMESTAMP, end_time TIMESTAMP, winner varchar(12), loser varchar(12),
FOREIGN KEY(white_sid) REFERENCES users(sid), FOREIGN KEY(black_sid) REFERENCES users(sid));

-- ��������
insert into game_log(white_sid, black_sid, start_time, end_time, winner, loser) VALUES ('test1', 'test1', 0, 0, 'test1', 'test1')