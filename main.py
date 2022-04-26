# This is a sample Python script.
from mininet.topo import Topo


# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class MyTopo(Topo):

    def build(self):
        leftHost = self.addHost('h1')
        rightHost = self.addHost('h3')
        leftHostBottom = self.addHost('h2')
        rightHostBottom = self.addHost('h4')

        rightSwitch = self.addSwitch('S2')
        leftSwitch = self.addSwitch('S1')
        centerSwitch = self.addSwitch('S3')

        self.addLink(leftHost, centerSwitch)
        self.addLink(centerSwitch, rightHost)
        self.addLink(rightHost, rightSwitch)
        self.addLink(rightSwitch, leftSwitch)
        self.addLink(leftSwitch, leftHost)
        self.addLink(leftSwitch, leftHostBottom)
        self.addLink(rightSwitch, rightHostBottom)


topos = { 'mytopo': (lambda: MyTopo())}
