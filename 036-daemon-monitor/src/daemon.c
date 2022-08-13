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

  printf("Initialising daemon36");
  while (1){
    time_t now;
    time(&now);

    // check dir
    printf("[iteration]");
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