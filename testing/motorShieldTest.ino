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

}
const int tnum = 1;

void loop() {
  switch (tnum){
  case 1:
    rightMotor(FORW, 50);
    leftMotor(FORW, 50);
    delay(100)
    rightMotor(FORW, 60);
    leftMotor(FORW, 60);
    delay(100)
    rightMotor(FORW, 70);
    leftMotor(FORW, 70);
    delay(100)
    rightMotor(FORW, 80);
    leftMotor(FORW, 80);
    delay(100)
    rightMotor(FORW, 90);
    leftMotor(FORW, 90);
    delay(100)
    rightMotor(FORW, 95);
    leftMotor(FORW, 95);
    delay(100)
    rightMotor(FORW, 100);
    leftMotor(FORW, 100);
    delay(1000);
    rightMotor(BACK, 100);
    leftMotor(BACK, 100);
    delay(1000);
    stopAllMotors();
    break;
  case 2:
    straight(100, 100);
    stopAllMotors();
    break;
  case 3:
    straight(100, 100);
    backward(100, 100);
    stopAllMotors();
    break;
  case 4:
    pointTurn(LEFT, 90, 100)
    pointTurn(RIGHT, 90, 100)
    break;
  }
 
}
