#!/usr/bin/python

"""Simple example of setting network and CPU parameters  """
from os import PathLike
import re
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSBridge
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import quietRun, dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from sys import argv
import time

import math
import matplotlib.pyplot as plt
# It would be nice if we didn't have to do this:
# # pylint: disable=arguments-differ



class SingleSwitchTopo( Topo ):
    def build( self,b,d,l ):
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
        host1 = self.addHost('h1', cpu=.25)
        host2 = self.addHost('h2', cpu=.25)
        self.addLink(host1, switch1, bw=b,delay=d, loss=l, use_htb=True)
        self.addLink(host2, switch2, bw=b, delay=d, loss=l, use_htb=True)
        self.addLink(switch1, switch2, bw=b, delay=d, loss=l, use_htb=True)
        
def Test(tcp,bw,delay,loss):
    "Create network and run simple performance test"
    topo = SingleSwitchTopo(bw, delay,loss)
    net = Mininet( topo=topo,
                    host=CPULimitedHost, link=TCLink,
                    autoStaticArp=False )
    net.start()
    info( "Dumping host connections\n" )
    dumpNodeConnections(net.hosts)     
    output = quietRun( 'sysctl -w net.ipv4.tcp_congestion_control=' + tcp )
    assert tcp in output
    info( "Testing bandwidth between h1 and h2 under TCP " + tcp + "\n" )
    h1, h2,s1 = net.getNodeByName('h1', 'h2','s1')

    _serverbw, clientbw = net.iperf( [ h1, h2 ], seconds=5 )
    #info( clientbw, '\n' )
    #CLI(net)
    net.stop()
    return clientbw


def stoi(result):
    number=0
    lens=1
    flag = True
    flag1 = False
    flag2 = False
    for i in range(len(result)):
        if result[i].isdigit()  and flag:
            print(result[i])
            number=number*10+float(result[i])
        elif result[i].isdigit() and not flag:
            number = number+float(result[i])/pow(10,lens)
            lens = lens + 1
        elif result[i] == '.':
            flag = False
        elif result[i] == 'K':
            flag1 = True
            break
        elif result[i] == 'M':
            flag2 = True
            break

    if flag1: #kb/s
        number = number/1000
    if not flag2 and not flag1: #b/s
        number = number/1000000
    
    return number
    

if __name__ == '__main__':
    setLogLevel('info')    
    # pick a congestion control algorithm, for example, 'reno', 'cubic', 'bbr', 'vegas', 'hybla', etc.   
    tcp1 = 'reno'
    tcp2 = 'bbr'

    losss1  = [i*0.5 for i in range(0,18,1)]
    bws = [i*10 for i in range(1,21)]
    delays = [str(i)+'ms' for i in range(5,205,5)]
    delayss = [i for i in range(5,205,5)]
    result_throughput_reno = [[] for i in range(3)] #0 for loss, 1 for bw, 2 for delay
    result_throughput_bbr = [[] for i in range(3)]


    
    # the losss vary, bandwidth=100, dalay =5
    for loss in losss1:
        result_throughput_reno[0].append(stoi(Test(tcp1, 100, '5ms', loss)))
        result_throughput_bbr[0].append(stoi(Test(tcp2, 100, '5ms', loss)))

    
    # the bandwitdh vary, loss = 0, dalay =5
    for bw in bws:
        result_throughput_reno[1].append(stoi(Test(tcp1, bw, '5ms', 0)))
        result_throughput_bbr[1].append(stoi(Test(tcp2, bw, '5ms', 0)))


    # the delay vary, bandwidth=100, loss = 0
    for delay in delays:
        result_throughput_reno[2].append(stoi(Test(tcp1, 100, delay, 0)))
        result_throughput_bbr[2].append(stoi(Test(tcp2, 100, delay, 0)))


    #draw the figure
 
    plt.subplot(231)
    plt.plot(losss1,result_throughput_reno[0])
    plt.xlabel('loss rate/ %')
    plt.ylabel('throughput\Mbits/sec')
    plt.title('throughput varies with loss rate of TCP reno')

    plt.subplot(232)
    plt.plot(bws,result_throughput_reno[1])
    plt.xlabel('bandwidth\Mbits/sec')
    plt.ylabel('throughput\Mbits/sec')
    plt.title('throughput varies with bandwidth of TCP reno')

    plt.subplot(233)
    plt.plot(delayss,result_throughput_reno[2])
    plt.xlabel('delay/ms')
    plt.ylabel('throughput\Mbits/sec')
    plt.title('throughput varies with delay of TCP reno')


    plt.subplot(234)
    plt.plot(losss1,result_throughput_bbr[0])
    plt.xlabel('loss rate/ %')
    plt.ylabel('throughput\Mbits/sec')
    plt.title('throughput varies with loss rate of TCP bbr')

    plt.subplot(235)
    plt.plot(bws,result_throughput_bbr[1])
    plt.xlabel('bandwidth\Mbits/sec')
    plt.ylabel('throughput\Mbits/sec')
    plt.title('throughput varies with bandwidth of TCP bbr')

    plt.subplot(236)
    plt.plot(delayss,result_throughput_bbr[2])
    plt.xlabel('delay/ms')
    plt.ylabel('throughput\Mbits/sec')
    plt.title('throughput varies with delay of TCP bbr')


    
    plt.show()


    print("****************************************")
    print(result_throughput_reno)
    print("***********************************************************")
    print(result_throughput_bbr)



