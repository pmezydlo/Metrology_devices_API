SET DATESTYLE TO 'European';
SET DATESTYLE TO 'SQL';

DROP TABLE devices CASCADE;
DROP TABLE logs CASCADE;

CREATE TABLE devices
(
    id              SERIAL PRIMARY KEY, 
    own_name        char(50),
    manufacturer    char(50),
    name	    char(50),
    serial_nr       char(50),
    firmware_ver    char(50),
    lan_address     char(15),
    lan_port        int,
    active	    boolean
);

CREATE TABLE logs
(
    id              SERIAL PRIMARY KEY,
    log_date        date default current_date,
    log_time        time default current_time,    
    message         char(255)
);

INSERT INTO logs VALUES (default, default, default, 'Create base');
INSERT INTO logs VALUES (default, default, default, 'Wszysko dziala');

INSERT INTO devices VALUES (default, 'osc1', 'RIGOL', '', '', '', '192.168.20.15', 5555, FALSE);
INSERT INTO devices VALUES (default, 'mul3', 'HP', '', '', '', '192.168.20.15', 5555, FALSE);
INSERT INTO devices VALUES (default, 'analiz', 'KEYSIGHT', '', '', '', '192.168.20.15', 5555, FALSE);
