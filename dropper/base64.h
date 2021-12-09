#ifndef BASE_64_H_
#define BASE_64_H_

#include <string>
#include <vector>

std::wstring b64Encode(std::vector<uint8_t> binaryData);
std::vector<uint8_t> b64Decode(std::wstring toDecode);

#endif