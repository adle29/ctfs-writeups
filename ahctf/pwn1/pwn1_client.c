#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)
{
    volatile int money;
    char buffer[64];

    money = 0;
    printf("What is your name?\n");
    gets(buffer);

    printf("Hello, %s\n",buffer);

    if(money == 0xdeadbeef)
    {
    	printf("Nice, you're rich now. Here's the flag:\n");
        printf("AHCTF{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}");
    }
    else
    {
    	printf("You are too poor to view the flag. Balance: 0x%08x\n", money);
    }
}
