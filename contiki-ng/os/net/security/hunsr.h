/* Log configuration */
#include "sys/log.h"
#include "hmac.h"
#include <stdlib.h>

#define LOG_MODULE "RPL"
#define LOG_LEVEL LOG_LEVEL_RPL
#define RPL_DAO_SECURITY_INFO 13
#define KEY_LENGTH 16

extern unsigned char sharedkey[8];

char *toString(unsigned char *buffer, int pos)
{
    char *string = malloc(sizeof(char) * (pos * 3 + 1)); // Allocate enough space for each number and potential separators.
    string[0] = '\0';                                    // Initialize empty string.

    for (size_t i = 0; i < pos; i++)
    {
        // Convert byte to string representation with space separator.
        char temp[4];
        sprintf(temp, "%x ", buffer[i]);

        // Concatenate to the final string.
        strcat(string, temp);
    }

    return string;
}

unsigned int calculate_digest(unsigned char *buffer, int length, unsigned char *key)
{

    unsigned int sum = hmac_sha256(key, KEY_LENGTH, buffer, length);
    return sum;
}

void set_dio_header_digest(unsigned char *buffer, int pos)
{
    unsigned int sum;
    sum = calculate_digest(buffer, pos, sharedkey);
    // LOG_WARN("hunsr SET buffer size is= %d \n", pos);
    // LOG_WARN("hunsr SET buffer = %s \n", toString(buffer, pos));
    // LOG_WARN("hunsr SET sharedkey = %s \n", toString(sharedkey, 16));
    // LOG_WARN("hunsr SET sum = %X \n", sum);
    memcpy(&buffer[pos], &sum, 4);
    // LOG_WARN("hunsr htest this log by call method set_header_digest in header file \n");
}

bool check_dio_header_digest(unsigned char *buffer, int pos)
{
    unsigned int sum;
    sum = calculate_digest(buffer, pos, sharedkey);

    // LOG_WARN("hunsr Check buffer size is= %d \n", pos);
    // LOG_WARN("hunsr Check buffer = %s \n", toString(buffer, pos + 4));
    // LOG_WARN("hunsr Check sharedkey = %s \n", toString(sharedkey, 8));
    // LOG_WARN("hunsr Check sum = %X \n", sum);

    unsigned int buffersum = 0;

    for (int i = 3; i >= 0; i--)
    {
        buffersum |= buffer[pos + i] << (i * 8);
    }

    // LOG_WARN("hunsr Check buffersum = %X sum=%X \n ", buffersum, sum);

    if (buffersum == sum)
        return true;
    else
        return false;
}
