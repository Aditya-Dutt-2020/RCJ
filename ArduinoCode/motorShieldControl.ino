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
int camServoDeg = 180;
int camAdd = 180;

void initMotorshield()
{
  // connect to the motor shield
  AFMS.begin();
  // set pin mode
  pinMode(encPinL, INPUT);
  pinMode(encPinR, INPUT);
  // connect to camera servo
  camServo.attach(servoPin);
  camServo.write(0);
  delay(15);
  // attatch interrupts for encoders
  attachInterrupt(digitalPinToInterrupt(encPinL), encLChange, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encPinR), encRChange, CHANGE);
}

void rightMotor(int dir, int pwm){
  // Takes speed from 0-100 and direction and moves motor accordingly
  //pwm = pwm * (255/100);
  RMotor->setSpeed(pwm);
  RMotor->run(dir);
}

void leftMotor(int dir, int pwm){
  // Takes speed from 0-100 and direction and moves motor accordingly
  //pwm = map(pwm, 0, 100, 0, 255);
  LMotor->setSpeed(pwm);
  LMotor->run(dir);
}



void porportionalTurn(int dir, int rpwm, int lpwm){
  // takes two speeds for each motor and turns one forward and one backward depending on {dir} variable
  if (dir == FORW){
    leftMotor(FORWARD, lpwm);
    rightMotor(FORWARD, rpwm);
  }
  if (dir == BACK){
    leftMotor(BACKWARD, lpwm);
    rightMotor(BACKWARD, rpwm);
  }
}

void encLChange(){
  stateCountL += 1;
}

void encRChange(){
  stateCountR += 1;
}

void startEncoders(){
  // initializes encoders /w variables
  stateCountL = 0;
  stateCountR = 0;
}
float* getCentimeters(){
  // gets amount of centimeters moved from encoders since startEncoders(); was called.
  //startEncoders();
  float cl = stateCountL/statesPerCentimeter;
  float cr = stateCountR/statesPerCentimeter;
  // return centimeters ran for each motor.
  float arr[2] = {cl, cr};
  return &arr[0];
}

float getDegrees(){
  // get amount of degrees turned since startEncoders was called
  //startEncoders();
  // convert to degrees and return
  float deg = (stateCountR/statesPerDegree + stateCountL/statesPerDegree)/2; // take average degrees
  return deg;
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
  float* enc = getCentimeters();
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
  float deg = getDegrees();
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

void turnServo(int dir, int deg, int inHowManyMSPerDeg=15){
  if (dir == RIGHT){
    camAdd = 1;
  } else {
    camAdd = -1;
  }
  for (int i; i<deg; i++){
    camServo.write(camServoDeg);
    delay(inHowManyMSPerDeg);
    camServoDeg += camAdd;
  }
}
int pos =0;
void testServo(){
  turnServo(LEFT, 90);
  //delay(30);
  turnServo(RIGHT, 90);
  turnServo(LEFT, 180);
  turnServo(RIGHT, 180);
}

void testEncoder(){
  Serial.print(stateCountL);
  Serial.println(stateCountR);
}
