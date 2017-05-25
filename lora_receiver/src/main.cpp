/*
Original code by : https://github.com/Snootlab/lora_chisterapi
Edited by : Ramin Sangesari
*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

#include <RH_RF95.h>

RH_RF95 rf95;

int run = 1;

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

void readMHPacket(uint8_t *buf) {
	printf(">>Node: %u, Type: %u, Lenght: %u, Content: %s\n", buf[0], buf[1], buf[2], &buf[3]);

    // ENCORE TOUT L?ASPECT receiving DATA MANAGEMENT 
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
