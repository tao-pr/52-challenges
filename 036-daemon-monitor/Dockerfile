FROM centos:7
COPY src/daemon.c mydaemon/
COPY Makefile mydaemon/
COPY make-run.sh mydaemon/
RUN yum update && mydaemon/make-run.sh

