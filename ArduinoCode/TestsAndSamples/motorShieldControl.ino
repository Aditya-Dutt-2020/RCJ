/*
 * 
 * Motor, servo, and encoder control.
 * Include this code to interface with the servo and motors with or without encoders
 * Made by Mannan Bhardwaj
 * WIP
 * 
 */


#include "motorShieldControl.h"
#include "pin.h"

// init variables
uint32_t lastStateL = 0;
uint32_t curStateL = 0;
uint32_t stateCountL=0;
uint32_t lastStateR = 0;
uint32_t curStateR = 0;
uint32_t stateCountR=0;

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
  camServo.attach(servoCam);
  camServo.write(0);
  delay(15);
  // attatch interrupts for encoders
  attachInterrupt(digitalPinToInterrupt(encPinL), encLChange, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encPinR), encRChange, CHANGE);
}

void rightMotor(int dir, int pwm){
  // Takes speed from 0-100 and direction and moves motor accordingly
  RMotor->setSpeed(pwm);
  RMotor->run(dir);
}

void leftMotor(int dir, int pwm){
  // Takes speed from 0-100 and direction and moves motor accordingly
  LMotor->setSpeed(pwm);
  LMotor->run(dir);
}

void stopAllMotors(){
  rightMotor(RELEASE, 0);
  leftMotor(RELEASE, 0);
}

void proportionalTurn(int dir, int rpwm, int lpwm){
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
float *getCentimeters(){
  // gets amount of centimeters moved from encoders since startEncoders(); was called.
  //startEncoders();
  float cl = stateCountL*distancePerState;
  float cr = stateCountR*distancePerState;
  float *arr;
  arr = malloc(2 * sizeof(*arr));
  // return centimeters ran for each motor.
 /* Serial.print(cl);
  Serial.print("   ");
  Serial.print(cr);
  Serial.print("   ");
  Serial.println(circum/statesPerRotation);*/
  arr[0] = cl;
  arr[1] = cr;
  return arr;
}

float convertToEnc(int deg){
  // get amount of degrees turned since startEncoders was called
  //startEncoders();
  // convert to degrees and return
  return degreePerStates*deg;
}

void straight(int cent, int pwm){
  // go straight an amount of centimeters
  startEncoders(); // init encoders
  float *enc;
  enc = getCentimeters();
  // go forward while encoders allow
  while (enc[0] <= cent and enc[1] <= cent){
    Serial.print(enc[0]);
    Serial.print("   ");
    Serial.println(enc[1]);
    rightMotor(FORWARD, pwm);
    leftMotor(FORWARD,  pwm);
    enc = getCentimeters();
  }
  // stop motors
  rightMotor(FORWARD, 0);
  leftMotor(FORWARD,  0);
  free(enc);
}

void backward(int cent, int pwm){
  // go backwards an amount of centimeters
  startEncoders(); // init encoders
  float* enc;
  enc = getCentimeters();
  // keep going until goal reached
  while (enc[0] <= cent and enc[1] <= cent){
    Serial.print(enc[0]);
    Serial.print("   ");
    Serial.println(enc[1]);
    rightMotor(BACKWARD, pwm);
    leftMotor(BACKWARD,  pwm);
    enc = getCentimeters();
  }
  // stop motors
  rightMotor(BACKWARD, 0);
  leftMotor(BACKWARD,  0);
}

//void pointTurn(int dir, int ang, int pwm){
//  // point turn some amount of degrees in a certain direction
//  startEncoders(); //init encoders
//  int degenc = convertToEnc(ang)
//  // keep osn turning until goal reached
//  while (stateCountR < degenc){
////    Serial.println(deg);
//    if (dir == RIGHT){
//      leftMotor(FORWARD, pwm);
//      rightMotor(BACKWARD, pwm);
//    }
//    if (dir == LEFT){
//      leftMotor(BACKWARD, pwm);
//      rightMotor(FORWARD, pwm);
//    }
//  }
//  // stop motors
//  leftMotor(FORWARD, 0);
//  rightMotor(FORWARD,0); 
//}
void pointTurn(int dir, float ang, int pwm){
  // point turn some amount of degrees in a certain direction
  startEncoders(); //init encoders
  float FracTurn = ang/360;
  float distNeeded = FracTurn * circumOfRobot;
  Serial.println(90/360);
  // keep on turning until goal reached
  while (stateCountR < (statesPerCm*distNeeded)){
//    Serial.println(deg);
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
  Serial.print("   ");
  Serial.println(stateCountR);
}
