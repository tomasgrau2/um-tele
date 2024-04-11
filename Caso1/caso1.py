from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding routers\n' )
    r0 = net.addHost('r0', ip = '192.168.100.6/29')
    r1 = net.addHost('r1', ip = '192.168.100.1/29')
    r2 = net.addHost('r2', ip = '192.168.100.9/29')
    r0.cmd( 'sysctl net.ipv4.ip_forward=1' )
    r1.cmd( 'sysctl net.ipv4.ip_forward=1' )
    r2.cmd( 'sysctl net.ipv4.ip_forward=1' )


    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone')
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, failMode='standalone')
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch, failMode='standalone')

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.1.254/24', defaultRoute="10.0.1.1")
    h2 = net.addHost('h2', cls=Host, ip='10.0.2.254/24', defaultRoute="10.0.2.1")

    info( '*** Add links\n')
    net.addLink(s1, r0, intfName2='r0-eth1', params2={'ip': '192.168.100.6/29'})
    net.addLink(s2, r0, intfName2='r0-eth2', params2={'ip': '192.168.100.14/29'})

    net.addLink(s1, r1, intfName1='s1-eth2', intfName2='r1-eth1', params2={'ip': '192.168.100.1/29'})
    net.addLink(s2, r2, intfName1='s2-eth2', intfName2='r2-eth1', params2={'ip': '192.168.100.9/29'})

    net.addLink(r1, s3, intfName1='r1-eth2', params1={'ip': '10.0.1.1/24'})
    net.addLink(r2, s4, intfName1='r2-eth2', params1={'ip': '10.0.2.1/24'})

    net.addLink(s3,h1)
    net.addLink(s4,h2)

    info( '*** Add routes\n')
    h1.cmd('ip route add 192.168.100.0/29 via 10.0.1.1')
    h1.cmd('ip route add 192.168.100.8/29 via 10.0.1.1')
    h1.cmd('ip route add 10.0.2.0/24 via 10.0.1.1')


    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([])
    net.get('s2').start([])
    net.get('s3').start([])
    net.get('s4').start([])
    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()