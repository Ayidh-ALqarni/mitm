import os
from mininet.net import Mininet #Mininet:main class to create and manage a network
from mininet.node import Node, Controller, RemoteController
from mininet.log import setLogLevel, info #Set mininet's default output level
from mininet.cli import CLI
from mininet.topo import Topo #The base class for mininet Topologies
from mininet.util import quietRun #Stop TOPO
from mininet.moduledeps import pathCheck

CURR_PATH = os.getcwd() #getting the current path
DECODED_LOG_FILE_PATH = CURR_PATH +  "/decoded.log" #creating decode log file
LOG_FILE_PATH= CURR_PATH + "/logfile.log" #creating log file

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd("sysctl -w net.ipv4.ip_forward=1") #Setting up Ipv4 forwrding
        self.cmd("sysctl -p /etc/sysctl.conf")

    def terminate( self ):
        self.cmd("sysctl -w net.ipv4.ip_forward=0") #disabling Ipv4 Forwarding
        self.cmd("sysctl -p /etc/sysctl.conf")
        super( LinuxRouter, self ).terminate()

class SimpleTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        left_host = self.addHost( 'h1', ip='192.168.0.3/24',
            mac='00:00:00:00:00:01')
        right_host = self.addHost( 'h2', ip='192.168.0.4/24',
            mac='00:00:00:00:00:02')
        #attacker_host = self.addHost( 'h3', ip='192.168.0.5/24',
        #    mac='00:00:00:00:00:03')
        attacker_host = self.addNode( 'h3', cls=LinuxRouter, ip='192.168.0.5/24',
            mac='00:00:00:00:00:03')
        main_switch = self.addSwitch( 's1' )

        # Add links from the hosts to this single switch
        self.addLink( left_host, main_switch )
        self.addLink( right_host, main_switch )
        self.addLink( attacker_host, main_switch )

def start_sshd( host ):
    "Start sshd on host"
    stop_sshd()
    info( '*** Starting sshd in %s\n' % host.name )
    name, intf, ip = host.name, host.defaultIntf(), host.IP()
    banner = '/tmp/%s.banner' % name
       host.cmd( 'echo "Welcome to %s at %s" >  %s' % ( name, ip, banner ) )
       host.cmd( '/usr/sbin/sshd -o Banner=%s -o UseDNS=no' % banner)
       info( '***', host.name, 'is running sshd on', intf, 'at', ip, '\n' )

   def stop_sshd():
       "Stop *all* sshd processes with a custom banner"
       info( '*** Shutting down stale sshd/Banner processes ',
             quietRun( "pkill -9 -f Banner" ), '\n' )

   def create_attack_log(host):
       host.cmd("chmod 666 %s>>!#:2" % DECODED_LOG_FILE_PATH)
       host.cmd("chmod 666 %s>>!#:2" % LOG_FILE_PATH)

   def delete_attack_log(host):
       host.cmd("rm %s" % DECODED_LOG_FILE_PATH)
       host.cmd("rm %s" % LOG_FILE_PATH)

   def main():
       topo = SimpleTopo() # design topology
       info( '*** Creating network\n' )
       net = Mininet(topo=topo) #Passing Topology to Mininet Class
       net.start() # starting the networ

       # Print the elements of the network
       for item in net.items():
           print item

       print "Encoded log file at %s" % LOG_FILE_PATH
       print "Decoded log file at %s" % DECODED_LOG_FILE_PATH
       h1, h2, attacker, s1 = net.get('h1', 'h2', 'h3', 's1')
           # Start a ssh server on host 2
           start_sshd(h2)
           # Giving H3 rights to read and write Log Files of H2
           create_attack_log(attacker)
           #Console Logging the network
           CLI(net)
           #Stop sshd server
           stop_sshd()
           #delete all attack logs
           delete_attack_log(attacker)
           #stop network
           net.stop()

       if __name__ == '__main__':
           setLogLevel( 'info' )
           main()


