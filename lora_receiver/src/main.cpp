/*
Original code by : https://github.com/Snootlab/lora_chisterapi
Edited by : Philippe Rochat & Lionel Isoz
*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> // C++, not a good id
#include <signal.h>
#include <RH_RF95.h>
#include <iostream> // ... to comment out too
#include <string> // Idem 
#include <fstream> // idem

using namespace std;

RH_RF95 rf95;

int run = 1;

int Nbr_received_DATA = 0; // Global var to cound collected data types (when complete, we have the 3 types)
// Global string vars to store the data (a collection of 3 positioning elements)
char longitude[256]; 
char latitude[256];
char altitude[256];

/* Signal the end of the software */
void sigint_handler(int signal)
{
    run = 0;
}

void setup()
{ 
    wiringPiSetupGpio();

    if (!rf95.init()) 
    {
        fprintf(stderr, "Init failed\n");
        exit(1);
    }

    /* Tx Power is from +5 to +23 dbm */
    rf95.setTxPower(23);
    /* There are different configurations
     * you can find in lib/radiohead/RH_RF95.h 
     * at line 437 
     */
    rf95.setModemConfig(RH_RF95::Bw125Cr45Sf128);
    rf95.setFrequency(868.0); /* MHz */
}

void readMHPacket(uint8_t *buf)
{

	FILE *fd; // File descriptor
	
	printf(">>Node: %u, Type: %u, Lenght: %u, Content: %s\n", buf[0], buf[1], buf[2], &buf[3]);

    // The received DATA MANAGEMENT :
   
  
    // Collect data until we have a collection of the 3 types needed
    if (Nbr_received_DATA < 3) {
      	if (buf[1] == 2) {// If data type at octer 2 is of type 2 (aka LONGITUDE)
          	Nbr_received_DATA +=1;
			strcpy(longitude, (char *)&buf[3]); // Copy buf into global var to be kept until we have the 3
       	} else if (buf[1] == 3) { // If data type at octer 2 is of type 3 (aka LATITUDE)
            Nbr_received_DATA +=1;
			strcpy(latitude, (char *)&buf[3]);
        } else if (buf[1] == 4) { // If data type at octer 2 is of type 4 (aka ALTITUDE)
            Nbr_received_DATA +=1;
			strcpy(altitude, (char *)&buf[3]);
        } 
	} else {
		Nbr_received_DATA = 0; // Reset type counter
		if(!(fd = fopen("SolarLoon.kml", "a"))) { // Open file descriptor to append into
			// crashing error --- would be cleaner with perror()
			printf("File opening for w ERROR !\n");
			//exit(1);
		} else { 
			fprintf(fd, "%s, %s, %s", longitude, latitude, altitude); // Write the collection
			fclose(fd);
		}
	}
}


void loop()
{

    /* If we receive one message we show on the prompt
     * the address of the sender and the Rx power.
     */
    if( rf95.available() ) 
    {
        uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
        uint8_t len = sizeof(buf);

        if (rf95.recv(buf, &len))
         {
              readMHPacket(&buf[0]);
        }
    }
}

int main(int argc, char **argv)
{
    signal(SIGINT, sigint_handler);

    setup();

    while( run )
    {
     loop();
     usleep(1);
    }

    return EXIT_SUCCESS;
}
