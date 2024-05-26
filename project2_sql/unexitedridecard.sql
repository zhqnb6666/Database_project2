create table unexitedridecard
(
    ride_id       int auto_increment
        primary key,
    user_id       decimal       null,
    start_station varchar(255)  null,
    start_time    timestamp     null,
    level         int default 0 null,
    constraint unexitedridecard_ibfk_1
        foreign key (user_id) references cards (code),
    constraint unexitedridecard_ibfk_2
        foreign key (start_station) references stations (english_name)
);

create index start_station
    on unexitedridecard (start_station);

create index user_id
    on unexitedridecard (user_id);

