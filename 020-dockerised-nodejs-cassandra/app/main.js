const yargs = require('yargs');

// Argument parser
const argv = yargs
  .option('port', {
    alias: 'p',
    description: 'Port number to listen',
    type: 'integer'
  })
  .help()
  .alias('help', 'h')
  .argv;

const cassandra = require('cassandra-driver');
const C = new cassandra.Client({
  contactPoints: ['c1:9042'], // Use container name (c1) instead of 0.0.0.0
  localDataCenter: 'datacenter1'
});

/**
 * Prepare cassandra
 *
 * API REF: https://docs.datastax.com/en/developer/nodejs-driver/4.6/api/class.Client/
 */
async function prep(){
  await C.connect();
  await C.execute("CREATE KEYSPACE IF NOT EXISTS ks1 WITH replication \
    = {'class':'SimpleStrategy', 'replication_factor':1}");
  await C.execute("USE ks1");
  await C.execute("CREATE TABLE IF NOT EXISTS tb1 (\
    id bigint PRIMARY KEY,\
    ts timestamp,\
    v text)");
  await C.execute("INSERT INTO tb1 \
    (id, ts, v) \
    VALUES (0, toTimestamp(toDate(now())), 'sample')");
}

// Upon startup, prepare the database
prep();

// Start a simple REST server
const express = require("express");
var app = express();
var server = app.listen(argv.port, () => {
 console.log(`Server running on port ${argv.port}`);
});

// list all records
app.get("/ls", (req, res, next) => {
  const query = 'SELECT * FROM ks1.tb1';
  C.execute(query)
    .then((records) => {
      res.setHeader('Content-Type', 'application/json');
      res.send(JSON.stringify(records.rows));
    })
});

// add new record
app.post("/add/:id", async (req, res, next) => {
  await C.connect();
  const dt = 'toTimestamp(toDate(now()))';
  C.execute(`INSERT INTO ks1.tb1 (id, ts, v) VALUES (${req.params.id}, ${dt}, '${req.query.v}')`)
    .then((r) => {
      res.setHeader('Content-Type', 'application/json');
      res.send({status: 'ok'});
    })
    .catch((e) => {
      res.status = 500;
      res.send({status: 'error'});
      console.error(e);
    })
});

// Handle shutdown event signal
// REF: https://hackernoon.com/graceful-shutdown-in-nodejs-2f8f59d1c357
process.on('SIGTERM', () => {
  console.info('SIGTERM signal received.');
  // Shutdown the server, so serves no more new req
  server.close(() => {
    console.info('Shutting down server.');
    C.shutdown();
    console.info('Cassandra connection terminated.')
    console.info('[BYE]');
  })
});



