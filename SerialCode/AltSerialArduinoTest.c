#define sprint Serial.println
#define LEFT 0
#define RIGHT 1
#define BACK 0
#define FORW 1
/*sample usage: //ideally would be run in a while true loop to constantly be checking
//command from pi: "t045r" means turn 45 deg right
Struct command = readPi();
int typeOfMovement = command.MoT;
int amount = command.mag;
int direction = command.dir;
//then i can make the associated movements once the type, amount, and direction of movement has been set.
*/
String incoming = "random";
void initSerial() {
  Serial.begin(115200);
  pinMode(13, OUTPUT);
  Serial.setTimeout(5);
}
struct movement{ 
    bool MoT; //Move or Turn. Move is 0, Turn is 1
    bool dir; //direction. 0 is left or back depending on MoT, 1 is right or forward depending on MoT
    int mag; //magnitude; ie cm of movement or deg of turn
}; 
  
typedef struct movement Struct;
Struct readPi() {
  // Returns integer code for stop or go or an integer for amount of degrees
  // GO -- 999
  // STOP -- 998
  Struct comm; //short for command
  char target[10];
  if (Serial.available() > 0)
  {
    incoming = Serial.readString();
    for(int z = 0; z<=incoming.length(); z++)
      target[z] = incoming[z];
  }
  else
  {
    incoming = "NULL";
    for(int z = 0; z<=incoming.length(); z++)
      target[z] = incoming[z];    
  }
  if (incoming == "stop")
  {
    comm.mag = 998;
  }
  if (incoming == "cont")
  {
    comm.mag = 999;
  }
  if (target[0] == 't')
  {
    int turnVal = (String(target[4])+String(target[5])+String(target[6])).toInt();
    int dir = target[7] == 'l' ? LEFT : RIGHT; 
    comm.MoT = 1;
    comm.dir = dir;
    comm.mag = turnVal;
  }
  if (target[0] == 'm')
  {
    String strdist = (String(target[4])+String(target[5])+String(target[6]));
    float size = strlen(strdist);
    int dist = strdist.toInt();
    int dir = target[7] == 'f' ? FORW : BACK;
    comm.MoT = 0;
    comm.dir = dir;
    comm.mag = turnVal;
  }
  incoming = "reset";
  return comm;
}


/*void flash(int times)
{
  for(int x = 0; x<times; x++)
  {
    digitalWrite(13, HIGH);
    delay(400);
    digitalWrite(13, LOW);
    delay(400);
  }
}
*/


