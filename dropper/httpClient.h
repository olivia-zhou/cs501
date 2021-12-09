#ifndef HTTP_CLIENT_H_
#define HTTP_CLIENT_H_

std::wstring makeHttpRequest(std::wstring fqdn, int port, std::wstring uri, std::wstring header_data, std::wstring request_data, bool useTLS);

#endif