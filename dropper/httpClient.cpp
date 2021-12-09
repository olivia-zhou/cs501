#include <windows.h>
#include <string>
#include <winhttp.h>

#include "httpClient.h"

std::wstring makeHttpRequest(std::wstring fqdn, int port, std::wstring uri, std::wstring header_data, std::wstring request_data, bool useTLS)
{
    std::wstring result = L"";
    HINTERNET hSession = NULL,
              hConnect = NULL,
              hRequest = NULL;
    BOOL bResult = FALSE;
    DWORD dwSize = 0;
    DWORD dwDownloaded = 0;
    LPSTR pszOutBuffer;

    hSession = WinHttpOpen(NULL, WINHTTP_ACCESS_TYPE_AUTOMATIC_PROXY, WINHTTP_NO_PROXY_NAME, WINHTTP_NO_PROXY_BYPASS, 0);
    if (hSession)
    {
        hConnect = WinHttpConnect(hSession, fqdn.data(), port, 0);
    }
    if (hConnect)
    {
        hRequest = WinHttpOpenRequest(hConnect, L"POST", uri.data(),
                                      NULL, WINHTTP_NO_REFERER,
                                      WINHTTP_DEFAULT_ACCEPT_TYPES,
                                      useTLS? WINHTTP_FLAG_SECURE : 0);
    }
    if (hRequest != NULL)
    {
        bResult = WinHttpSendRequest(hRequest, header_data.data(), header_data.size(), request_data.data(), request_data.size(), header_data.size() + request_data.size(), 0);
        if (bResult)
        {
            bResult = WinHttpReceiveResponse(hRequest, NULL);
        }
        if (bResult)
        {
            do
            {
                if (!WinHttpQueryDataAvailable(hRequest, &dwSize))
                {
                    break;
                }
                pszOutBuffer = new char[dwSize + 1];
                ZeroMemory(pszOutBuffer, dwSize+1);
                if (!WinHttpReadData(hRequest, pszOutBuffer, dwSize, &dwDownloaded))
                {
                    break;
                }
                wchar_t * tempString = new wchar_t[dwSize + 1];
                std::mbstowcs(tempString, pszOutBuffer, dwSize+1);
                result.append(tempString);
                delete [] pszOutBuffer;
                delete [] tempString;
                if (!dwDownloaded)
                    break;
            } while (dwSize > 0);
        }
    }
    if (hRequest)
        WinHttpCloseHandle(hRequest);
    if (hConnect)
        WinHttpCloseHandle(hConnect);
    if (hSession)
        WinHttpCloseHandle(hSession);
    return result;
}
