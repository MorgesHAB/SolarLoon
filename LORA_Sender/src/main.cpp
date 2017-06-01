/*
Original code by : https://github.com/Snootlab/lora_chisterapi
Edited by : Philippe Rochat & Lionel Isoz
*/
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>
#include <RH_RF95.h>

RH_RF95 rf95;

#define GPSTIME 0
#define SPEED 1
#define LONGITUDE 2
#define LATITUDE 3
#define ALTITUDE 4

#define msg_Temperature 5
#define msg_Pressure 6
#define msg_Humidity 7

#define NODE_NUMBER 8
// string NODE_NUMBER = "MorgesHAB"

uint8_t msg[200];

int run = 1;

/* Send a message every 3 seconds */
void sigalarm_handler(int signal)
{
   rf95.send(msg, sizeof(msg));
   rf95.waitPacketSent();
//   printf("Sent!\n");
   alarm(3);
}

/* Compose a message to be sent in a MorgesHabPacket : MHPacket */
/*Syntax is:
  byte 0: node number
  byte 1: msg type
  byte 2: msg length (max 200-4)
  byte 3 & ... : ASCII encoded value, null terminated
*/
void writeMHPacket(uint8_t type, char *m) {
  msg[0] = NODE_NUMBER;
  msg[1] = type;
  msg[2] = (uint8_t)strlen(m);
  strcpy((char *)&msg[3], m); // We should use strncpy !!!!
}

/* get content from such a packet ... */
/*
void readMHPacket(uint8_t *msg) {
  printf(">>Node: %u, Type: %u, Length: %u, Content: %s\n", msg[0], msg[1], msg[2], &msg[3]);
} 
*/

/* Signal the end of the software */
void sigint_handler(int signal)
{
    run = 0;
}

void setup() {
     wiringPiSetupGpio();

     if (!rf95.init()) 
     {
         fprintf(stderr, "Init failed\n");
         exit(1);
     }

     /* Tx power is from +5 to +23 dBm */
     rf95.setTxPower(23);
     /* There are different configurations
      * you can find in lib/radiohead/RH_RF95.h 
      * at line 437 
      */
     rf95.setModemConfig(RH_RF95::Bw125Cr45Sf128);
     rf95.setFrequency(868.0); /* Mhz */
}

int main(int argc, char **argv)
{
    signal(SIGINT, sigint_handler);
    signal(SIGALRM, sigalarm_handler);

    alarm(3);

    setup();

  // i will run through GPSTIME, SPEED, LONGITUDE, LATITUDE, ALTITUDE
  for(int i = 1; i<argc; i++) { // Skip 0 which is program itself
    writeMHPacket(i-1, argv[i]);
    sigalarm_handler(1); // Fake a signal
   // readMHPacket(&msg[0]);
  }

    return EXIT_SUCCESS;
}
