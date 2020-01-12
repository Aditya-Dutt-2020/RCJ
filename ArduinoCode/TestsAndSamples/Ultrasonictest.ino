

int USPingPin = 7;
int USRecvPin = 8;
int maxDist = 250;

float sos = 0.0343; // sos = speed of sound. In ms

void initUS() {
  pinMode(USPingPin, OUTPUT);
  pinMode(USRecvPin,  INPUT);
  Serial.begin(9600);
}

long getDist(){
  digitalWrite(USPingPin, LOW);
  delayMicroseconds(2);
  digitalWrite(USPingPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(USPingPin, LOW);
  
  long t = pulseIn(USRecvPin, HIGH);
  long dist = t * sos / 2;

  if (dist > maxDist){
    dist = 0;
  }
  
  return dist;
}


void setup(){
  initUS();
}

void loop(){
  Serial.println(getDist());
}
