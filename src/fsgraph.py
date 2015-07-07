#!/usr/bin/env python

__author__ = 'atticus'

import sh
import re
import pydot as pd

from optparse import OptionParser

#
# TODO:
#
# - Change optparse to argparse
#

#
# cpr_test used for off-cluster development
# cpr = sh.Command('/usr/bin/isi_cpr')
cpr_test = sh.Command('/bin/cat')

# cpr_r_l = ' -r l'
# cpr_r_f = ' -r f'
# cpr_r_i = ' -r i'
# cpr_r_B = ' -r B'
# cpr_r_L = ' -r L'

# directory containing the cpr output
CPR = '../cpr/'

#
# testing cpr stuff
cpr_r_l = CPR + 'cpr_r_l_embedded_leaf.txt'
cpr_r_f = CPR + 'cpr_r_f_embedded_leaf.txt'
cpr_f_l = CPR + 'cpr_f_l_embedded_leaf.txt'

#
# production cpr options
cpr_r_i = ' -r i'
cpr_r_B = ' -r B'
cpr_r_L = ' -r L'

# regular expression patterns
INODE_PAT = '[0-9]{1,3},[0-9]{1,3},[0-9]+:512'
LIN_PAT = '[0-9a-f]{1,4}:[0-9a-f]{4}:[0-9a-f]{4}[::[0-9A-Z]+]'
BADDR_PAT = '[0-9]{1,3},[0-9]{1,3},[0-9]+:8192'

ip = re.compile(INODE_PAT)
lp = re.compile(LIN_PAT)
bp = re.compile(BADDR_PAT)

#
# attributes for the different node types
# on the digraph
#
INODE_ATTRS = {
    'shape': 'box',
    'style': 'solid',
    'color': 'green'
}

LIN_ATTRS = {
    'shape': 'box',
    'style': 'solid',
    'color': 'blue'
}

MASTER_ATTRS = {
    'shape': 'box',
    'style': 'solid',
    'color': 'red'
}

INNER_ATTRS = {
    'shape': 'box',
    'style': 'solid',
    'color': 'yellow'
}

LEAF_ATTRS = {
    'shape': 'box',
    'style': 'solid',
    'color': 'orange'
}


def get_inodes(s):
    """

    :rtype : dict
    """
    i = dict()
    i['inodes'] = ip.findall(s)
    return i


def get_lin_master(s):
    """

    :rtype : dict
    """
    l = dict()
    l['lin_masters'] = bp.findall(s)
    return l


def get_lin_inner(s):
    """

    :rtype : dict
    """
    li = dict()
    lib = dict()
    tokens = s.strip().split()
    for i in range(len(tokens)):
        if 'Entry' in tokens[i]:
            lib['entry'] = tokens[i + 1]
    blks = bp.findall(s)
    lib['blocks'] = blks

    return lib


def get_lin_leaf(s):
    """

    :rtype : dict
    """
    ll = dict()
    lib = dict()
    tokens = s.strip().split()
    for i in range(len(tokens)):
        if 'Entry' in tokens[i]:
            lib['entry'] = tokens[i + 1]
    blks = bp.findall(s)
    lib['blocks'] = blks
    ll['lin_leaf'] = lib

    return ll


def get_lin_info(lin):
    """

    :rtype : dict
    """
    li = dict()
    linfo = dict()

    with open('cpr_r_l.tmp', 'w') as f:
        f.write(str(cpr_test(cpr_r_l)))

    with open('cpr_r_l.tmp', 'r') as f:
        linfo['val'] = lin
        for line in f:
            if line.strip().startswith('di_size'):
                tokens = line.strip().split()
                linfo['size'] = tokens[1]
                linfo['blocks'] = tokens[3]
            if line.strip().startswith('di_logical_size'):
                tokens = line.strip().split()
                linfo['logical'] = tokens[1]
            if line.strip().startswith('current_prot'):
                tokens = line.strip().split()
                prot = (tokens[2], tokens[3], tokens[4], tokens[5])
                linfo['prot'] = '{0} {1}{2}{3}'.format(*prot)
            if line.strip().startswith('lin table snapid'):
                tokens = line.strip().split()
                crc = tokens[9]
                linfo['crc'] = crc
            if line.strip().startswith('Data Section'):
                if f.next().strip().startswith('Metatree'):
                    linfo['mt_type'] = 'Embedded'
                else:
                    linfo['mt_type'] = 'External'
    li['lin'] = linfo
    return li


def make_mirrors(key, n):
    """

    :param key: str or int
    :param n: dict
    :return: string
    """
    mirrors = 'mirrors: '
    for i in range(len(n[key])):
        if i == 0: continue
        mirrors = mirrors + n[key][i] + ' '
    return mirrors

def conv_chars(s):
    """

    :param s: string
    :return: string
    """
    return re.sub(':,', '_', s)

def make_node(n):
    node = None

    if 'inodes' in n:
        attrs = INODE_ATTRS
        attrs['tooltip'] = make_mirrors('inodes', n)
        name = conv_chars(['inodes'][0])
        attrs['label'] = 'inode: ' + name
        node = pd.Node(name=name, **attrs)

    if 'lin_masters' in n:
        attrs = MASTER_ATTRS
        attrs['tooltip'] = make_mirrors('lin_masters', n)
        name = conv_chars(n['lin_masters'][0])
        attrs['label'] = 'LIN Master: ' + name
        node = pd.Node(name=name, **attrs)

    if 'lin_inners' in n:
        name = k = n.keys()[0]
        attrs = INNER_ATTRS
        attrs['tooltip'] = make_mirrors('blocks', n[k])
        attrs['label'] = 'LIN Inner {0}\nEntry {1}'.format(name, n['entry'])
        node = pd.Node(name=name, **attrs)

    if 'lin_leaf' in n:
        name = k = n.keys()[0]
        attrs = LEAF_ATTRS
        attrs['tooltip'] = make_mirrors('blocks', n[k])
        attrs['label'] = 'LIN Leaf: ' + name
        node = pd.Node(name=name, **attrs)

    if 'lin' in n:
        attrs = LIN_ATTRS
        name = conv_chars(n['lin']['val'])
        attrs['label'] = 'LIN: {0}\nSize: {1}\nLogical Size: {2}\nBlocks: {3}\n' \
                         'Protection: {4}'.format(name, n['lin']['size'], n['lin']['logical'],
                                                  n['lin']['blocks'], n['lin']['prot'])
        node = pd.Node(name=name, **attrs)

    return node


def main():
    li_blocks = dict()
    lm_blocks = dict()
    ll_blocks = dict()
    li = dict()
    inodes = dict()
    li_nodes = dict()
    p = OptionParser()

    p.add_option('-l', '--lin', dest='lin',
                 help='LIN to map', metavar='<lin>')
    p.add_option('-d', '--debug', dest='debug',
                 help='Debug mode', action='store_true',
                 default=False)

    (o, a) = p.parse_args()

    # We can get all the LIN tree and inode
    # blocks from isi_cpr -f l<lin>
    cprinfo = cpr_test(cpr_f_l)

    lininfo = get_lin_info(o.lin)

    with open('cpr_f_l.tmp', 'w') as f:
        f.write(str(cprinfo))

    with open('cpr_f_l.tmp', 'r') as f:
        lcount = 0
        for line in f:
            if line.startswith('LIN'): continue
            if 'LIN Master' in line:
                lm_blocks = get_lin_master(line)
            if 'LIN Inner' in line:
                li_blocks[lcount] = get_lin_inner(line)
                lcount += 1
            if 'LIN Leaf' in line:
                ll_blocks = get_lin_leaf(line)
            if line.startswith('['):
                inodes = get_inodes(line)

    li['lin_inners'] = li_blocks

    if o.debug:
        print 'inodes: ' + str(inodes)
        print 'lin masters: ' + str(lm_blocks)
        print 'lin inners: ' + str(li)
        print 'lin leafs: ' + str(ll_blocks)
        print 'lin info: ' + str(lininfo)

    graph = pd.Dot(graph_type='digraph')

    in_node = make_node(inodes)
    lm_node = make_node(lm_blocks)
    for k in li['lin_inners'].keys():
        li_nodes[k] = make_node(li['lin_inners'][k])
    ll_node = make_node(ll_blocks)
    lin_node = make_node(lininfo)

    print in_node.to_string()

if __name__ == '__main__':
    main()
