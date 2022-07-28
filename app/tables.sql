# создай новую базу данных
# psql -f tables.sql -U timikus -h localhost -d test

create table if not exists users(
    id serial primary key,
    username varchar(30) not null,
    password varchar(255) not null
);

create table if not exists operators(
    id serial primary key,
    op_name varchar(30) not null,
    default_rate int 
);

create table if not exists requests(
    id serial primary key,
    request_id int not null,
    contract_id int not null,
    created timestamp without time zone not null,
    is_delayed boolean,
    operator_id int references operators(id) not null
);

insert into operators(op_name) values ('castorama-1'),('castorama-2'),('castorama-3');
insert into operators(op_name) values ('megastroy-1'),('megastroy-2'),('megastroy-3');
insert into operators(op_name) values ('leroy-1'),('leroy-2'),('leroy-3');

insert into requests(request_id, contract_id, created, is_delayed, operator_id) values (1235, 405, now(), True, 1);
insert into requests(request_id, contract_id, created, is_delayed, operator_id) values (1236, 406, now(), False, 1);
insert into requests(request_id, contract_id, created, is_delayed, operator_id) values (1237, 407, now(), True, 1);
insert into requests(request_id, contract_id, created, is_delayed, operator_id) values (1238, 408, now(), False, 2);
insert into requests(request_id, contract_id, created, is_delayed, operator_id) values (1239, 409, now(), True, 2);
insert into requests(request_id, contract_id, created, is_delayed, operator_id) values (1240, 410, now(), False, 2);
insert into requests(request_id, contract_id, created, is_delayed, operator_id) values (1241, 411, now(), True, 3);
insert into requests(request_id, contract_id, created, is_delayed, operator_id) values (1242, 412, now(), False, 3);
insert into requests(request_id, contract_id, created, is_delayed, operator_id) values (1243, 413, now(), True, 3);