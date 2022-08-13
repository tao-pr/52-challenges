/**
 * Daemon task 
 */

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include <time.h>
#include <dirent.h>
#include <errno.h>
#include <systemd/sd-journal.h>

void sigHandler(int sig){
  if (sig==SIGTERM){
    // exit cleanly
    printf("Terminating daemon36");
    exit(0);
  }
  else if (sig==SIGHUP){
    // reload config
    printf("Reloading config daemon36");
  }
}

int main(){

  char monitorDir[] = "/home/monitor/";

  // add signal handler
  printf("Initialising daemon36");
  struct sigaction action;
  action.sa_handler = sigHandler;
  sigfillset(&action.sa_mask);
  action.sa_flags = SA_RESTART;
  sigaction(SIGTERM, &action, NULL);
  sigaction(SIGUSR1, &action, NULL);
  sigaction(SIGHUP, &action, NULL);

  while (1){
    time_t now;
    time(&now);

    // check dir
    printf("%s [iteration]", ctime(now));
    DIR* dir = opendir(monitorDir);
    if (dir){
      closedir(dir);
      // check files inside
      char fullpath[256];
      struct dirent *p;
      while ((p = readdir(dir)) != NULL) {
        snprintf(fullpath, sizeof(fullpath), "%s%s", monitorDir, p->d_name);
        printf("--> %s\n", fullpath); // taodebug:
      }
    }
    else {
      // fail to opendir for some reason
      fprintf(stderr, "%s cannot be opened", monitorDir);
    }

    fflush(stdout);
    sleep(500);
  }

  return 0;
}