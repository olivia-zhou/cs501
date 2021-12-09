#ifndef LOADER_H_
#define LOADER_H_

#include <string>

bool InjectExecutionCode(std::wstring buffer);
bool SpawnShellCode(std::wstring buffer);

#endif