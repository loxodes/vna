/*
 * Copyright (C) 2016 Texas Instruments Incorporated - http://www.ti.com/
 *
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 *  * Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 *  * Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the
 *    distribution.
 *
 *  * Neither the name of Texas Instruments Incorporated nor the names of
 *    its contributors may be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#include <stdint.h>
#include <stdio.h>
#include <pru_cfg.h>
#include <pru_intc.h>
#include <rsc_types.h>
#include <pru_rpmsg.h>
#include "resource_table_1.h"

volatile register uint32_t __R31;
volatile register uint32_t __R30;

/* Host-1 Interrupt sets bit 31 in register R31 */
#define HOST_INT            ((uint32_t) 1 << 31)

/* The PRU-ICSS system events used for RPMsg are defined in the Linux device tree
 * PRU0 uses system event 16 (To ARM) and 17 (From ARM)
 * PRU1 uses system event 18 (To ARM) and 19 (From ARM)
 */
#define TO_ARM_HOST         18
#define FROM_ARM_HOST       19

/*
 * Using the name 'rpmsg-client-sample' will probe the RPMsg sample driver
 * found at linux-x.y.z/samples/rpmsg/rpmsg_client_sample.c 
 * ?? root@beaglebone:/lib/modules/4.4.91-ti-r133/kernel/samples/rpmsg/rpmsg_client_sample.ko
 *
 * Using the name 'rpmsg-pru' will probe the rpmsg_pru driver found
 
 * at linux-x.y.z/drivers/rpmsg/rpmsg_pru.c  ( rpmsg_pru.ko )
 * ?? root@beaglebone:/lib/modules/4.4.91-ti-r133/kernel/drivers/rpmsg/rpmsg_pru.ko

 */
//#define CHAN_NAME         "rpmsg-client-sample"
#define CHAN_NAME           "rpmsg-pru"

#define CHAN_DESC           "Channel 31"
#define CHAN_PORT           31

/*
 * Used to make sure the Linux drivers are ready for RPMsg communication
 * Found at linux-x.y.z/include/uapi/linux/virtio_config.h
 */
#define VIRTIO_CONFIG_S_DRIVER_OK   4

uint8_t payload[RPMSG_BUF_SIZE];

#define NUM_SAMPLES 96 

#define PRU_SHAREDMEM 0x00010000
volatile uint32_t *shared_mem = (volatile uint32_t *) PRU_SHAREDMEM;

#define CLKOUT 0x20
#define FS 0x10
#define DOUTA1_MASK 0x01
#define DOUTA2_MASK 0x02
#define DOUTA3_MASK 0x04
#define DOUTA4_MASK 0x08


void readadc(uint16_t offset) {
    uint32_t adc1, adc2, adc3, adc4;
    uint16_t i;
    while(!(__R31 & FS));
    while((__R31 & FS));

    for(i=0; i < 32; i++) {
        while((__R31 & CLKOUT));

        adc1 <<= 1;
        adc2 <<= 1;
        adc3 <<= 1;
        adc4 <<= 1;
    
        if(__R31 & DOUTA1_MASK) {
            adc1 |= 0x01;
        }
        if(__R31 & DOUTA2_MASK) {
            adc2 |= 0x01;
        }
        if(__R31 & DOUTA3_MASK) {
            adc3 |= 0x01;
        }
        if(__R31 & DOUTA4_MASK) {
            adc4 |= 0x01;
        }

        while(!(__R31 & CLKOUT));
    }
    shared_mem[4*offset+0] = adc1; 
    shared_mem[4*offset+1] = adc2; 
    shared_mem[4*offset+2] = adc3; 
    shared_mem[4*offset+3] = adc4;
    
}

void copy_adc_to_payload(uint16_t adc)
{
    /* todo: clean this up, typecast payload as uint32_t...?*/
    uint16_t i = 0;
    for(i = 0; i < NUM_SAMPLES; i++) {
        payload[4*i+0] = (shared_mem[4*i+adc] >> 0) & 0xFF;
        payload[4*i+1] = (shared_mem[4*i+adc] >> 8) & 0xFF;
        payload[4*i+2] = (shared_mem[4*i+adc] >> 16) & 0xFF;
        payload[4*i+3] = (shared_mem[4*i+adc] >> 24) & 0xFF;
    }
}
void main(void)
{
    struct pru_rpmsg_transport transport;
    uint16_t src, dst, len, i;
    volatile uint8_t *status;

    /* Allow OCP master port access by the PRU so the PRU can read external memories */
    CT_CFG.SYSCFG_bit.STANDBY_INIT = 0;

    /* Clear the status of the PRU-ICSS system event that the ARM will use to 'kick' us */
    CT_INTC.SICR_bit.STS_CLR_IDX = FROM_ARM_HOST;

    /* Make sure the Linux drivers are ready for RPMsg communication */
    status = &resourceTable.rpmsg_vdev.status;
    while (!(*status & VIRTIO_CONFIG_S_DRIVER_OK));

    /* Initialize the RPMsg transport structure */
    pru_rpmsg_init(&transport, &resourceTable.rpmsg_vring0, &resourceTable.rpmsg_vring1, TO_ARM_HOST, FROM_ARM_HOST);

    /* Create the RPMsg channel between the PRU and ARM user space using the transport structure. */
    while (pru_rpmsg_channel(RPMSG_NS_CREATE, &transport, CHAN_NAME, CHAN_DESC, CHAN_PORT) != PRU_RPMSG_SUCCESS);
    while (1) {
        /* Check bit 30 of register R31 to see if the ARM has kicked us */
        if (__R31 & HOST_INT) {
            /* Clear the event status */
            CT_INTC.SICR_bit.STS_CLR_IDX = FROM_ARM_HOST;
           
            /* Receive all available messages, multiple messages can be sent per kick */
            while (pru_rpmsg_receive(&transport, &src, &dst, payload, &len) == PRU_RPMSG_SUCCESS) {
                for(i = 0; i < NUM_SAMPLES; i++) {
                    readadc(i);                
                }
                for(i = 0; i < 4; i++) {
                    copy_adc_to_payload(i);
                    pru_rpmsg_send(&transport, dst, src, payload, NUM_SAMPLES * 4);
                }
            }
        }
    }
}
