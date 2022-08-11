# Daemon for monitoring

Experiment with monitoring from kernel, following style of [systemd daemon](http://0pointer.de/public/systemd-man/daemon.html#New-Style%20Daemons)

## Key features of Systemd daemon

- Unlike old style of daemon (SysV), it doesn't need to fork or close all standard file descriptors.
- Uses stdout for logging via systemd (unlike SysV which we have to use SysV log instead)
- Backward compatible with SysV
- Designed for higher parallelism



## Build & Run

This code is crafted for Linux. You can simply build and run this inside docker like so:

```bash
docker build .
```

## References

- [Systemd design blog post](http://0pointer.de/blog/projects/systemd.html)
- [Systemd info from Suse documentation](https://documentation.suse.com/sles/12-SP4/html/SLES-all/cha-systemd.html#)
- https://lloydrochester.com/post/c/unix-daemon-example/
- https://subscription.packtpub.com/book/programming/9781789951288/7/ch07lvl1sec74/creating-a-more-modern-daemon-for-systemd


## Licence

TBD
