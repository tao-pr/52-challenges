# RestAPI for fun

This project is created via `stack new restapi`


## Build and run

Uses `stack` to build and run

```sh
stack build
stack run
```

Try it out 

```bash
curl -XPOST localhost:3333/validate \
  -H 'Content-Type: application/json' \
  -d '{"sessionId":"12345", "zipped": ""}' | jq .
```

When posting to "/zip" endpoint, the JSON payload needs to 
contain "tag" as [Null|Unzipped], so JSON package can parse it

```bash
curl -XPOST localhost:3333/zip \
  -H 'Content-Type: application/json' \
  -d '{"token":"aaa", "date":"2022-01-03", "amount": 250, "tag": "Unzipped"}' | jq .
```

Test unzipping data

```bash
curl -XPOST localhost:3333/extract \
  -H 'Content-Type: application/json' \
  -d '{"sessionId": "foo", "zipped": "\\x31\\x139\\x8\\x0\\x0\\x0\\x0\\x0\\x0\\x19\\x171\\x86\\x74\\x204\\x205\\x47\\x205\\x43\\x81\\x178\\x50\\x208\\x81\\x74\\x73\\x44\\x73\\x85\\x178\\x82\\x50\\x50\\x48\\x50\\x210\\x53\\x48\\x212\\x53\\x48\\x86\\x210\\x81\\x42\\x73\\x76\\x7\\x10\\x133\\x230\\x85\\x101\\x22\\x20\\x164\\x166\\x128\\x4\\x242\\x179\\x83\\x243\\x128\\x66\\x217\\x198\\x134\\x74\\x181\\x0\\x6\\x164\\x78\\x167\\x63\\x0\\x0\\x0"}'
```


## Test

The project doesn't have a runnable unittest


## Licence

MIT