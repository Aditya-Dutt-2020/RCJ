

#include "motorShieldControl.h"
#include "ultrasonic.h"

uint16_t sensorValues1[8];

void setup() {
 initMotorshield();
 initUS();
 initLineTrace();
 setSpeeds(100, 100);

}
long dist;
void loop() {
  dist = getDist();
  if (dist < 5){
    // avoid time.
    pointTurn(RIGHT, 45);
    straight(10);
    pointTurn(LEFT, 45);
    for (int i; i < 8; i++){
      sensorValues1[i] = readSensor(i);
    }
    
    while (sensorValues1[4] < 127 and sensorValues1[5] < 127){
      for (int i; i < 8; i++){
        sensorValues1[i] = readSensor(i);
      }
    }
  }

}
