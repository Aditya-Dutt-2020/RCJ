/*
 * 
 * Motor, servo, and encoder control.
 * Include this code to interface with the servo and motors with or without encoders
 * Made by Mannan Bhardwaj
 * WIP
 * 
 */

#include <Wire.h>
#include <Servo.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
#include "motorShieldControl.h"

// init variables
int lastStateL = 0;
int curStateL = 0;
int stateCountL=0;
int lastStateR = 0;
int curStateR = 0;
int stateCountR=0;

// INIT MOTORSHIELD
// create a motorshield object to be used
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
// create a pointer to the left and right motor
Adafruit_DCMotor *LMotor = AFMS.getMotor(1);
Adafruit_DCMotor *RMotor = AFMS.getMotor(2);

// Init servo
Servo camServo;

void init()
{
  // connect to the motor shield
  AFMS.begin();
  // set pin mode
  pinMode(encPinL, INPUT_PULLUP);
  pinMode(encPinR, INPUT_PULLUP);
  // connect to camera servo
  camServo.attatch(servoPin)
}

void rightMotor(int dir, int pwm){
  // Takes speed from 0-100 and direction and moves motor accordingly
  pwm = pwm * (255/100);
  RMotor->setSpeed(pwm);
  RMotor->run(dir);
}

void leftMotor(int dir, int pwm){
  // Takes speed from 0-100 and direction and moves motor accordingly
  pwm = pwm * (255/100);
  LMotor->setSpeed(pwm);
  LMotor->run(dir);
}



void porportionalTurn(int dir, int rpwm, int lpwm){
  // takes two speeds for each motor and turns one forward and one backward depending on {dir} variable
  if (dir == RIGHT){
    leftMotor(FORWARD, lpwm);
    rightMotor(BACKWARD, rpwm);
  }
  if (dir == LEFT){
    leftMotor(BACKWARD, lpwm);
    rightMotor(FORWARD, rpwm);
  }
}

void startEncoders(){
  // initializes encoders /w variables
  lastStateL  = digitalRead(encPinL);
  lastStateR  = digitalRead(encPinR);
  stateCountL = 0;
  stateCountR = 0;
}
float* getCentimeters(){
  // gets amount of centimeters moved from encoders since startEncoders(); was called.
  // must be called in a loop continuolsly
  curStateL = digitalRead(encPinL);
  curStateR = digitalRead(encPinR);
  // keep track of encoders
  if !(curStateL == lastStateL){
    stateCountL ++;
  }
  if !(curStateR == lastStateR){
    stateCountR ++;
  }
  // convert to centimeters
  cl = stateCountL/statesPerCentimeter
  cr = stateCountR/statesPerCentimeter
  // return centimeters ran for each motor.
  float arr[2] = {cl, cr};
  return *arr
}

float getDegrees(){
  // get amount of degrees turned since startEncoders was called
  // must be called continuosly in a loop
  curStateL = digitalRead(encPinL);
  curStateR = digitalRead(encPinR);
  // keep track of encoders
  if !(curStateL == lastStateL){
    stateCountL ++;
  }
  if !(curStateR == lastStateR){
    stateCountR ++;
  }
  // convert to degrees and return
  deg = (stateCountR/statesPerDegree + stateCountL/statesPerDegree)/2 // take average degrees
  return deg
}

void straight(int cent, int pwm){
  // go straight an amount of centimeters
  startEncoders(); // init encoders
  float* enc = getCentimeters();
  // go forward while encoders allow
  while (enc[0] <= cent and enc[1] <= cent){
    rightMotor(FORWARD, pwm);
    leftMotor(FORWARD,  pwm);
  }
  // stop motors
  rightMotor(FORWARD, 0);
  leftMotor(FORWARD,  0);
}

void backward(int cent, int pwm){
  // go backwards an amount of centimeters
  startEncoders(); // init encoders
  float* enc = getEncoders()
  // keep going until goal reached
  while (enc[0] <= cent and enc[1] <= cent){
    rightMotor(BACKWARD, pwm);
    leftMotor(BACKWARD,  pwm);
  }
  // stop motors
  rightMotor(BACKWARD, 0);
  leftMotor(BACKWARD,  0);
}

void pointTurn(int dir, int ang, int pwm){
  // point turn some amount of degrees in a certain direction
  startEncoders(); //init encoders
  float deg = getDegrees()
  // keep on turning until goal reached
  while (deg < ang){
    if (dir == RIGHT){
      leftMotor(FORWARD, pwm);
      rightMotor(BACKWARD, pwm);
    }
    if (dir == LEFT){
      leftMotor(BACKWARD, pwm);
      rightMotor(FORWARD, pwm);
    }
  }
  // stop motors
  leftMotor(FORWARD, 0);
  rightMotor(FORWARD,0);
}

void turnServo(int deg){
  camServo.write(deg)
}
