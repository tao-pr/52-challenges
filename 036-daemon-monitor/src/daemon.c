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

  // add signal handler
  printf("Initialising daemon36\n");
  struct sigaction action;
  action.sa_handler = sigHandler;
  sigfillset(&action.sa_mask);
  action.sa_flags = SA_RESTART;
  sigaction(SIGTERM, &action, NULL);
  sigaction(SIGUSR1, &action, NULL);
  sigaction(SIGHUP, &action, NULL);

  printf("Ready\n");
  while (1){
    time_t now;
    time(&now);

    // check dir
    printf("%s [iteration]\n", ctime(&now));
    DIR* dir = opendir(monitorDir);
    if (dir){
      printf("Monitoring %s\n", monitorDir);
      // check files inside
      char fullpath[256];
      struct dirent *p;
      while ((p = readdir(dir)) != NULL) {
        // skip . and ..
        if (p->d_name[0] == '.')
          continue;
        snprintf(fullpath, sizeof(fullpath), "%s%s", monitorDir, p->d_name);
        printf("seen ==> %s\n", fullpath);
      }
      closedir(dir);
    }
    else {
      // fail to opendir for some reason
      fprintf(stderr, "%s cannot be opened\n", monitorDir);
    }

    printf("end of iteration");
    fflush(stdout);
    sleep(500);
  }

  return 0;
}