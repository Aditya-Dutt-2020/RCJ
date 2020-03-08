

#include "motorShieldControl.h"
#include "ultrasonic.h"

uint16_t sensorValues1[8];
void readsensors()
{
  for (int i; i < 8; i++)
  {
      sensorValues1[i] = readSensor(i);
  }
}


void objavoid()
{
  if(getDist()>5)
  {
    return;
  }
  bool dir; //left 0     right 1
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
  for(int abc=0;abc<3;abc++)
  {
      pointTurn(!dir,90);
      for(int i=0;i<50*2)
      {
        straight(0.5);
        readSensors();
        if(sensorValues1[4] < 127 and sensorValues1[5] < 127)
        {
            pointTurn(dir,90);
            return;
        }
      }
  }
  
  }
  
  
  

    


}
