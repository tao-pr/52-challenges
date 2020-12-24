const cassandra = require('cassandra-driver');
const C = new cassandra.Client({
  contactPoints: ['0.0.0.0:9042'],
  localDataCenter: 'datacenter1'
});

/**
 * Prepare cassandra
 *
 * API REF: https://docs.datastax.com/en/developer/nodejs-driver/4.6/api/class.Client/
 */
async function prep(){
  try {
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
  } finally {
    await C.shutdown();
  }
}


// Upon startup, prepare the database
prep();

// Start a simple REST server
// TAOTODO



