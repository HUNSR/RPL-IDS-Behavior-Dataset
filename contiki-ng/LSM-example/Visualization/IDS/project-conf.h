/*
 * Copyright (c) 2020, Institute of Electronics and Computer Science (EDI)
 *
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
 *
 * Author: Atis Elsts <atis.elsts@edi.lv>
 */

/* Logging */

/* Hunsr Enable Lightweight Security Mode */

#define CONF_LSM 0 //  Lightweight Security Mode


#define CONF_IDS 1 //  Introsion Detection System
#define CONF_SFA 0 //  Selective Forward Attack
#define CONF_VNA 1 //  Vesion Number Attack
#define CONF_DRA 1 //  Decrease Rank Attack
#define CONF_IRA 0 //  Increase Rank Attack
#define CONF_DISA 1 //  Increase Rank Attack

#define LOG_CONF_LEVEL_IPV6 LOG_LEVEL_NONE
#define LOG_CONF_LEVEL_RPL LOG_LEVEL_NONE
#define LOG_CONF_LEVEL_TCPIP LOG_LEVEL_NONE
#define LOG_CONF_LEVEL_6LOWPAN LOG_LEVEL_NONE
#define LOG_CONF_LEVEL_MAC LOG_LEVEL_NONE
#define TSCH_LOG_CONF_PER_SLOT 0


// hunsr end code

// #define LOG_CONF_LEVEL_IPV6 LOG_LEVEL_WARN
// #define LOG_CONF_LEVEL_RPL LOG_LEVEL_INFO
// #define LOG_CONF_LEVEL_TCPIP LOG_LEVEL_NONE
// #define LOG_CONF_LEVEL_6LOWPAN LOG_LEVEL_NONE
// #define LOG_CONF_LEVEL_MAC LOG_LEVEL_INFO
// #define TSCH_LOG_CONF_PER_SLOT 0




#define LINK_STATS_CONF_PACKET_COUNTERS 1

#define APP_SEND_INTERVAL_SEC 10
#define APP_WARM_UP_PERIOD_SEC 30

#define SICSLOWPAN_CONF_FRAG 0
#define UIP_CONF_BUFFER_SIZE 256
