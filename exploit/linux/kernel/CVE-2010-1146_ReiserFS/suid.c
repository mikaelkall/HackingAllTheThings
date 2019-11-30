#include <unistd.h>

int main()
{
    setuid(0);
    setgid(0);

    execl("/bin/sh","sh",0); 
    return 0;
}
