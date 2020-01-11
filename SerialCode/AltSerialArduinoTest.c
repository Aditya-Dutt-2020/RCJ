#define sprint Serial.println
#define LEFT 0 //Actuall 1
#define RIGHT 1 //Actuall 2
#define BACK 0 //Actuall 1
#define FORW 1 //Actuall 2
String incoming = "random";
void initSerial() {
  Serial.begin(115200);
  pinMode(13, OUTPUT);
  Serial.setTimeout(5);
}

int readPi() {
  // Returns integer code for stop or go or an integer for amount of degrees
  // GO -- 999
  // STOP -- 998
  // DIR,TURNVAL -- 0-1|0-360 EX. 2180. RIGHT 180 degrees. 1180-1|180 1=right,180=180 degs. 
  // DIR,DIST -- -|SIZE|DIR|0-INF. MUST BE NEGATIVE. EX. 2150, 2|0|50; backwards 50 centimeters!

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
    return 998;
  }
  if (incoming == "cont")
  {
    return 999;
  }
  if (target[0] == 't')
  {
    int turnVal = (String(target[4])+String(target[5])+String(target[6])).toInt();
    int dir = target[7] == 'l' ? LEFT : RIGHT; 
    int n = (dir+1)*100+turnval
    return n
  }
  if (target[0] == 'm')
  {
    String strdist = (String(target[4])+String(target[5])+String(target[6]));
    float size = strlen(strdist);
    int dist = strdist.toInt();
    int dir = target[7] == 'f' ? FORW : BACK;
    int n = size*(pow(10.0, size+1))+(dir+1)*(pow(10.0, size))+dist
    return dist
  }
  incoming = "reset";
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


