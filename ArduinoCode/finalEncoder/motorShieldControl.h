  
#ifndef MOTORSHIELDH
#define MOTORSHIELDH

// init constansts.
#define circum 18.22 
#define WB 21
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
void rightMotor(int dir, int pwm); // turn on right motor
void leftMotor(int dir, int pwm); //turn on left motor
void porportionalTurn(int dir, int rpwm, int lpwm); //Does a porportional turn
void startEncoders(); // Start/reset encoders to be used
float* getCentimeters(); // get amount of centimeters moved since startEncoders() was called
float getDegrees(); // get amount of degrees turned since startEncoders() was called
void straight(int cent, int pwm); // go straight an amount of centimeters
void backward(int cent, int pwm); // ditto above but backwards
void pointTurn(int dir, int ang, int pwm); // Do a point turn left or right a certain number of degrees
void turnServo(int deg); // set the servo to a certain degree.



#endif
