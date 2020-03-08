#include "motorShieldControl.h"
//#include "ultrasonic.h"
#include "serialArduino.h"

bool progStop = true;
int spd = 175;

void setup(){
  //initUS();
  initSerial();
  initMotorshield();
  initLineTrace();
  Serial.println("Finished Setup");
  delay(2000);
  digitalWrite(13, HIGH);
  delay(100);
  digitalWrite(13, LOW);
}

void loop(){
  struct movement comm = readPi();
    Serial.println("Stuck1");
    
    if (comm.mag == 998){progStop = true; Serial.println("Stuck2");}
    else if (comm.mag == 999) { progStop = false; digitalWrite(LED_BUILTIN, HIGH); Serial.println("Stuck3");}
    else if (progStop){
      Serial.println("Stuck5");
      if (comm.MoT == 1){
        Serial.println("Stuck6");
        pointTurn(comm.dir, comm.mag, spd);
      }
      else if (comm.MoT == 0){
        Serial.println("Stuck7");
        if (comm.dir == 0){
          backward(comm.mag, spd);
        } else {
          straight(comm.mag, spd);
        }
      }
    }
    
 if (!progStop){
    Serial.println("Not running");
    lineTrace();
    //digitalWrite(13, HIGH);
  }
}
