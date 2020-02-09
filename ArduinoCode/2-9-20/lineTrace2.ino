#include <QTRSensors.h>
#include "pin.h"
#include "motorShieldControl.h"
QTRSensors qtr;

const uint8_t SensorCount = 8;
uint16_t sensorValues[SensorCount];

#define LEFT 0
#define RIGHT 1
#define kP 30
#define tP 128
#define kD 70

bool white = 1;
int lastError = 0;
void setup()
{
  Serial.begin(9600);
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
void loop()
{

  uint16_t position = qtr.readLineBlack(sensorValues);
  int  error = position-(3500);
  int adjP =error/kP; 
  //int adjD = (error-lastError)/kD;
  
  int correction = adjP;
  setSpeeds(255, 255);
  delay(500);
  for (uint8_t i = 0; i < SensorCount; i++)
  {
    Serial.print(sensorValues[i]);
    Serial.print('\t');
  }
  Serial.print(position);
  Serial.print('\t');
  Serial.println(correction);

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
