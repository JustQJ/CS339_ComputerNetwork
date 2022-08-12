#!/usr/bin/env python
import sys

from functools import partial

from mininet.net import Mininet
from mininet.node import UserSwitch, OVSKernelSwitch, Controller, CPULimitedHost
from mininet.topo import Topo
from mininet.log import lg, info, setLogLevel
from mininet.util import irange, quietRun
from mininet.util import dumpNodeConnections
from mininet.link import TCLink


class networkTopo(Topo):
	def build(self,**params):
		# define the host
		h1  = self.addHost('h1')	
		h2  = self.addHost('h2')
		h3  = self.addHost('h3')
		#define the switch
		s1 = self.addSwitch('s1')
		s2 = self.addSwitch('s2')
		s3 = self.addSwitch('s3')

		#define the link
		self.addLink(h1, s1)
		self.addLink(s1, s2, bw=10, loss=5)
		self.addLink(s1, s3, bw=10, loss=5)
		self.addLink(s3, h3)
		self.addLink(h2, s2)

def throughputTest():
	#create the network
	topo = networkTopo()
	net = Mininet(topo=topo,
                   host=CPULimitedHost, link=TCLink,
                   autoStaticArp=True )

	net.start()
	info( "Dumping host connections\n" )
    	dumpNodeConnections(net.hosts)
	info("Testing the TCP throughput between every host pair\n")
	h1, h2, h3 = net.getNodeByName('h1','h2','h3')
	info("h1 and h2:\n")
	net.iperf((h1,h2), l4Type = 'TCP')
	info("h1 and h3:\n")
	net.iperf((h1,h3), l4Type = 'TCP')
	info("h2 and h3:\n")
	net.iperf((h2,h3), l4Type = 'TCP')
	net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    # testing
    throughputTest()