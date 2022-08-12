
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER,DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet,ipv4,arp,ether_types
import time
from ryu.lib.packet import  in_proto as inet


class ExampleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(ExampleSwitch13, self).__init__(*args, **kwargs)
        # initialize mac address table.
        self.datapaths = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser


        self.datapaths[datapath.id] = datapath

        # install the table-miss flow entry.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions,0)

        #add flows
        #s1
        if datapath.id == 1:
            #s3-s1
            kwargs = dict(in_port = 2, eth_type=ether_types.ETH_TYPE_IP,
                    ipv4_src="10.0.0.2", ipv4_dst="10.0.0.1")
            match = parser.OFPMatch(**kwargs)
            actions = [parser.OFPActionOutput(1)]
            self.add_flow(datapath,1,match,actions,0)

            #s4-s1
            kwargs = dict(in_port = 3, eth_type=ether_types.ETH_TYPE_IP,
                    ipv4_src="10.0.0.2", ipv4_dst="10.0.0.1")
            match = parser.OFPMatch(**kwargs)
            actions = [parser.OFPActionOutput(1)]
            self.add_flow(datapath,1,match,actions,0)
            #group s1-s3,s1-s4

            kwargs = dict(in_port = 1, eth_type=ether_types.ETH_TYPE_IP,
                  ipv4_src="10.0.0.1", ipv4_dst="10.0.0.2")
            #kwargs = dict(in_port = 1)
            match = parser.OFPMatch(**kwargs)
            outport1 = 2
            outport2 = 3
            weight1 = 50
            weight2 = 50
            watch_port1 = 2
            watch_group1 = ofproto.OFPG_ANY
            watch_port2 = 3
            watch_group2 = ofproto.OFPG_ANY
            group_id = 2021
            self.add_group(datapath,match,outport1,outport2,weight1,weight2,watch_port1,watch_port2,watch_group1,watch_group2,group_id)

        #s2
        if datapath.id == 2:
            #s3-s2
            kwargs = dict(in_port = 2, eth_type=ether_types.ETH_TYPE_IP,
                    ipv4_src="10.0.0.1", ipv4_dst="10.0.0.2")
            match = parser.OFPMatch(**kwargs)
            actions = [parser.OFPActionOutput(1)]
            self.add_flow(datapath,1,match,actions,0)

            #s4-s2
            kwargs = dict(in_port = 3, eth_type=ether_types.ETH_TYPE_IP,
                    ipv4_src="10.0.0.1", ipv4_dst="10.0.0.2")
            match = parser.OFPMatch(**kwargs)
            actions = [parser.OFPActionOutput(1)]
            self.add_flow(datapath,1,match,actions,0)
           
            #group s2-s3,s2-s4
            kwargs = dict(in_port = 1, eth_type=ether_types.ETH_TYPE_IP,
                    ipv4_src="10.0.0.2", ipv4_dst="10.0.0.1")
            match = parser.OFPMatch(**kwargs)
            outport1 = 2
            outport2 = 3
            weight1 = 50
            weight2 = 50
            watch_port1 = 2
            watch_group1 = ofproto.OFPG_ANY
            watch_port2 = 3
            watch_group2 = ofproto.OFPG_ANY
            group_id = 2022
            self.add_group(datapath,match,outport1,outport2,weight1,weight2,watch_port1,watch_port2,watch_group1,watch_group2,group_id)

            
            

        #s3
        if datapath.id == 3:     
            kwargs = dict(in_port = 1, eth_type=ether_types.ETH_TYPE_IP,
                    ipv4_src="10.0.0.1", ipv4_dst="10.0.0.2")
            match = parser.OFPMatch(**kwargs)
            actions = [parser.OFPActionOutput(2)]
            self.add_flow(datapath,1,match,actions,0)
            
            kwargs = dict(in_port = 2, eth_type=ether_types.ETH_TYPE_IP,
                    ipv4_src="10.0.0.2", ipv4_dst="10.0.0.1")
            match = parser.OFPMatch(**kwargs)
            actions = [parser.OFPActionOutput(1)]
            self.add_flow(datapath,1,match,actions,0)

        #s4
        if datapath.id == 4:  
            kwargs = dict(in_port = 1, eth_type=ether_types.ETH_TYPE_IP,
                    ipv4_src="10.0.0.1", ipv4_dst="10.0.0.2")
            match = parser.OFPMatch(**kwargs)
            actions = [parser.OFPActionOutput(2)]
            self.add_flow(datapath,1,match,actions,0)
            
            kwargs = dict(in_port = 2, eth_type=ether_types.ETH_TYPE_IP,
                    ipv4_src="10.0.0.2", ipv4_dst="10.0.0.1")
            match = parser.OFPMatch(**kwargs)
            actions = [parser.OFPActionOutput(1)]
            self.add_flow(datapath,1,match,actions,0)

        

    def add_group(self,datapath,match,outport1,outport2,weight1,weight2,watch_port1,watch_port2,watch_group1,watch_group2,group_id):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        actions1 = [parser.OFPActionOutput(outport1)]
        actions2 = [parser.OFPActionOutput(outport2)]
        buckets = [parser.OFPBucket(weight1, watch_port1, watch_group1,
                                        actions1),
                    parser.OFPBucket(weight2, watch_port2, watch_group2,
                                        actions2)]
        
        req = parser.OFPGroupMod(datapath, ofproto.OFPGC_ADD,
                                ofproto.OFPGT_SELECT, group_id, buckets)
        datapath.send_msg(req)
        actions = [parser.OFPActionGroup(group_id=group_id)]
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                                actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=1,
                                match=match, instructions=inst)
        datapath.send_msg(mod)




    def add_flow(self, datapath, priority, match, actions,timeout):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst,hard_timeout=timeout)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # get Datapath ID to identify OpenFlow switches.
        dpid = datapath.id

        # analyse the received packets using the packet library.
        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        ipv4_pkt = pkt.get_protocol(ipv4.ipv4)
        #arp_pkt = pkt.get_protocol(arp.arp)
        dst = eth_pkt.dst
        src = eth_pkt.src
        ethtype = eth_pkt.ethertype

        in_port = msg.match['in_port']

        # get the received port number from packet_in message.
        

        self.logger.info("packet in %s  %s %s %s %s", dpid, src, dst, in_port,ethtype)
        if ipv4_pkt:
            ipv4dst = ipv4_pkt.dst
            ipv4src = ipv4_pkt.src
            self.logger.info("packet ipv4 in %s  %s %s %s %s", dpid, ipv4src, ipv4dst, in_port,ethtype)
        if ethtype == ether_types.ETH_TYPE_LLDP:  #ingore the LLDP packet
            return

        if ethtype == ether_types.ETH_TYPE_ARP or ethtype == ether_types.ETH_TYPE_IP: #deal with the arp packet
            if in_port == 1:
                actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
            if in_port == 2 or in_port==3:
                actions = [parser.OFPActionOutput(1)]


            # construct packet_out message and send it.
            out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=ofproto.OFP_NO_BUFFER,
                                  in_port=in_port, actions=actions,
                                  data=msg.data)
            datapath.send_msg(out)






            

        



        

