create table rent( 
    url varchar(2083) not null, 
    id int not null auto_increment, 
    title text not null, 
    price int not null, 
    layout varchar(255), 
    sqm varchar(255), 
    floor varchar(255), 
    hourse_type varchar(255), 
    house_status varchar(255), 
    community varchar(255), 
    pet varchar(255), 
    prkg varchar(255), 
    cooking varchar(255), 
    id_req varchar(255),
    primary key(id), 
    unique index url_hash using hash(url)
);