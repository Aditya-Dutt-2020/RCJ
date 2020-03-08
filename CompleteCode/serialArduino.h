#ifndef serialArduino
#define serialArduino

//#define LEFT 0
//#define RIGHT 1
#define BACKSER 0
#define FORWSER 1

struct movement{ 
    bool MoT; //Move or Turn. Move is 0, Turn is 1
    bool dir; //direction. 0 is left or back depending on MoT, 1 is right or forward depending on MoT
    int mag; //magnitude; ie cm of movement or deg of turn
}; 
  
//struct movement readPi();
void initSerial();
//struct movement readPi();


#endif
