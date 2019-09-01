# b0f-Practice

## Summary

All documentation and experimenting, tools for practice b0f

## Usage

Usage command 'vagrant up --provision' to start a windowsXP machine to practice b0f explotation.
Note all .exe binaries can be found under X: 

```sh
⬢  b0f-Practice  master ⦿ vagrant up --provision 
Bringing machine 'offsecXP' up with 'virtualbox' provider...                                                                                      
==> offsecXP: Importing base box 'Windows32XP_Offsec_Practice'...
==> offsecXP: Matching MAC address for NAT networking...                                                                                                                                                                                                                                             
==> offsecXP: Setting the name of the VM: WindowsXP32_Offsec_Practice
==> offsecXP: Clearing any previously set network interfaces...
==> offsecXP: Available bridged network interfaces:                                                                                               
1) enp30s0                                       
2) virbr0                        
3) enp24s0                             
4) docker0                                                                                                                                        
5) br-398201765f58                  
6) br-f557a0054ae3                                                                                                                                
==> offsecXP: When choosing an interface, it is usually the one that is  
==> offsecXP: being used to connect to the internet.                     
    offsecXP: Which interface should the network bridge to? 1                                                                                     
==> offsecXP: Preparing network interfaces based on configuration...
    offsecXP: Adapter 1: nat        
    offsecXP: Adapter 2: bridged                                                                                                                  
==> offsecXP: Forwarding ports...                     
    offsecXP: 5985 (guest) => 55985 (host) (adapter 1)
    offsecXP: 5986 (guest) => 55986 (host) (adapter 1)                                                                                            
    offsecXP: 22 (guest) => 2222 (host) (adapter 1)                     
==> offsecXP: Booting VM...
==> offsecXP: Waiting for machine to boot. This may take a few minutes... 
    offsecXP: WinRM address: 127.0.0.1:55985
    offsecXP: WinRM username: vagrant
    offsecXP: WinRM execution_time_limit: PT2H
    offsecXP: WinRM transport: negotiate
```
