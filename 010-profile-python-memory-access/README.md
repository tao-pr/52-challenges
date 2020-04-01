# Profiling Memory Access in Python 3.7

Run the preset profiling

```bash

$ mprof run python3 -m memory_profile.mem INPLACE
$ mprof run python3 -m memory_profile.mem NEW_ARRAY_SAME_REF

```

## Memory profiling

![inplace](plots/mem-inplace.png)
![newarry](plots/mem-newarray.png)


## Pickle vs Joblib

To run

```bash
$ mprof run python3 -m memory_profile.serialise JOBLIB WRITE
$ mprof run python3 -m memory_profile.serialise JOBLIB READ

$ mprof run python3 -m memory_profile.serialise JOBLIB-COMPRESS WRITE
$ mprof run python3 -m memory_profile.serialise JOBLIB-COMPRESS READ

$ mprof run python3 -m memory_profile.serialise PICKLE WRITE
$ mprof run python3 -m memory_profile.serialise PICKLE READ

```

Space usage

```
 76M  joblib
 15M  joblib-compressed
 76M  pickle
```

Writing memory & time comparison

![m](plots/joblib-write.png)
![m](plots/joblib-compress-write.png)
![m](plots/pickle-write.png)

Reading memory & time comparison

![m](plots/joblib-read.png)
![m](plots/joblib-compress-read.png)
![m](plots/pickle-read.png)


## Licence

MIT