#include "config.h"

#include <string.h>
#include <sysinfoapi.h>
#include <windows.h>
#include <winbase.h>

#define DEBUG 1

#if DEBUG == 1
#include <stdio.h>
#define LOG wprintf
#else
#define LOG void
#endif

int wmain(int argc, wchar_t **argv, wchar_t **envp)
{
    HANDLE namedPipe = CreateNamedPipeA(MALWARE_NAMED_PIPE, PIPE_ACCESS_DUPLEX, PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE, 2, 512, 512, 0, NULL);
    if (namedPipe == INVALID_HANDLE_VALUE)
    {
        LOG(L"Only one instance at a time!\n");
        return 1;
    }
    if (INVALID_FILE_ATTRIBUTES == GetFileAttributesA(MALWARE_FILE_EXISTS_STRING) && GetLastError() == ERROR_FILE_NOT_FOUND)
    {
        // LOG(L"No ch0nky.txt\n");
        return -1;
    }
    SYSTEMTIME currentTime;
    GetSystemTime(&currentTime);
    if (MALWARE_KILL_DATE_YEAR <= currentTime.wYear && MALWARE_KILL_DATE_MONTH <= currentTime.wMonth && MALWARE_KILL_DATE_DAY < currentTime.wDay)
    {
        // LOG(L"Kill Date passed!\n");
        return -1;
    }
    while (true)
        ;
    return 0;
}