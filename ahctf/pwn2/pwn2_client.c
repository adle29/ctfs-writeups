#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void give_flag()
{
	printf("AHCTF{xxxxxxxxxxxxxxxxxxxxxxx}\n");
    	fflush(stdout);
}

int main(int argc, char **argv)
{
	char buffer[64];
	printf("%d", sizeof(buffer));
	gets(buffer);
}
