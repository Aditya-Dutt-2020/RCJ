//#include "motorShieldControl.h"
///*
// * Testing from Motor Shield stuffs
// * Put the number in the variable "tnum"
// * 1 --  Simple forward/backward motor test
// * 2 --  Straight encoder test -- 100 centimeters
// * 3 --  Straight and backwards encoder test -- 100 centimeters
// * 4 --  Point turn test -- turns 90 degrees, then back
// * NOTE: MAKE SURE EVERYTHING IS WHAT IT SHOULD BE -- 90 DEGREES WHEN TURNING AND 100 WHEN GOING STRAIGHT OR BACKWARD!!!!!
// *       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
// *       READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ 
// */
//void setup() {
//  initMotorshield();
//  Serial.begin(9600);
//  startEncoders();
//}
//const int tnum = 1;
//
//void loop() {
//  while(1)
//  {
//
//    setSpeeds(255, 255);
//    runMotors(FORW);
//  }
//  switch (tnum){
//  case 1:
//      
//  
//     /* rightMotor(BACK, 100);
//      leftMotor(BACK, 100);
//      Serial.println(BACK);
//      delay(1000);*/
//  
//      break;
//  case 2:
//  Serial.println("Starting");
//  setSpeeds(0, 0);
//    Serial.println("Did Step1");
//  runMotors(FORW);
//      Serial.println("Did Step2");
//  delay(3000);
//      Serial.println("Did Step3");
//  setSpeeds(abs((128+220)), abs((128-220)));
//        Serial.println("Did Step4");
//  proportionalTurn(((128+220) < 0) ? BACK : FORW, ((128-220) < 0) ? BACK : FORW);
//      Serial.println("Did Step5");
//    delay(5000);
//        Serial.println("Did Step6");
//    break;
//  case 3:
//    straight(20, 255);
//    backward(20, 255);
//    stopAllMotors();
//    break;
//  case 4:
//    //delay(4000);
//    Serial.println("Went again");
//    pointTurn(RIGHT, 90);
//
//    delay(5000);
//    //pointTurn(RIGHT, 90, 255);
//    break;
//  }
// 
//}
