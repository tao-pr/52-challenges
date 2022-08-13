FROM centos:7
COPY src/daemon.c mydaemon/src/
COPY Makefile mydaemon/
COPY daemon36.service mydaemon/
WORKDIR mydaemon
RUN \
  (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
  systemd-tmpfiles-setup.service ] || rm -f $i; done); \
  rm -f /lib/systemd/system/multi-user.target.wants/*;\
  rm -f /etc/systemd/system/*.wants/*;\
  rm -f /lib/systemd/system/local-fs.target.wants/*; \
  rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
  rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
  rm -f /lib/systemd/system/basic.target.wants/*;\
  rm -f /lib/systemd/system/anaconda.target.wants/*; \
  yum install make gcc -y && \
  mkdir -p bin &&  \
  mkdir -p /home/monitor && \
  echo "make all ..." && \
  echo 'pwd    = ' $(pwd) && \
  echo 'whoami =' $(whoami) && \
  ls -l && \
  make all && \
  echo "make all [DONE]" && \
  cp daemon36.service /etc/systemd/system/ && \
  echo "daemon36.service installed" && \
  alias ll=ls
CMD /usr/sbin/init

