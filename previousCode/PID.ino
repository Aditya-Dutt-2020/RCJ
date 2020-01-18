#include <QTRSensors.h>
QTRSensors qtr;

const uint8_t SensorCount = 8;
uint16_t sensorValues[SensorCount];
#define motorL 6
#define RDir 4
#define LDir 7
#define motorR 5
#define button A7
#define mulR 1
#define mulL 0.97
#define LEFT 0
#define RIGHT 1
#define kP 70
#define tP 50
#define kD 70
int lastError = 0;
void setup()
{
  // configure the sensors
  Serial.begin(9600);
  qtr.setTypeRC();
  qtr.setSensorPins((const uint8_t[]){2, 3, 8, 9, 10, 11, 12, A0}, SensorCount);
  //qtr.setEmitterPin(2);
   delay(500);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH); // turn on Arduino's LED to indicate we are in calibration mode

  // 2.5 ms RC read timeout (default) * 10 reads per calibrate() call
  // = ~25 ms per calibrate() call.
  // Call calibrate() 400 times to make calibration take about 10 seconds.
  for (uint16_t i = 0; i < 200; i++)
  {
    qtr.calibrate();
  }
  digitalWrite(LED_BUILTIN, LOW); // turn off Arduino's LED to indicate we are through with calibration
   pinMode(motorL, OUTPUT);
  pinMode(RIGHT, OUTPUT);
  pinMode(LEFT, OUTPUT);
  pinMode(button, INPUT);
  pinMode(motorR, OUTPUT);
    pinMode(A7, INPUT);
    while(analogRead(A7) >= 1020)
  {
    delay(1);
  }
}
void setMotor(int side, int spd)
{
  if(side == LEFT)
  {
    analogWrite(motorL, abs(spd)*mulL);
    digitalWrite(LDir, spd>=0 ? HIGH : LOW);
  }
  else if(side == RIGHT)
  {
    analogWrite(motorR, abs(spd)*mulR);
    digitalWrite(RDir, spd>=0 ? HIGH : LOW);
  }
}
bool white = 1;
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
  int adjP =error/kP; /*+ kIintegral*/
  int adjD = (error-lastError)/kD;
  int correction = adjP + adjD;
  setMotor(LEFT, (tP+correction));
  setMotor(RIGHT, (tP-correction));
  /*Serial.print("Correction: ");
  Serial.print(correction);
  Serial.print(", ");
  Serial.print(tP-correction);
  Serial.print(", ");
  Serial.println(tP+correction);
  */lastError = error;
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
    setMotor(LEFT, 0);
    setMotor(RIGHT, 0);
    delay(500);
    go(250, -50);
    delay(500);
    qtr.read(sensorValues);
    if(sensorValues[7] >=500)
    {
      setMotor(LEFT, 100);
      setMotor(RIGHT, -100);
      delay(300);
      setMotor(LEFT, 0);
      setMotor(RIGHT, 0);
      delay(30);
    }
    else if(sensorValues[0] >=500)
    {
      setMotor(RIGHT, 100);
      setMotor(LEFT, -100);
      delay(300);
      setMotor(LEFT, 0);
      setMotor(RIGHT, 0);
    }
    else
    {
      
      go(50, 200);
      qtr.read(sensorValues);
      while(sensorValues[4] <=200)
      {
        qtr.read(sensorValues);
        go(50, 200);
      }
    }
  }
  white = 1;
  Serial.println(position);
}
