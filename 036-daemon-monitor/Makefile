all: src/daemon.c
	$(CC) -o bin/daemon36 $?

start:
	systemctl start daemon36

check:
	ps xj | head -1
	@ps xj | grep daemon36

log:
	grep daemon36 /var/log/syslog | tail

