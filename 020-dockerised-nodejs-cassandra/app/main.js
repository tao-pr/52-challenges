const cassandra = require('cassandra-driver');
const C = new cassandra.Client({
  contactPoints: ['h1', 'h2'],
  localDataCenter: 'datacenter1',
  keyspace: 'ks1'
});

const sql_prepare = 
  "CREATE KEYSPACE IF NOT EXISTS ks1 WITH replication \
    = {'class':'SimpleStrategy', 'replication_factor':1}; \
  USE ks1;\
  CREATE TABLE IF NOT EXISTS tb1 (\
    id bigint PRIMARY_KEY,\
    ts timestamp,\
    v text); \
  INSERT INTO tb1 \
    (id, ts, v) \
    VALUES (0, toTimestamp(toDate(now())), 'sample');\
  ";

// Upon startup, prepare the database
C.execute(sql_prepare)
  .then(_ => console.log("Cassandra keyspace created."))
  .catch(e => console.error(e));


// Start a simple REST server