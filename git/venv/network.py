import xml.etree.ElementTree as ET
import re

class Node:
    def __init__(self, var_name, outcome, property=None):
        self.var_name = var_name # string, read from <'VARIABLE'>
        self.outcome = outcome # a list of string, read from <'VARIABLE'>
        self.parents = [] # a list of names of nodes, list size can be 0, 1, 2, ... read from <DEFINITION>=><GIVEN>
        self.children = [] # a list of nodes, list size can be 0, 1, 2, ...
        self.table = {} #{GIVEN: [p(FOR), p(!FOR)], !GIVEN: [p(FOR), p(!FOR)]} read from <DEFINITION>=><TABLE> given = [GIVEN].sort().toString()
        self.property = property

    def add_child(self, child):
        self.children.append(child)

    def add_parent(self, parent_name):
        self.parents.append(parent_name)

    def build_table(self, prob_list):
        evidence_list = self.evidence_list_generator(self.parents)
        i = 0
        for evidence in evidence_list:
            evidence.sort()
            evid_str = str(evidence)
            self.table[evid_str] = [prob_list[i], prob_list[i+1]]

    def evidence_list_generator(self, e):
        evidence_list = []
        length = len(e)
        period = (2 ** len(e)) / 2
        flip = False
        for i in range(2 ** length):
            evidence_list.append([])
        for col in range(length):
            j = 1
            for row in range(2 ** length):
                evidence_list[row].append(e[col])
                if flip:
                    evidence_list[row][col] = '!' + evidence_list[row][col]
                # print(row, col, probtable[row][col])
                j += 1
                if j > period:
                    flip = not flip
                    j = 1

            period = period / 2

        return evidence_list


class BayesianNetwork:
    def __init__(self):
        self.root = [] # list node.var_name with no parent
        self.vars2id = {} # a dict of all node.var_name to index in [vars] in the network
        self.vars = [] # a list of all nodes

    def init_network(self, file):
        network = ET.parse(file).getroot().find('NETWORK')
        #for var in network.findall('VARIABLE'):


