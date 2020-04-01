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

Space usage

```
 76M  joblib
 15M  joblib-compressed
 76M  pickle
```

Writing memory & time comparison

![m](plots/joblib-write)
![m](plots/joblib-compress-write)
![m](plots/pickle-write)

Reading memory & time comparison

![m](plots/joblib-read)
![m](plots/joblib-compress-read)
![m](plots/pickle-read)


## Licence

MIT