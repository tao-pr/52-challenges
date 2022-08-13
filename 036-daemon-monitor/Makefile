all: src/daemon.c
	$(CC) -o bin/daemon36 $?

check:
	systemctl -l status daemon36

log:
	journalctl -u daemon36

start:
	systemctl daemon-reload
	systemctl start daemon36

stop:
	systemctl stop daemon36

