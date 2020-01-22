#include <QTRSensors.h>
#include "pin.h"
#include "motorShieldControl.h"
QTRSensors qtr;

const uint8_t SensorCount = 8;
uint16_t sensorValues[SensorCount];

#define LEFT 0
#define RIGHT 1
#define kP 70
#define tP 50
#define kD 70

bool white = 1;
int lastError = 0;
void setup()
{
  // configure the sensors
  qtr.setTypeRC();
  qtr.setSensorPins((const uint8_t[]){LA0, LA1, LA2, LA3, LA4, LA5, LA6, LA7}, SensorCount);

  // 2.5 ms RC read timeout (default) * 10 reads per calibrate() call
  // = ~25 ms per calibrate() call.
  // Call calibrate() 400 times to make calibration take about 10 seconds.
  for (uint16_t i = 0; i < 200; i++)
  {
    qtr.calibrate();
  }
  pinMode(RIGHT, OUTPUT);
  pinMode(LEFT, OUTPUT);
}

void go(float seconds, int spd)
{
  setMotor(LEFT, spd);
  setMotor(RIGHT, spd);
  delay(seconds);
  setMotor(LEFT, 0);
  setMotor(RIGHT, 0);
}
void loop()
{
  uint16_t position = qtr.readLineBlack(sensorValues);
  int  error = position-(3500);
  int adjP =error/kP; 
  int adjD = (error-lastError)/kD;
  int correction = adjP + adjD;
  porportionalTurn(FORW, (tP-correction), (tP+correction));
  
  lastError = error;
  qtr.read(sensorValues);
  
  for (uint8_t i = 0; i < SensorCount; i++)
  {
    if(sensorValues[i] >= 200)
    {
      white = 0;
    }
  }
  
  if(white == 1)
  {
    stopAllMotors();
    leftMotor(BACK, 50);
    rightMotor(BACK, 50);
    delay(250);
    stopAllMotors();
    
    qtr.read(sensorValues);
    if(sensorValues[7] >=500)
    {
      leftMotor(FORW, 100);
      rightMotor(BACK, 100);
      delay(300);
      stopAllMotors();
    }
    else if(sensorValues[0] >=500)
    {
      leftMotor(BACK, 100);
      rightMotor(FORW, 100);
      delay(300);
      stopAllMotors();
    }
    else
    {
      leftMotor(FORW, 200);
      rightMotor(FORW, 200);
      delay(50);
      stopAllMotors();
      qtr.read(sensorValues);
      while(sensorValues[4] <=200)
      {
        qtr.read(sensorValues);
        leftMotor(FORW, 200);
        rightMotor(FORW, 200);
        delay(50);
        WSstopAllMotors();
      }
    }
  }
  white = 1;
  Serial.println(position);
}
