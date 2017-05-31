/*
Original code by : https://github.com/Snootlab/lora_chisterapi
Edited by : Philippe Rochat & Lionel Isoz
*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <RH_RF95.h>

RH_RF95 rf95;

int run = 1;

int Nbr_received_DATA = 0; // Global var to cound collected data types (when complete, we have the 3 types)
// Global string vars to store the data (a collection of 3 positioning elements)
char longitude[256]; 
char latitude[256];
char altitude[256];

bool First_Time = true;

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
	printf(">>Node: %u, Type: %u, Lenght: %u, Content: %s\n", buf[0], buf[1], buf[2], &buf[3]);

  // The received DATA MANAGEMENT :

  FILE *fd; // File descriptor
  // Collect data until we have a collection of the 3 types needed
  if (Nbr_received_DATA < 3) 
  {
      // If data type at octer 2 is of type 2 (aka LONGITUDE)
    	if (buf[1] == 2) 
      {
        	Nbr_received_DATA +=1;
		      strcpy(longitude, (char *)&buf[3]); // Copy buf into global var to be kept until we have the 3
     	} 
      else if (buf[1] == 3) // If data type at octer 2 is of type 3 (aka LATITUDE)
      { 
          Nbr_received_DATA +=1;
		      strcpy(latitude, (char *)&buf[3]);
      } 
      else if (buf[1] == 4) // If data type at octer 2 is of type 4 (aka ALTITUDE)
      { 
          Nbr_received_DATA +=1;
		      strcpy(altitude, (char *)&buf[3]);
      } 
	} 
  else 
  {
		Nbr_received_DATA = 0; // Reset type counter
		if(!(fd = fopen("SolarLoon.kml", "a"))) // Open file descriptor to append into
    { 
			// crashing error --- would be cleaner with perror()
			printf("File opening for w ERROR !\n");
			//exit(1);
		} 
    else 
    { 
			fprintf(fd, "\n%s,%s,%s", longitude, latitude, altitude); // Write the collection
			fclose(fd);
		}
	}

  FILE *fd2; // File descriptor

  if(!(fd2 = fopen("All_received_messages.txt", "a"))) // Open file descriptor to append into
    { 
      // crashing error --- would be cleaner with perror()
      printf("All_received_msg File opening for w ERROR  !\n");
      //exit(1);
    } 
    else 
    { 
      if (First_Time == true)
      {
        fprintf(fd2, "ALl the received messages during the flight : \n" );
        First_Time = false;

      }
      fprintf(fd2, "\n%s", &buf[3]); // Write the collection
      fclose(fd2);
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
