

#include "motorShieldControl.h"
#include "ultrasonic.h"
/*
uint16_t sensorValues1[8];
void readsensors()
{
  for (int i; i < 8; i++)
  {
      sensorValues1[i] = readSensor(i);
  }
}
*/

void objavoid()
{
  bool dir; //left 0     right 1
  if (getDist() < 5)
  {
    pointTurn(LEFT,90);
    if (getDist() < 5)
    {
      dir=RIGHT;
    }
    else
    {
      dir=LEFT;
    }
    pointTurn(RIGHT,90);
    
    pointTurn(dir,90);
    straight(30);
    pointTurn(!dir,90);
    straight(40);
    pointTurn(!dir,90);
    straight(30);
    pointTurn(dir,90);
    
    
  }

}
