/**
 * Daemon task 
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <syslog.h>

// http://www.netzmafia.de/skripten/unix/linux-daemon-howto.html

static void run_fork(pid_t* pid){
  // Fork off the parent process
  *pid = fork();
  if (*pid < 0){
    exit(EXIT_FAILURE);
  }
  /* If we got a good PID, then
     we can exit the parent process. */
  if (*pid > 0){
    exit(EXIT_SUCCESS);
  }
}

static void run_umask(){
  umask(0);
}

static void run_logs(){
  // taotodo:

}

static void run_sid_creation(pid_t *sid){
  // taotodo:
  *sid = setsid();
  if (*sid < 0) {
    // todo: log failure
    exit(EXIT_FAILURE);
  }
}

static void run_chdir(){
  if ((chdir("/")) < 0){
    exit(EXIT_FAILURE);
  }
}

static void run_stdfile_closure(){
  close(STDIN_FILENO);
  close(STDOUT_FILENO);
  close(STDERR_FILENO);
}

int main(){
  // step 1: make daemon autonomous by forking a child process
  pid_t pid;
  run_fork(&pid);
  // step 2: change filemode, so it can write any files
  run_umask();
  // step 3: open syslogs for writing
  run_logs();
  // step 4: create sid
  pid_t sid;
  run_sid_creation(&sid);
  // step 5: change working dir to root to avoid variations of distributions
  run_chdir();
  // step 6: close standard file descriptors
  run_stdfile_closure();

  while (1){
    // taotodo: daemon logic

    syslog(LOG_NOTICE, "Daemon started.");
    sleep(10);
    break;
  }

  syslog(LOG_NOTICE, "Daemon terminated.");
  closelog();

  return EXIT_SUCCESS;
}