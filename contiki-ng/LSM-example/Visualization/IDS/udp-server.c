/*
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the Institute nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE INSTITUTE AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE INSTITUTE OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 * This file is part of the Contiki operating system.
 *
 */
#include "net/routing/rpl-lite/rpl.h"
#include "net/ipv6/uip-icmp6.h"

rpl_nbr_t *blacklistnbr;

#include "contiki.h"
#include <stdlib.h> // for strtol function
#include "net/routing/routing.h"
#include "net/netstack.h"
#include "net/ipv6/simple-udp.h"

#include "sys/log.h"

unsigned char sharedkey[16] = {0x2f, 0x8c, 0xe7, 0x59, 0xa1, 0xd3, 0x76, 0x48, 0x13, 0x5c, 0x9d, 0xfa, 0x0b, 0x64, 0x82, 0xc5};

unsigned char privatekey[8] = {};

unsigned char privatekeys[MAX_NODES][16] = {
    {0x6d, 0xfb, 0x8e, 0x27, 0xa9, 0x4c, 0x13, 0xd5, 0x3b, 0x8f, 0x2a, 0x11, 0x5c, 0x9b, 0x47, 0xe6},
    {0x7a, 0xee, 0x43, 0xbc, 0x35, 0x98, 0x0f, 0xa7, 0x6d, 0x12, 0x3e, 0x2f, 0xb9, 0x4c, 0x77, 0xa2},
    {0x12, 0x34, 0x56, 0x78, 0x9a, 0xbc, 0xde, 0xf0, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88},
    {0x52, 0x14, 0xa8, 0x6f, 0xe2, 0xdc, 0x8b, 0x41, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x00},
    {0xf4, 0x60, 0x9a, 0x3d, 0x1c, 0x57, 0xe8, 0x02, 0x5d, 0x2e, 0x3f, 0x4a, 0xb6, 0x7c, 0x89, 0xd0},
    {0x2b, 0x76, 0xd3, 0xfe, 0x65, 0xa0, 0xc9, 0x84, 0xe7, 0x8d, 0x0c, 0x2b, 0x9f, 0x5a, 0x47, 0x33},
    {0x90, 0x55, 0x1e, 0x49, 0xbd, 0xf8, 0x73, 0xdb, 0x55, 0x7c, 0x3e, 0x90, 0x2f, 0x16, 0x4b, 0x78},
    {0xc1, 0x8d, 0x46, 0x01, 0x3a, 0xe5, 0x6f, 0x22, 0xb4, 0x8d, 0x6a, 0x91, 0x0f, 0x3b, 0x4e, 0x2c},
    {0xa2, 0x37, 0xf0, 0xb3, 0x86, 0xc1, 0x0a, 0x45, 0x70, 0x2f, 0x6e, 0x84, 0x39, 0x5c, 0x7a, 0xd1},
    {0xd9, 0x04, 0x6d, 0xae, 0x5f, 0x9a, 0xe1, 0xc6, 0x33, 0x21, 0x1f, 0x5b, 0x7c, 0xd8, 0x29, 0xa0},
    {0x99, 0x04, 0x64, 0xa2, 0x5f, 0x4a, 0xa1, 0xe6, 0x1e, 0x9a, 0x3b, 0x48, 0xf7, 0x6d, 0x2e, 0x81},
    {0x1a, 0xb3, 0x8d, 0x7e, 0x9f, 0xc2, 0x5e, 0x34, 0x8a, 0x57, 0x0b, 0x4d, 0x6f, 0x29, 0xd8, 0x63},
    {0xc8, 0x2f, 0x95, 0x76, 0x3d, 0x1a, 0x6b, 0x54, 0x0e, 0x8d, 0x1c, 0x9e, 0x72, 0x3f, 0x8a, 0xb6},
    {0x9c, 0x34, 0x0e, 0x87, 0x51, 0xad, 0x23, 0x6f, 0x1d, 0x78, 0xa4, 0x29, 0x6c, 0x5b, 0x92, 0x3e},
    {0x56, 0x8f, 0x23, 0xd9, 0xa7, 0x1b, 0x4e, 0xc5, 0x7d, 0x6e, 0x92, 0x30, 0x1a, 0x5c, 0x8b, 0x9f},
    {0x0f, 0x4a, 0x6c, 0x98, 0x2b, 0x57, 0xd4, 0x89, 0x3e, 0xa1, 0x7d, 0xf4, 0x20, 0x8e, 0x31, 0x7b},
    {0x81, 0xd7, 0x43, 0x2f, 0x96, 0xa5, 0x7c, 0xe1, 0x36, 0x0d, 0x54, 0x9b, 0x8e, 0x2c, 0x1f, 0x5a},
    {0xa9, 0x3c, 0x18, 0x52, 0xe4, 0x89, 0x7d, 0xf1, 0x5b, 0x27, 0x6f, 0xc8, 0xd3, 0x4a, 0x1e, 0x02},
    {0x4f, 0x62, 0x38, 0x1d, 0x9e, 0x7a, 0x5b, 0x4c, 0x82, 0x03, 0x91, 0x6d, 0xb5, 0xe8, 0x2a, 0x7f},
    {0x63, 0x2a, 0xb7, 0x48, 0xe9, 0x1f, 0x5c, 0xd7, 0x0e, 0xf3, 0x86, 0x2b, 0xa9, 0x7d, 0x0c, 0x34}};

// unsigned short int nodesinfo[MAX_NODES][PARAMETER_NUMBER] = {0}; // 0 version , 1 rank , other reserved

#define LOG_MODULE "App"
#define LOG_LEVEL LOG_LEVEL_INFO

#define WITH_SERVER_REPLY 1
#define UDP_CLIENT_PORT 8765
#define UDP_SERVER_PORT 5678

// Global variables
#define BUFFER_SIZE 1024       // Adjust size as needed
char recv_buffer[BUFFER_SIZE]; // To store concatenated chunks
size_t recv_pos = 0;           // Current position in the buffer

static struct simple_udp_connection udp_conn;
long extract_number(const char *str)
{
  char *endptr;
  long number = strtol(str, &endptr, 10); // Convert initial digits to long

  // Check for errors and non-numeric characters
  if (str == endptr || *endptr != ' ')
  {
    return -1; // Indicate error: no number found or invalid format
  }

  return number; // Return the extracted number
}

PROCESS(udp_server_process, "UDP server");
AUTOSTART_PROCESSES(&udp_server_process);

bool is_dataset_message = false; // Global flag to track if we're processing a dataset message

void udp_rx_callback(struct simple_udp_connection *c,
                     const uip_ipaddr_t *sender_addr,
                     uint16_t sender_port,
                     const uip_ipaddr_t *receiver_addr,
                     uint16_t receiver_port,
                     const uint8_t *data,
                     uint16_t datalen)
{

  char *strdata = (char *)data;

  // Check if this is the first chunk and starts with "ds:"
  if (recv_pos == 0 && strncmp(strdata, "ds:", 3) == 0)
  {
    // This is a dataset message, mark the flag
    is_dataset_message = true;
  }

  // If we have previously marked this as a dataset message, handle the chunks as part of the dataset
  if (is_dataset_message)
  {
    // Ensure there's enough space in the buffer to add the new chunk
    if (recv_pos + datalen < BUFFER_SIZE)
    {
      // Copy the received chunk into the buffer
      memcpy(recv_buffer + recv_pos, data, datalen);
      recv_pos += datalen;
      // LOG_WARN("ds: test Buffer %s \n", recv_buffer);
    }
    else
    {
      LOG_WARN("Buffer overflow, discarding chunk\n");
      return;
    }

    // Check if the received chunk contains an end delimiter (e.g., '$')
    if (data[datalen - 1] == '$')
    {
      recv_buffer[recv_pos] = '\0'; // Null-terminate the buffer to make it a valid string

      // Now we have the complete dataset message, handle it
      LOG_INFO("d%s\n", recv_buffer);

      // Reset the buffer and the dataset flag for the next message
      recv_pos = 0;
      is_dataset_message = false;
    }
  }
  else
  {
    // Handle message starting with a sequence number (non-dataset message)
    uint32_t seqnum = extract_number(strdata);

    // Check if the sequence number extraction was successful
    if (seqnum != -1)
    {
      LOG_INFO("app receive packet seqnum=%" PRIu32 " from=", seqnum);
  LOG_INFO_6ADDR(sender_addr);
  LOG_INFO_("\n");

  LOG_INFO("Received request '%.*s' from ", datalen, (char *)data);
  // LOG_INFO_6ADDR(receiver_addr);
  LOG_INFO_6ADDR(sender_addr); // hunsr there ara error in this line becouse sender_addr print root address
  LOG_INFO_("\n");


      // Process the message based on the sequence number
      // (Add your packet delivery rate recording or other logic here)
    }
    else
    {
      LOG_WARN("Invalid message format, discarding\n");
    }

#if WITH_SERVER_REPLY
    // hunsr
    char msg[250];
    strcpy(msg, (char *)data);
    if (strstr((char *)data, "okko") != NULL)
      strcat(msg, "correct");
    else if (strstr((char *)data, "kook") != NULL)
      strcat(msg, "error");

    uint16_t datalength = (uint16_t)strlen(msg);
    simple_udp_sendto(&udp_conn, msg, datalength, sender_addr);
    /* send back the same string to the client as an echo reply */
    LOG_INFO("Sending response .'%.*s'  \n", datalength, (char *)msg);

    //  simple_udp_sendto(&udp_conn, data, datalen, sender_addr);
#endif /* WITH_SERVER_REPLY */
  }
}

// /*---------------------------------------------------------------------------*/
// static void
// udp_rx_callback(struct simple_udp_connection *c,
//                 const uip_ipaddr_t *sender_addr,
//                 uint16_t sender_port,
//                 const uip_ipaddr_t *receiver_addr,
//                 uint16_t receiver_port,
//                 const uint8_t *data,
//                 uint16_t datalen)
// {
//   // Extract sequence number from data
//   char *strdata = (char *)data;
//   // uint32_t seqnum = extract_number(strdata);
//  uint32_t seqnum = 66;

//   LOG_INFO("isp %s\n", strdata);

//   // LOG_INFO(strdata);

//   // // Variable to store RPL message type
//   // const char *rpl_message_type = "Unknown";

//   // // Check if the packet is an ICMPv6 RPL control message
//   // if (UIP_IP_BUF->proto == UIP_PROTO_ICMP6)
//   // {
//   //   uint8_t icmp_type = UIP_ICMP_BUF->type;

//   //   // Determine the RPL message type based on the ICMPv6 type and code
//   //   switch (icmp_type)
//   //   {
//   //   case RPL_CODE_DIS:
//   //     rpl_message_type = "DIS";
//   //     break;
//   //   case RPL_CODE_DIO:
//   //     rpl_message_type = "DIO";
//   //     break;
//   //   case RPL_CODE_DAO:
//   //     rpl_message_type = "DAO";
//   //     break;
//   //   default:
//   //     rpl_message_type = "Other RPL Message";
//   //     break;
//   //   }
//   // }

//   // // Log dataset information in a single line starting with "dataset"
//   // printf("dataset Timestamp: %lu, SeqNum: %" PRIu32 ", Data: %.*s, RPL Message Type: %s, Source: ",
//   //        clock_time(), seqnum, datalen, (char *)data, rpl_message_type);

//   // // Log sender IP address using LOG_INFO_6ADDR
//   // LOG_INFO_6ADDR(sender_addr);

//   // printf(", Receiver: ");

//   // // Log receiver IP address using LOG_INFO_6ADDR
//   // LOG_INFO_6ADDR(receiver_addr);

//   // printf(", Sender Port: %u, Receiver Port: %u\n", sender_port, receiver_port);

//   LOG_INFO("app receive packet seqnum=%" PRIu32 " from=", seqnum);
//   LOG_INFO_6ADDR(sender_addr);
//   LOG_INFO_("\n");

// #if WITH_SERVER_REPLY
//   char msg[50];
//   strcpy(msg, (char *)data);
//   if (strstr((char *)data, "okko") != NULL)
//     strcat(msg, "correct");
//   else if (strstr((char *)data, "kook") != NULL)
//     strcat(msg, "error");

//   uint16_t datalength = (uint16_t)strlen(msg);
//   simple_udp_sendto(&udp_conn, msg, datalength, sender_addr);
//   LOG_INFO("Sending response: '%.*s'\n", datalength, (char *)msg);
// #endif /* WITH_SERVER_REPLY */
// }

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(udp_server_process, ev, data)
{
  PROCESS_BEGIN();
#if LSM == 1

  nodesinfo[1][0] = 240; // root version
  nodesinfo[1][1] = 128; // root rank
#endif

#if DRA == 1
  LOG_ERR("Server online now for node 1 \n");
#endif /* DRA == 1 */

  /* Initialize DAG root */
  NETSTACK_ROUTING.root_start();

  /* Initialize UDP connection */
  simple_udp_register(&udp_conn, UDP_SERVER_PORT, NULL,
                      UDP_CLIENT_PORT, udp_rx_callback);

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/
