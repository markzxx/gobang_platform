use mysql;
select host, user from user;
-- ��Ϊmysql�汾��5.7������½��û�Ϊ�������
create user docker identified by '123456';
-- ��docker_mysql���ݿ��Ȩ����Ȩ��������docker�û�������Ϊ123456��
grant all on chess.* to docker@'%' identified by '123456' with grant option;
-- ��һ������һ��Ҫ�У�
flush privileges;