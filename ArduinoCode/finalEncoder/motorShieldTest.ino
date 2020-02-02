#include "motorShieldControl.h"
/*
 * Testing from Motor Shield stuffs
 * Put the number in the variable "tnum"
 * 1 --  Simple forward/backward motor test
 * 2 --  Straight encoder test -- 100 centimeters
 * 3 --  Straight and backwards encoder test -- 100 centimeters
 * 4 --  Point turn test -- turns 90 degrees, then back
 * NOTE: MAKE SURE EVERYTHING IS WHAT IT SHOULD BE -- 90 DEGREES WHEN TURNING AND 100 WHEN GOING STRAIGHT OR BACKWARD!!!!!
 *       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 *       READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ 
 */
void setup() {
  initMotorshield();
  Serial.begin(9600);
  startEncoders();
}
const int tnum = 4;

void loop() {
  switch (tnum){
  case 1:
    leftMotor(FORW, 255);
    rightMotor(FORW, 255);
   

    testEncoder();

   /* rightMotor(BACK, 100);
    leftMotor(BACK, 100);
    Serial.println(BACK);
    delay(1000);*/

    break;
  case 2:
  delay(3000);
    backward(20, 255);
    stopAllMotors();
    delay(5000);
    break;
  case 3:
    straight(20, 255);
    backward(20, 255);
    stopAllMotors();
    break;
  case 4:
    //delay(4000);
    pointTurn(LEFT, 1800.0f, 255);
    delay(5000);
    //pointTurn(RIGHT, 90, 255);
    break;
  }
 
}
