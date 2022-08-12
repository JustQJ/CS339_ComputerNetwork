import sys

from functools import partial

from mininet.net import Mininet
from mininet.node import UserSwitch, OVSKernelSwitch, Controller
from mininet.topo import Topo
from mininet.log import lg, info
from mininet.util import irange, quietRun
from mininet.link import TCLink
from mininet.node import CPULimitedHost
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

class netTopo(Topo):
    #define the star network  
    def build(self, N, **params):
        #N clients and one server and N switches
        server = self.addHost('server')
        switch = self.addSwitch('s1')
        clients = [self.addHost('client%s' %h) for h in irange(1,N)]
        
        #add links 
        self.addLink(server,switch,bw=1, delay='5ms', loss=0, use_htb=True)
        for client in clients:
            self.addLink(client, switch,bw=1, delay='5ms', loss=0, use_htb=True)
        
        
            


def netTest(N): # N is the clients number
    topo = netTopo(N)    
    net = Mininet( topo=topo,                   
                    host=CPULimitedHost, link=TCLink,                   
                    autoStaticArp=True )  
    net.start()    
    info( "Dumping host connections\n" )    
    dumpNodeConnections(net.hosts)

    server = net.getNodeByName('server')
    clients = [net.getNodeByName('client%s' %h) for h in irange(1,N)]
    

    #set the server and clients
    server.cmd("./multserver &")
    for i in range(1,N+1):
        # write the outputs of clients to the client.txt, the output is the time 
        clients[i-1].cmd("./client %s >> cilent.txt &" %i) 
        
    CLI(net)    
    net.stop()

if __name__=='__main__':
    #define N clients
    N=10  
    netTest(N)


        
