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

        self.addLink(centerSwitch, leftHost)
        self.addLink(centerSwitch, rightHost)

        self.addLink(rightSwitch, rightHost)
        self.addLink(rightSwitch, rightHostBottom)
        self.addLink(rightSwitch, leftSwitch)

        self.addLink(leftSwitch, leftHostBottom)
        self.addLink(leftSwitch, leftHost)


topos = {'mytopo': (lambda: MyTopo())}
