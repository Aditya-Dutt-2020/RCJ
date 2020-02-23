#include "motorSheildControl.h"
#include "ultrasonic.h"
#include "serialArduino.h"

bool progStop = false;
int spd = 175;

void setup(){
  initUS();
  initMotorshield();
  initSerial();
}

void loop(){
  movement comm = readPi();
  if (comm.mag != 997){
    if (comm.mag == 998){ progStop = true;}
    else if (comm.mag == 999) { progStop = false; }
    else if (progStop){
      if (comm.MoT == 1){
        pointTurn(comm.dir, comm.mag, spd);
      }
      else if (comm.MoT == 0){
        if (comm.dir == 0){
          backward(comm.mag, spd)
        } else {
          straight(comm.mag, spd)
        }
      }
    }
  }
  if (not progStop){
    lineTrace();
    
  }
}
