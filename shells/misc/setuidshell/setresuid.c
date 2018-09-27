#define _GNU_SOURCE  
#include <unistd.h>
#include <stdlib.h>
int main(void)
{ 
    setresuid(1000, 1000, 1000); 
    system("/bin/bash"); 
}
