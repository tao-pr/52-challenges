FROM centos:7
COPY src/daemon.c mydaemon/src/
COPY Makefile mydaemon/
COPY daemon36.service mydaemon/
WORKDIR mydaemon
RUN \
  yum install make gcc -y && \
  mkdir -p bin &&  \
  mkdir -p /home/monitor && \
  echo "make all ..." && \
  echo 'pwd    = ' $(pwd) && \
  echo 'whoami =' $(whoami) && \
  ls -l && \
  make all && \
  echo "make start ..." && \
  make start

