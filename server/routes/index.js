const express = require('express');
const router = express.Router();
const pg = require('pg');
const path = require('path');
const connectionString = process.env.DATABASE_URL || 'postgres://postgres:postgres@localhost:5432/measure_device_base';

router.get('/', (req, res, next) => {
    res.sendFile(path.join(
    __dirname, '..', '..', 'client', 'views', 'index.html'));
});

router.get('/api/v1/dev', (req, res, next) => {
    const results = [];
    pg.connect(connectionString, (err, client, done) => {
        if(err) {
            done();
            console.log(err);
            return res.status(500).json({success: false, data: err});
        }
    
        const query = client.query('SELECT * FROM devices');
        query.on('row', (row) => {
            results.push(row);
        });

        query.on('end', () => {
            done();
            return res.json(results);
        });
    });
});

router.get('/api/v1/logs', (req, res, next) => {
    const results = [];
    pg.connect(connectionString, (err, client, done) => {
        if(err) {
            done();
            console.log(err);
            return res.status(500).json({success: false, data: err});
        }

        const query = client.query('SELECT * FROM logs');
        query.on('row', (row) => {  
            results.push(row);
        });

        query.on('end', () => {
            done();
            return res.json(results);
        });
    });
});

router.post('/api/v1/dev', (req, res, next) => {
    const results = [];
    const data = {own_name: req.body.own_name, lan_address: req.body.lan_address, lan_port: req.body.lan_port, active: false};

    pg.connect(connectionString, (err, client, done) => {
        if(err) {
            done();
            console.log(err);
            return res.status(500).json({success: false, data: err});
        }

        client.query('INSERT INTO devices(own_name, lan_address, lan_port, active) values($1, $2, $3, $4)',[data.own_name, data.lan_address, data.lan_port, data.active]);
        const query = client.query('SELECT * FROM devices');
        query.on('row', (row) => {
            results.push(row);
        });

        query.on('end', () => {
            done();
            return res.json(results);
        });
    });
});

router.delete('/api/v1/dev/:dev_id', (req, res, next) => {
    const results = [];
    const id = req.params.dev_id;
    pg.connect(connectionString, (err, client, done) => {
        if(err) {
            done();
            console.log(err);
            return res.status(500).json({success: false, data: err});
        }

        client.query('DELETE FROM devices WHERE id=($1)', [id]);
        var query = client.query('SELECT * FROM devices');
        
        query.on('row', (row) => {
            results.push(row);
        });

    query.on('end', () => {
      done();
      return res.json(results);
    });
  });
});

router.delete('/api/v1/logs/', (req, res, next) => {
    const results = [];
    pg.connect(connectionString, (err, client, done) => {
        if(err) {
            done();
            console.log(err);
            return res.status(500).json({success: false, data: err});
        }

        client.query('DELETE FROM logs');
        var query = client.query('SELECT * FROM logs');
        query.on('row', (row) => {
            results.push(row);
        });

        query.on('end', () => {
            done();
            return res.json(results);
        });
    });
});

module.exports = router;
