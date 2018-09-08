/*
 * Copyright (C) 2015 Texas Instruments Incorporated - http://www.ti.com/
 *
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * * Redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer.
 *
 * * Redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the
 * distribution.
 *
 * * Neither the name of Texas Instruments Incorporated nor the names of
 * its contributors may be used to endorse or promote products derived
 * from this software without specific prior written permission.
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


#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <sys/poll.h>

#include <sys/types.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#include <sys/mman.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <time.h>


#define MAX_BUFFER_SIZE 512
#define ADC_PAYLOAD_SIZE 384
char readBuf[MAX_BUFFER_SIZE];
#define DEVICE_NAME0 "/dev/rpmsg_pru30"
#define DEVICE_NAME1 "/dev/rpmsg_pru31"
#define ADC_PORT 10520
 

int main(void)
{
 struct pollfd pollfds[2];
 int result = 0;
 int pru_data;

 uint32_t i, number_of_samples;
 int32_t socket_desc , client_sock , c;
 struct sockaddr_in server , client;

 socket_desc = socket(AF_INET , SOCK_STREAM , 0);
 printf("created socket\n");
 i = 1;
 setsockopt(socket_desc, SOL_SOCKET, SO_REUSEADDR, &i, sizeof(i));
 server.sin_family = AF_INET;
 server.sin_addr.s_addr = INADDR_ANY;
 server.sin_port = htons(ADC_PORT);


 if( bind(socket_desc, (struct sockaddr *)&server, sizeof(server)) < 0 ) {
    printf("bind failed\n");
    return 1;
 }


 
 
 pollfds[1].fd = open(DEVICE_NAME1, O_RDWR);
   
 if (pollfds[1].fd < 0) {
 printf("Failed to open %s\n",DEVICE_NAME1);
 return -1;
 }
 
 listen(socket_desc, 3);

 while(1) {
    printf("waiting for incoming connections.."); 
    c = sizeof(struct sockaddr_in);
    client_sock = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c);

    if (client_sock < 0) {
        printf("socket accept failed!\n");
        break;
    }
    printf("accepted connection!\n");

    recv(client_sock, &number_of_samples, sizeof(number_of_samples), MSG_WAITALL);

    
    i = ADC_PAYLOAD_SIZE/4;
    write(client_sock, &i, sizeof(i));

    result = write(pollfds[1].fd, "hello world_1!",13);
    
    printf("kicked PRU1!\n");
    for(i = 0; i < 4; i++) {
        result = read(pollfds[1].fd,readBuf,ADC_PAYLOAD_SIZE);
        if(result > 0) printf("ADC %d data received from PRU_1\n",i);
        write(client_sock, readBuf, ADC_PAYLOAD_SIZE);
    }

    recv(client_sock, &number_of_samples, sizeof(number_of_samples), MSG_WAITALL);
    close(client_sock);
 }
    
 printf("error, exiting\n");
 close(client_sock);
 close(socket_desc);
 close(pollfds[1].fd);
 return 0;
}
