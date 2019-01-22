all:
	gcc ./shell.c -m32 -ggdb -fno-stack-protector -w -z execstack -o shell32
	gcc ./shell.c -ggdb -fno-stack-protector -w -z execstack -o shell64
	gcc ./setresuid.c -m32 -ggdb -fno-stack-protector -w -z execstack -o setresuid32
	gcc ./setresuid.c -ggdb -fno-stack-protector -w -z execstack -o setresuid64
	gcc ./reverse_tcp.c -o reverse_tcp64
	gcc ./reverse_tcp.c -m32 -o reverse_tcp32

shell32:
	gcc ./shell.c -m32 -ggdb -fno-stack-protector -w -z execstack -o shell32
	gcc ./setresuid.c -m32 -ggdb -fno-stack-protector -w -z execstack -o setresuid32
	gcc ./reverse_tcp.c -m32 -o reverse_tcp32
shell64:
	gcc ./shell.c -ggdb -fno-stack-protector -w -z execstack -o shell64
	gcc ./setresuid.c -ggdb -fno-stack-protector -w -z execstack -o setresuid64
	gcc ./reverse_tcp.c -o reverse_tcp64
clean:
	rm -f shell32 shell64
