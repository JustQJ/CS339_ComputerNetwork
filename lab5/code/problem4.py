#!/usr/bin/python

"""Simple example of setting network and CPU parameters  """

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import OVSBridge
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import quietRun, dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from sys import argv
import time
# It would be nice if we didn't have to do this:
# pylint: disable=arguments-differ



class SingleSwitchTopo( Topo):
    def build( self, bw1, bw2, bw3):
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
        host1 = self.addHost('h1', cpu=.10)
        host2 = self.addHost('h2', cpu=.10)
        host3 = self.addHost('h3', cpu=.10)
        host4 = self.addHost('h4', cpu=.10)
        host5 = self.addHost('h5', cpu=.10)
        host6 = self.addHost('h6', cpu=.10)

        self.addLink(host1, switch1, bw=bw1, delay='5ms', loss=0,use_htb=True)
        self.addLink(host2, switch1, bw=bw2, delay='5ms', loss=0, use_htb=True)
        self.addLink(host3, switch1, bw=bw3, delay='5ms', loss=0, use_htb=True)

        # the bettleneck 
        self.addLink(switch1, switch2, bw=100, delay='5ms', loss=0, use_htb=True)


        self.addLink(host4, switch2, bw=100, delay='5ms', loss=0,use_htb=True)
        self.addLink(host5, switch2, bw=100, delay='5ms', loss=0, use_htb=True)
        self.addLink(host6, switch2, bw=100, delay='5ms', loss=0, use_htb=True)

def Test(tcp, bw1, bw2, bw3):
    "Create network and run simple performance test"
    topo = SingleSwitchTopo(bw1, bw2, bw3)
    net = Mininet( topo=topo,
                    host=CPULimitedHost, link=TCLink,
                    autoStaticArp=False )
    net.start()
    info( "Dumping host connections\n" )
    dumpNodeConnections(net.hosts)  
    # set up tcp congestion control algorithm
    output = quietRun( 'sysctl -w net.ipv4.tcp_congestion_control=' + tcp )
    assert tcp in output
    info( "Testing bandwidth between h1 and h2 under TCP " + tcp + "\n" )
    h1, h2, h3, h4,h5,h6 = net.getNodeByName('h1', 'h2', 'h3','h4','h5','h6')

    #set servers
    h4.cmd("iperf -s > log4.txt &")
    h5.cmd("iperf -s > log5.txt &")
    h6.cmd("iperf -s > log6.txt &")

    # set clients
    h1.cmd("iperf -c 10.0.0.4 -t 10 > log1.txt &")
    h2.cmd("iperf -c 10.0.0.5 -t 10 > log2.txt &")
    h3.cmd("iperf -c 10.0.0.6 -t 10 > log3.txt &")

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')    
    # pick a congestion control algorithm, for example, 'reno', 'cubic', 'bbr', 'vegas', 'hybla', etc.   
    tcp = 'bbr'
    #tcp = 'reno'
    
    #set different bandwidth 
    Test(tcp, 100, 100, 100)
    #Test(tcp, 10, 40, 80)
