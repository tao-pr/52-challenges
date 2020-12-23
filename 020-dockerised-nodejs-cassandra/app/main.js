const cassandra = require('cassandra-driver');
const C = new cassandra.Client({
  contactPoints: ['h1', 'h2'],
  localDataCenter: 'datacenter1',
  keyspace: 'ks1'
});

const sql_create_ks = "CREATE KEYSPACE IF NOT EXISTS ks1 WITH replication \
  = {'class':'SimpleStrategy', 'replication_factor':1};";

const sql_create_tb = "CREATE TABLE IF NOT EXISTS ks1.tb1 (\
  id bigint PRIMARY_KEY,\
  ts timestamp,\
  v text\
  )";
const query = 'SELECT name, email FROM users WHERE key = ?';

// Upon startup, prepare the database
C.execute(sql_create_ks)
  .then(_ => console.log("Cassandra keyspace created."))
  .then(_ => C.execute(sql_create_tb))
  .then(_ => console.log("Cassandra table created."))
