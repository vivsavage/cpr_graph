__author__ = 'ron'

# import networkx as nx
import pydot as pd

NODE_ATTRS = {
    'addr': None,
    'lin': None,
    'size': None,
    'prot': None,
    'type': None
}

NODE_DOT_ATTRS = {
    'shape': 'box',
    'color': 'green'
}

EDGE_DOT_ATTRS = {
    'style': 'solid',
    'color': 'red'
}


class FsObj:
    def __init__(self, addr, lin):
        self.addr = addr
        self.lin = lin
        self.size = 512
        self.prot = '8x'
        self.type = 'inode'

    def __str__(self):
        return 'FsObj: %s' % self.addr

    @property
    def addr(self):
        return self.addr

    @property
    def lin(self):
        return self.lin

    @property
    def size(self):
        return self.size

    @property
    def prot(self):
        return self.prot

    @property
    def type(self):
        return self.type


def make_node_attrs(f):
    d = NODE_ATTRS

    d['addr'] = f.addr
    d['lin'] = f.lin
    d['size'] = f.size
    d['prot'] = f.prot
    d['type'] = f.type

    return d


if __name__ == "__main__":
    f1 = FsObj('2,4,75747474:512', '1:90ea:88b4')
    f2 = FsObj('4,9,47363987:512', '1:308c:fe41')

    print(f1)
    print(f2)

    fd1 = make_node_attrs(f1)
    fd2 = make_node_attrs(f2)

    graph = pd.Dot(graph_type='digraph')
    n1 = pd.Node(name="node 1", **NODE_DOT_ATTRS)
    n2 = pd.Node(name="node 2", **NODE_DOT_ATTRS)
    e1 = pd.Edge(n1, n2, **EDGE_DOT_ATTRS)

    graph.add_node(n1)
    graph.add_node(n2)
    graph.add_edge(e1)

    graph.write_svg("erk.svg")
