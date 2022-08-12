#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h> 
#include <time.h>
#include <string>
int BufSize = 1024;
int main(int argc, char *argv[]){

    if(argc!=2)
        return 0;
    int clientIndex=atoi(argv[1]);  //to get the client index


    time_t clock;
    int CreateSocket = 0,n = 0;    
    char dataReceived[BufSize];    
    struct sockaddr_in ipOfServer;     
    memset(dataReceived, '0' ,sizeof(dataReceived));     
    if((CreateSocket = socket(AF_INET, SOCK_STREAM, 0))< 0)    
    {        
        printf("Socket not created \n");        
        return 1;    
    }     
    ipOfServer.sin_family = AF_INET;    
    ipOfServer.sin_port = htons(2020);    
    ipOfServer.sin_addr.s_addr = inet_addr("10.0.0.11");     
    if(connect(CreateSocket, (struct sockaddr *)&ipOfServer, sizeof(ipOfServer))<0)    
    {        
        printf("Connection failed due to port and ip problems\n");        
        return 1;    
    } 


    //print the starting time
    
    snprintf(dataReceived, sizeof(dataReceived), "%d", clientIndex); 
    if(fputs(dataReceived, stdout) == EOF)        
    {            
    printf("\nStandard output error");        
    }
    snprintf(dataReceived, sizeof(dataReceived), " starting time: ");
    if(fputs(dataReceived, stdout) == EOF)        
    {            
    printf("\nStandard output error");        
    }
    clock = time(NULL); 
    snprintf(dataReceived, sizeof(dataReceived), "%.24s\r\n", ctime(&clock));
    if(fputs(dataReceived, stdout) == EOF)        
    {            
        printf("\nStandard output error");        
    }   


    //creat the file index.txt file to store the data coming from the server
    char filename[20]="./clientsData/";
    strcat(filename, argv[1]);
    char tt[10] = ".txt";
    strcat(filename, tt);
    
    FILE *outfile;
    outfile = fopen(filename,"a+");

    //receive the data
    while((n = read(CreateSocket, dataReceived, sizeof(dataReceived)-1)) > 0)    
    {        
        dataReceived[n] = 0;        
        if(fputs(dataReceived, outfile) == EOF)     //write the data to the file    
        {            
            printf("\nStandard output error");        
        }         
        
    }     
    if( n < 0)    
    {        
        printf("Standard input error \n");    
        
    }  


    //print the ending time of this client
    snprintf(dataReceived, sizeof(dataReceived),"%d", clientIndex); 
    if(fputs(dataReceived, stdout) == EOF)        
    {            
    printf("\nStandard output error");        
    }
    snprintf(dataReceived, sizeof(dataReceived), " ending time:   ");
    if(fputs(dataReceived, stdout) == EOF)        
    {            
    printf("\nStandard output error");        
    }
    clock = time(NULL);  

    snprintf(dataReceived, sizeof(dataReceived), "%.24s\r\n", ctime(&clock));
    if(fputs(dataReceived, stdout) == EOF)        
    {            
        printf("\nStandard output error");        
    }   


    return 0;
}