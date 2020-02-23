#include <Wire.h>
#include <Servo.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

#ifndef MOTORSHIELDH
#define MOTORSHIELDH

// init constansts.
#define circum 18.22 
#define WB 19
#define statesPerRotation 1800
#define distancePerState (circum/statesPerRotation)
#define statesPerCm (statesPerRotation/circum)
#define degreePerStates (WB/5.8)
#define circumOfRobot (WB*PI)


// use this to find out dir in turns
#define RIGHT 1
#define LEFT 0
#define FORW FORWARD
#define BACK BACKWARD

// predef funcs
void initMotorshield(); //initialize motor shield and servo
void rightMotor(int dir); // turn on right motor
void leftMotor(int dir); //turn on left motor
void setSpeeds(int lpwm, int rpwm);  // set the speeds
void porportionalTurn(int Ldir, int Rdir); //Does a porportional turn
void startEncoders(); // Start/reset encoders to be used
float* getCentimeters(); // get amount of centimeters moved since startEncoders() was called
float getDegrees(); // get amount of degrees turned since startEncoders() was called
void straight(int cent, int pwm); // go straight an amount of centimeters
void backward(int cent, int pwm); // ditto above but backwards
void pointTurn(int dir, float ang); // Do a point turn left or right a certain number of degrees
void turnServo(int deg); // set the servo to a certain degree.



#endif
