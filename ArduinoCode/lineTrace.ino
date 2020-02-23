#include <QTRSensors.h>
#include "pin.h"
#include "motorShieldControl.h"
#include "lineTrace.h"
#include "Serial.h"
QTRSensors qtr;

const uint8_t SensorCount = 8;
uint16_t sensorValues[SensorCount];

#define LEFT 0
#define RIGHT 1
#define kP 20
#define tP 128
#define kD 70

bool white = 1;
int lastError = 0;
void initLineTrace()
{
  initMotorshield();
  Serial.begin(115200);
  // configure the sensors
  qtr.setTypeRC();  
  qtr.setSensorPins((const uint8_t[]){LA0, LA1, LA2, LA3, LA4, LA5, LA6, LA7}, SensorCount);
   pinMode(LED_BUILTIN, OUTPUT);
   digitalWrite(LED_BUILTIN, HIGH);
  // 2.5 ms RC read timeout (default) * 10 reads per calibrate() call
  // = ~25 ms per calibrate() call.
  // Call calibrate() 400 times to make calibration take about 10 seconds.
  for (uint16_t i = 0; i < 200; i++)
  {
    qtr.calibrate();
  }
  digitalWrite(LED_BUILTIN, LOW);
  pinMode(RIGHT, OUTPUT);
  pinMode(LEFT, OUTPUT);
  setSpeeds(0, 0);
  runMotors(FORW);
}

uint16_t readSensor(int i){
  qtr.read(sensorValues);
  return sensorValues[i];
}


void lineTrace()
{
  struct Movement localComm = readPi();
  if(localComm.mag == 999)
  {
 
  Serial.println(localComm.mag);
  qtr.read(sensorValues);
  uint16_t turnPos;
  uint16_t pos = qtr.readLineBlack(sensorValues);
  int  error = pos-(3500);
  int adjP =error/kP; 
  //int adjD = (error-lastError)/kD;
  int correction = adjP;
  int lms, rms;
//  Serial.println(tP-correction);
  if (error > 3000)
  {
//     Serial.println("Running1");
     lms = (abs(tP+correction)) > 255 ? 255 : (abs(tP+correction));
     rms = (abs(-tP-correction)) > 255 ? 255 : (abs(-tP-correction));
  }else if(error < -3000)
  {
//    Serial.println("Running2");
     lms = (abs(-tP+correction)) > 255 ? 255 : (abs(-tP+correction));
     rms = (abs(tP-correction)) > 255 ? 255 : (abs(tP-correction));
  }else
  {
   //Serial.println("Running3");
   lms = (abs(tP+correction)) > 255 ? 255 : (abs(tP+correction));
   rms = (abs(tP-correction)) > 255 ? 255 : (abs(tP-correction));
  }

  setSpeeds(lms, rms);
  proportionalTurn(((tP + correction) < 0) ? BACK : FORW, ((tP - correction) < 0) ? BACK : FORW);

  if (pos == 0)
  {

    setSpeeds(0, 0);
    runMotors(FORW);
    straight(3, 255);
    pointTurn(LEFT, 90, 255);
   backward(1, 255);
   qtr.read(sensorValues);

    delay(2000);
    if (qtr.readLineBlack(sensorValues) == 7000 || qtr.readLineBlack(sensorValues) == 0)
    {

      straight(2, 255);
      pointTurn(RIGHT, 90, 255);
      while(qtr.readLineBlack(sensorValues) == 7000 ||qtr.readLineBlack(sensorValues) == 0)
      {
        setSpeeds(75, 75);
        runMotors(FORW);
      }

      continue;
    }
    delay(200);
    
  }
  if (pos == 7000)
  {
//    Serial.println("Right Turn");
    setSpeeds(0, 0);
    runMotors(FORW);
    straight(3, 255);
    pointTurn(RIGHT, 90, 255);
    backward(1, 255);
    //Serial.print("This is the end of a right turn; This is what I see: ");
    qtr.read(sensorValues);
    turnPos = qtr.readLineBlack(sensorValues);
//    Serial.println(turnPos);
    delay(2000);
    if (turnPos == 7000 || turnPos == 0)
    {
 //     Serial.println("never mind, no Right turn, just a gap");
      straight(2,255);
      pointTurn(LEFT, 90, 255);
      qtr.read(sensorValues);
      while(qtr.readLineBlack(sensorValues) == 7000 ||qtr.readLineBlack(sensorValues) == 0)
      {
        setSpeeds(75, 75);
        runMotors(FORW);
      }
//      Serial.println("Back on line after right turn");
      continue;
    }
    delay(200);
  }
  
  //Serial.println(pos);
  lastError = error;
  qtr.read(sensorValues);
  
  /*for (uint8_t i = 0; i < SensorCount; i++)
  {
    if(sensorValues[i] >= 200)
    {
      white = 0;
    }
  }*/
  white = 1;
    
}
