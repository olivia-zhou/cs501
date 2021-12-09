#ifndef HTTP_CLIENT_H_
#define HTTP_CLIENT_H_

#include <string>

std::wstring makeHttpRequest(std::wstring fqdn, int port, std::wstring uri, std::wstring header_data, std::string request_data, bool useTLS);

#endif