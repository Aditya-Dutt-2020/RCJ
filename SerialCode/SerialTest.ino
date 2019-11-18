#define sprint Serial.println
#define LEFT 0
#define RIGHT 1
#define BACK 0
#define FORW 1
String incoming = "random";
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(13, OUTPUT);
  Serial.setTimeout(5);
}

void loop() {
  // put your main code here, to run repeatedly
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
  digitalWrite(13, LOW);
 // Serial.println(incoming == "stop");
  if (incoming == "stop")
  {
    sprint("I have stopped");
  }
  if (incoming == "cont")
  {
    sprint("I can continue"); 
  }
  if (target[0] == 't')
  {
    int turnVal = (String(target[4])+String(target[5])+String(target[6])).toInt();
    bool dir = target[7] == 'l' ? LEFT : RIGHT;
    flash(dir == LEFT ? 1 : 2);
    delay(1000);
    flash(turnVal);
  }
  if (target[0] == 'm')
  {
    int dist = (String(target[4])+String(target[5])+String(target[6])).toInt();
    bool dir = target[7] == 'f' ? FORW : BACK;
  }
    /*else{
  }
    Serial.println(incoming);
  }*/
  incoming = "reset";
}


void flash(int times)
{
  for(int x = 0; x<times; x++)
  {
    digitalWrite(13, HIGH);
    delay(400);
    digitalWrite(13, LOW);
    delay(400);
  }
}
