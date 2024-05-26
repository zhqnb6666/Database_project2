create table unexitedridepassenger
(
    ride_id       int auto_increment
        primary key,
    user_id       varchar(255)  null,
    start_station varchar(255)  null,
    start_time    timestamp     null,
    level         int default 0 null,
    constraint unexitedridepassenger_ibfk_1
        foreign key (user_id) references passengers (id_number),
    constraint unexitedridepassenger_ibfk_2
        foreign key (start_station) references stations (english_name)
);

create index start_station
    on unexitedridepassenger (start_station);

create index user_id
    on unexitedridepassenger (user_id);

