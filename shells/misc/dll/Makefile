all:
	i686-w64-mingw32-g++ payload.c -lws2_32 -o payload.dll -shared
	i686-w64-mingw32-g++ useradd.c -lws2_32 -o useradd.dll -shared
clean:
	rm payload.dll useradd.dll
