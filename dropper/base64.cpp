#include <windows.h>
#include <wincrypt.h>
#include <tchar.h>
#include <iostream>
#include <vector>
#include <cstdint>

#include "base64.h"

//hint: use CRYPT_STRING_BASE64

std::wstring b64Encode(std::vector<uint8_t> binaryData)
{
    // note that this will convert your std::string into a c string.
    std::wstring returnBuff = L"error";
    DWORD returnLen = 0;
    // your code here
    // Hint: you should make two calls to ::CryptBinaryToStringW
    // One to get the right size for the buffer
    // Then one to copy the data over
    // std::vector<uint8_t> is a perfectly fine container for raw binary  data
    // as it is allocated in contiguous chunks of memory
    // you can also easily convert it to raw data via returnBuff.data()
    if (CryptBinaryToStringW(binaryData.data(), binaryData.size(), CRYPT_STRING_BASE64, NULL, &returnLen))
    {
        returnBuff.resize(returnLen);
        CryptBinaryToStringW(binaryData.data(), binaryData.size(), CRYPT_STRING_BASE64, returnBuff.data(), &returnLen);
    }
    return returnBuff;
}

std::vector<uint8_t> b64Decode(std::wstring toDecode)
{
    // as before you should make two calls to ::CryptStringToBinaryW
    std::vector<uint8_t> returnBuff;
    DWORD returnLen = 0;
    if (CryptStringToBinaryW(toDecode.data(), toDecode.size(), CRYPT_STRING_BASE64, NULL, &returnLen, NULL, NULL))
    {
        returnBuff.resize(returnLen);
        CryptStringToBinaryW(toDecode.data(), toDecode.size(), CRYPT_STRING_BASE64, returnBuff.data(), &returnLen, NULL, NULL);
    }
    return returnBuff;
}