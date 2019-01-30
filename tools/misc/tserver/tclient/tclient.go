package main

// File: tclient.go
// Author: nighter@nighter.se
// Not finalised yet.

import (
	"bytes"
	"flag"
	"fmt"
	"log"
	"os"
	"os/exec"
	"bufio"
)

func checkErr(err error) {
	if err != nil {
		panic(err)
	}
}

func printUsage() {
	usage := `                                                                                                 
	████████╗ ██████╗██╗     ██╗███████╗███╗   ██╗████████╗
	╚══██╔══╝██╔════╝██║     ██║██╔════╝████╗  ██║╚══██╔══╝
	   ██║   ██║     ██║     ██║█████╗  ██╔██╗ ██║   ██║   
	   ██║   ██║     ██║     ██║██╔══╝  ██║╚██╗██║   ██║   
	   ██║   ╚██████╗███████╗██║███████╗██║ ╚████║   ██║   
	   ╚═╝    ╚═════╝╚══════╝╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   		
	Tclient [nighter@nighter.se] [Wrapsup plink.exe]
	--------------------------------------------------------
	-p <port to tunnel>	  |  The port you want to tunnel
	-P <lport>                |  Override lport
	-l <lhost>	          |  Override lhost
	-w <password>             |  Override password
	--------------------------------------------------------

	Example: tclient -p 445

Usage: tclient <arguments>
`
	fmt.Println(usage)
	os.Exit(0)
}

func Shellout(command string) (error, string, string) {
	var stdout bytes.Buffer
	var stderr bytes.Buffer
	cmd := exec.Command("cmd", "/C", command)
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr
	err := cmd.Run()
	return err, stdout.String(), stderr.String()
}

func main() {

	/* Settings */
	var PORTUNNEL = "445"
	var LHOST = "10.100.12.64"
	var LPORT = "80"
	var LPASSWORD = "ZmY1NzkzMjhlYTFjZDU3ODA4Y2JmZT"

	portTunnel := flag.String("p", "", "Port to tunnel")
	lport := flag.String("P", "", "Ovveride lport")
	lhost := flag.String("l", "", "Override lhost")
	lpassword := flag.String("w", "", "Override password")

	flag.Parse()

	if *portTunnel == "" {
		printUsage()
	} else {
		PORTUNNEL = *portTunnel
	}

	if *lport != "" {
		LPORT = *lport
	}

	if *lhost != "" {
		LHOST = *lhost
	}

	if *lpassword != "" {
		LPASSWORD = *lpassword
	}
 
	command := " echo y | plink.exe -l root -pw " + LPASSWORD + " -R " + PORTUNNEL + ":127.0.0.1:" + PORTUNNEL + " " + LHOST + " -P " + LPORT
	fmt.Println(command)

	err, out, errout := Shellout(command)
	if err != nil {
		log.Printf("error: %v\n", err)
	}

	fmt.Println(out)
	fmt.Println(errout)

	buf := bufio.NewReader(os.Stdin)
	fmt.Print("Press any key to kill tunnel.")	
	buf.ReadBytes('\n')
}
