package main

// File: allportscan.go
// No credits to me for this 
// code is borrowed from unknown source.
import (
	"flag"
	"fmt"
	"net"
	"sync"
	"time"
)

func main() {
	var wg sync.WaitGroup
	var target string
	fmt.Println("all ports scanner")
	flag.StringVar(&target, "t", "", "target hostname or IP")
	flag.Parse()
	fmt.Println("")
	if target == "" {
		fmt.Println("Specify a target with the -t flag.")
		fmt.Println("  ex: allportscan -t <ip>")
		return
	}
	fmt.Println("Scanning", target, " ports 1-65535")
	wg.Add(65535)
	for p := 1; p < 65536; p++ {
		port := fmt.Sprintf("%d", p)
		go func(port string) {
			defer wg.Done()
			c, e := net.DialTimeout("tcp", target+":"+port, time.Second*1)
			if e == nil {
				fmt.Println(port + "/open")
				c.Close()
			}
		}(port)
		if p%5 == 0 {
			time.Sleep(2 * time.Millisecond)
		}
	}
	wg.Wait()
}
