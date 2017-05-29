/*
Original code by : https://github.com/Snootlab/lora_chisterapi
Edited by : Philippe Rochat & Lionel Isoz
*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <RH_RF95.h>
#include <iostream>
#include <string>
#include <fstream>

using namespace std;

RH_RF95 rf95;

int run = 1;

bool First_Time_1 = true;
bool First_Time_2 = true;
bool Check_if_all_msg = false;
int Nbr_received_DATA = 0;

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

    ofstream fichier("SolarLoon.kml", ios::out | ios::app);  // write in mode append

    if(fichier)
    {
            if (First_Time_1 == true)
            {
                // Move in the file to the right place
                fichier.seekp(120, ios::end);  // (nbr bytes, start point)
            }
            // We want to check if we have received all the GPS informations before
            // recording into file.kml ! 
            if (Check_if_all_msg == false)
            {
                if (buf[1] == 2)
                {
                    Nbr_received_DATA +=1;
                    LONGITUDE = string &buf[3];
                }
                if (buf[1] == 3)
                {
                    Nbr_received_DATA +=1;
                    LATITUDE = string &buf[3];
                }
                if (buf[1] == 4)
                {
                    Nbr_received_DATA +=1;
                    ALTITUDE = string &buf[3];
                }
                if (Nbr_received_DATA == 3)
                {
                    Check_if_all_msg = true;
                    Nbr_received_DATA = 0;
                }
                if (Nbr_received_DATA != 3)
                {
                    Nbr_received_DATA = 0;
                }
            if (Check_if_all_msg == true)
            {
                fichier << "\n" << LONGITUDE << "," << LATITUDE << "," << ALTITUDE;
                Check_if_all_msg = false;
            }

            fichier.close();
    }
    else
    {
            cerr << "Impossible d'ouvrir le fichier !" << endl;
    }

    // But we also want to record all the messages received during the launch,
    // So GPS Data and Captor Data together
    ofstream fichier2("All_received_messages.txt", ios::out | ios::app);  // write in mode append

    if(fichier2)
    {
        if (First_Time_2 == true) 
        {
            fichier2 << "ALl the received messages during the flight : \n";
            First_Time_2 = false;
        }

        fichier2 << &buf[3] << "\n";    
                    
        fichier2.close();
    }
    else
    {
            cerr << "Impossible d'ouvrir le fichier !" << endl;
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
