#include <pthread.h>
#include <stdio.h>
#include <stdio.h> // standard input and output library
#include <stdlib.h> // this includes functions regarding memory allocation 
#include <string.h> // contains string functions#include 
#include <errno.h> //It defines macros for reporting and retrieving error conditions through error codes#include 
#include <time.h> //contains various functions for manipulating date and time#include
#include <unistd.h> //contains various constants#include
#include <sys/types.h> //contains a number of basic derived types that should be used whenever appropriate#include 
#include <arpa/inet.h> // defines in_addr structure#include 
#include <sys/socket.h> // for socket creation#include 
#include <netinet/in.h> //contains constants and structures needed for internet domain addresses 

pthread_mutex_t mutex;
// the function for every thread
int BufSize = 1024;
int count = 100000;
int clinentNumber = 1024;

void *client_thread(void *client)
{


    


    int clientC = *(int*)client;//get the file description  
    char buffer[BufSize];
    
    memset(&buffer,'0', BufSize); 
    
    for(int i=0; i<count; i++)
    {
        snprintf(buffer, sizeof(buffer), "I'm client!\r\n");
        write(clientC, buffer, strlen(buffer));       
    } 

   close(clientC);

  


}


int main(){

    pthread_t client[clinentNumber]; //to store the threads
    int clientnum=0; //to recode the number of clients 
    
    pthread_attr_t attr;
    pthread_attr_init(&attr);



    struct sockaddr_in server, client_addr; // server
    socklen_t leng = sizeof(client_addr);
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    memset(&server, '0', sizeof(server));
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = htonl(INADDR_ANY);
    server.sin_port = htons(2020);
    bind(sock, (struct sockaddr*)&server, sizeof(server));
    listen(sock,20);

    

    while (1)
    {
        
        memset(&client_addr,'0',sizeof(client_addr));
        int clientcount = accept(sock,(struct sockaddr*)&client_addr, &leng); //get the client
        

        //print the information about the client
        char ip[16];
        char name[256];
         snprintf(name,sizeof(name),"client ip: %s, port: %d. \n", inet_ntop(AF_INET,&client_addr.sin_addr,ip,sizeof(ip)),
                ntohs(client_addr.sin_port));
        fputs(name,stdout);
       // printf(name);
        //creat the threads
         
        
         if(pthread_create(&client[clientnum], &attr,client_thread, (void*)&clientcount) ){        
            printf("Error creating thread\n");       
            return 1;    
            }    
        
       
        clientnum++;

        sleep(1);
    }

    close(sock);
    return 0;

    

}