SET DATESTYLE TO 'European';
SET DATESTYLE TO 'SQL';

DROP TABLE devices CASCADE;
DROP TABLE logs CASCADE;
DROP TABLE tasks CASCADE;
DROP TYPE log_t;
DROP TYPE dev_status_t;
DROP TYPE task_status_t;

CREATE TYPE log_t AS ENUM ('LOG', 'WARNING', 'ERROR');
CREATE TYPE part_sys_t AS ENUM ('TASK', 'CORE', 'BASE', 'NOT DEFINED', 'SERVER');
CREATE TYPE task_status_t AS ENUM ('PENDING', 'RUN', 'READY');

CREATE TABLE devices
(
    id              SERIAL PRIMARY KEY, 
    name            char(50) UNIQUE,
    lan_address     char(15),
    lan_port        int
);

CREATE TABLE logs
(
    id          SERIAL PRIMARY KEY,
    date        char(8),
    time        char(8),
    sys         part_sys_t,
    type        log_t,
    msg         char(255)
);

CREATE TABLE tasks
(
    id         SERIAL PRIMARY KEY,
    name       char(50),
    dev        int REFERENCES devices(id),
    date       char(8),
    time       char(8),
    status     task_status_t default 'PENDING',
    msg        TEXT,
    req        TEXT
);


INSERT INTO devices VALUES (default, 'osc1', '192.168.20.15', 5555);



