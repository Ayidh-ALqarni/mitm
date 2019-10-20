                                                                                             
from mininet.topo import Topo #Topo: the base class for Mininet topologies
from mininet.net import Mininet #Mininet: main class to create and manage a network
from mininet.util import dumpNodeConnections #dumpNodeConnections(): dumps connections to/from a set of nodes.
from mininet.log import setLogLevel #setLogLevel( 'info' | 'debug' | 'output' ): set Mininet's default output level; 'info' is recommended as it provides useful information.

class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def build(self, n=2):  #build The method to override in your topology class. Constructor parameters (n) will be passed through to it automatically by Topo.__init__()
        switch = self.addSwitch('s1') #addSwitch(): adds a switch to a topology and returns the switch name
        # Python's range(N) generates 0..N-1
        for h in range(n):
            host = self.addHost('h%s' % (h + 1)) #addHost(): adds a host to a topology and returns the host name
            self.addLink(host, switch) #addLink(): adds a bidirectional link to a topology (and returns a link key, but this is not important). Links in Mininet are bidirectional unless noted otherwise.

def simpleTest():
    "Create and test a simple network"
    topo = SingleSwitchTopo(n=2)
    net = Mininet(topo)
    net.start() #start(): starts your network
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll() #pingAll(): tests connectivity by trying to have all nodes ping each other
    net.stop() #stop(): stops your network

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
