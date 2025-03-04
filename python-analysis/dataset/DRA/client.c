#include "net/routing/rpl-lite/rpl-timers.h"
#include "net/routing/rpl-lite/rpl.h"
#include "contiki.h"
#include "sys/node-id.h"
#include "net/routing/routing.h"
#include "random.h"
#include "net/netstack.h"
#include "net/ipv6/simple-udp.h"
#include <stdint.h>
#include <inttypes.h>
#include "sys/log.h"

#define LOG_MODULE "App"
#define LOG_LEVEL LOG_LEVEL_INFO

#define UDP_CLIENT_PORT 8765
#define UDP_SERVER_PORT 5678
// //////////////////////////////////////////////////Settings/////////////////////////////
#define SEND_INTERVAL (25 * CLOCK_SECOND)
#if IDS == 1
#define IDS_INTERVAL (480 * CLOCK_SECOND)
#endif
#if DISA == 1
#define DISA_INTERVAL (15* CLOCK_SECOND)
////////////////////////////////////////////////////////////////////////////////////////
uint8_t DISA_on;

extern uint8_t VNA_on ;
extern uint8_t DRA_on ;

#endif /* DIS_ATTACK */

static struct simple_udp_connection udp_conn;
static uint32_t rx_count = 0;

/*---------------------------------------------------------------------------*/
/* Move udp_rx_callback before process thread */
static void udp_rx_callback(struct simple_udp_connection *c,
                            const uip_ipaddr_t *sender_addr,
                            uint16_t sender_port,
                            const uip_ipaddr_t *receiver_addr,
                            uint16_t receiver_port,
                            const uint8_t *data,
                            uint16_t datalen)
{
  LOG_INFO("Received response '%.*s' from ", datalen, (char *)data);
  LOG_INFO_6ADDR(sender_addr);
  LOG_INFO_("\n");
  rx_count ++;
}

/*---------------------------------------------------------------------------*/
PROCESS(udp_client_process, "UDP client");
AUTOSTART_PROCESSES(&udp_client_process);

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(udp_client_process, ev, data)
{
  static struct etimer periodic_timer; // For UDP sending interval
  static struct etimer disa_timer;     // For DIS message interval
  static struct etimer ids_timer;      // For DIS message interval
  static char str[60];
  uip_ipaddr_t dest_ipaddr;
  static uint32_t tx_count;
  static uint32_t ids_count;

  static uint32_t missed_tx_count;
  // static uint32_t missed_ids_count;

  PROCESS_BEGIN();

  /* Initialize UDP connection */
  simple_udp_register(&udp_conn, UDP_CLIENT_PORT, NULL,
                      UDP_SERVER_PORT, udp_rx_callback);

  /* Set initial timers */
  etimer_set(&periodic_timer, random_rand() % SEND_INTERVAL); // UDP send interval
  etimer_set(&disa_timer, DISA_INTERVAL);                      // DISA attack every 10 seconds

#if IDS == 1
  etimer_set(&ids_timer, IDS_INTERVAL); // ids attack every 120 seconds
#endif

  while (1)
  {
    PROCESS_WAIT_EVENT();

    /* Handle UDP sending timer */
    if (etimer_expired(&periodic_timer))
    {
      if (NETSTACK_ROUTING.node_is_reachable() &&
          NETSTACK_ROUTING.get_root_ipaddr(&dest_ipaddr))
      {

        /* Print statistics every 10th TX */
        if (tx_count % 10 == 0)
        {
          LOG_INFO("Tx/Rx/MissedTx: %" PRIu32 "/%" PRIu32 "/%" PRIu32 "\n",
                   tx_count, rx_count, missed_tx_count);
        }

        LOG_INFO("app generate packet seqnum=%" PRIu32 " node_id=%u\n", tx_count, node_id);
        LOG_INFO("Sending request %" PRIu32 " to ", tx_count);
        LOG_INFO_6ADDR(&dest_ipaddr);
        LOG_INFO_("\n");

        snprintf(str, sizeof(str), "%u okko::hello $", tx_count);
        simple_udp_sendto(&udp_conn, str, strlen(str), &dest_ipaddr);
        tx_count++;
      }
      else
      {
        LOG_INFO("Not reachable yet\n");
        if (tx_count > 0)
        {
          missed_tx_count++;
        }
      }

      /* Add some jitter */
      etimer_set(&periodic_timer, SEND_INTERVAL - CLOCK_SECOND + (random_rand() % (2 * CLOCK_SECOND)));
    }

#if IDS == 1
    if (etimer_expired(&ids_timer))
    {
      ids_count ++;

      char log_buffer[1024]; // Adjust size as needed
      convert_array_to_string(log_buffer, sizeof(log_buffer));

      printf("ids: %s \n", log_buffer);
      printf("ids_count:  %i \n", ids_count);
      // reset_info();
      etimer_reset(&ids_timer); // Reset DIS timer to trigger every 10 seconds
    }
#endif


#if DISA == 1

    /* Handle DIS sending timer */
    if (etimer_expired(&disa_timer))
    {

      if (VNA_on )
      {
           rpl_timers_dio_reset("reset timer: VNA_on");
      }
      if ( DRA_on)
      {
        rpl_timers_dio_reset("reset timer: DRA_on"); 
      }

      if (DISA_on)
      {
#if IDS == 1
      if(currentnodeinfo[9] != 3)
      {
        currentnodeinfo[9] = 3;
         reset_info();
      }
        
#endif
        // LOG_INFO("Sending DIS message for DIS attack.\n");
        rpl_icmp6_dis_output(NULL); // Send DIS message
        LOG_INFO("DISA active and sent \n");
      }
#if IDS == 1
      else if (currentnodeinfo[9] == 3)
      {
          currentnodeinfo[9] = 0;
          reset_info();
      }
        
#endif

      etimer_reset(&disa_timer); // Reset DIS timer to trigger every 10 seconds
    }
#endif
  }

  PROCESS_END();
}
