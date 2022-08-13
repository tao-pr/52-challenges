# Daemon for monitoring

Experiment with monitoring from kernel, following style of [systemd daemon](http://0pointer.de/public/systemd-man/daemon.html#New-Style%20Daemons)

## Key features of Systemd daemon

- Unlike old style of daemon (SysV), it doesn't need to fork or close all standard file descriptors.
- Uses stdout for logging via systemd (unlike SysV which we have to use SysV log instead)
- Backward compatible with SysV
- Designed for higher parallelism

## Build & Run

The project is crafted to build and run on Linux distro, so first off, you need to build the docker with following

```bash
docker build -t centos .
```

Then start the docker with privilege so it can run daemon with `systemd` and bind TTY. 
Note that the daemon is started with name `daemon36`.

```bash
docker run -it --rm -d --privileged centos
````

Once container started, you can tunnel TTY normally and start the daemon

```bash
docker exec -it {CONTAINER_ID} /bin/sh
> make start
> systemctl list-units
```

You can simply inspect log with

```bash
make log

# or follow with
journalctl -u daemon36 -f
```

And stop the process with

```bash
make stop
```


## References

- [Systemd design blog post](http://0pointer.de/blog/projects/systemd.html)
- [Systemd info from Suse documentation](https://documentation.suse.com/sles/12-SP4/html/SLES-all/cha-systemd.html#)
- https://subscription.packtpub.com/book/programming/9781789951288/7/ch07lvl1sec74/creating-a-more-modern-daemon-for-systemd


## Licence

TBD
