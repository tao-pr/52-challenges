FROM centos:7
COPY src/daemon.c mydaemon/
COPY Makefile mydaemon/
WORKDIR mydaemon
RUN \
  yum install make gcc -y && \
  mkdir -p bin &&  \
  echo "make all ..." && \
  echo 'pwd    = ' $(pwd) && \
  echo 'whoami =' $(whoami) && \
  ls -l && \
  make all && \
  echo "make start ..." && \
  make start

