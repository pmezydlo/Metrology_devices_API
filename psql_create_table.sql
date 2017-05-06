SET DATESTYLE TO 'European';
SET DATESTYLE TO 'SQL';

DROP TABLE devices CASCADE;
DROP TABLE logs CASCADE;
DROP TABLE tasks CASCADE;
DROP TYPE log_t;
DROP TYPE dev_status_t;
DROP TYPE task_status_t;

CREATE TYPE log_t AS ENUM ('log', 'warning', 'error');
CREATE TYPE task_status_t AS ENUM ('PENDING', 'RUN', 'READY');

CREATE TABLE devices
(
    id              SERIAL PRIMARY KEY, 
    own_name        char(50) UNIQUE,
    manufacturer    char(50),
    name	    char(50),
    serial_nr       char(50),
    firmware_ver    char(50),
    lan_address     char(15),
    lan_port        int
);

CREATE TABLE logs
(
    id          SERIAL PRIMARY KEY,
    date        char(8),
    time        char(8),
    type        log_t,
    msg         char(25)
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

INSERT INTO logs VALUES (default, '12.02.11', '23:12:21', 'log', 'Create base');
INSERT INTO logs VALUES (default,  '21.12.16', '23:12:12', 'error', 'type error test');

INSERT INTO devices VALUES (default, 'osc1', 'RIGOL', '', '', '', '192.168.20.15', 5555);
INSERT INTO devices VALUES (default, 'mul3', 'HP', '', '', '', '192.168.20.15', 5555);
INSERT INTO devices VALUES (default, 'analiz', 'KEYSIGHT', '', '', '', '192.168.20.15', 5555);

INSERT INTO tasks VALUES (default, 'task no.1', '1', '13.02.21', '23:12:21', default, '*RST\n*IDN', '');


