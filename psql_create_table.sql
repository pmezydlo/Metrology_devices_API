SET DATESTYLE TO 'European';
SET DATESTYLE TO 'SQL';

DROP TABLE devices CASCADE;
DROP TABLE logs CASCADE;
DROP TYPE log_t;
DROP TYPE dev_status_t;
DROP TABLE tasks CASCADE;

CREATE TYPE dev_status_t AS ENUM ('NOREADY', 'READY', 'RUN');

CREATE TABLE devices
(
    id              SERIAL PRIMARY KEY, 
    own_name        char(50) UNIQUE,
    manufacturer    char(50),
    name	    char(50),
    serial_nr       char(50),
    firmware_ver    char(50),
    lan_address     char(15),
    lan_port        int,
    status	    dev_status_t default 'NOREADY'
);

CREATE TYPE log_t AS ENUM ('log', 'warning', 'error');

CREATE TABLE logs
(
    id              SERIAL PRIMARY KEY,
    log_date        char(8),
    log_time        char(8),
    log_type        log_t,
    log_msg         char(25)
);

CREATE TABLE tasks
(
    task_id         SERIAL PRIMARY KEY,
    task_name       char(50),
    task_date       char(8),
    task_time       char(8),
    task_msg        char(255),
    task_req        char(255)
);

INSERT INTO logs VALUES (default, '12.02.11', '23:12:21', 'log', 'Create base');
INSERT INTO logs VALUES (default,  '21.12.16', '23:12:12', 'error', 'type error test');

INSERT INTO devices VALUES (default, 'osc1', 'RIGOL', '', '', '', '192.168.20.15', 5555, default);
INSERT INTO devices VALUES (default, 'mul3', 'HP', '', '', '', '192.168.20.15', 5555, default);
INSERT INTO devices VALUES (default, 'analiz', 'KEYSIGHT', '', '', '', '192.168.20.15', 5555, default);

INSERT INTO tasks VALUES (default, 'task no.1', '13.02.21', '23:12:21', '', '');


