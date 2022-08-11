/**
 * Daemon task 
 */

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include <time.h>

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


  while (1){
    time_t now;
    time(&now);

    fflush(stdout);
    sleep(50);
  }

  return 0;
}