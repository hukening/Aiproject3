import xml.etree.ElementTree as ET
import re

class BayesianNetwork():
    def __init__(self, file):
        self.file = file
        self.network = ET.parse(file).getroot().find('NETWORK')
        self.vars = self.get_variable()
        self.bn = self.prob_network()

    def get_probability(self, query, evidence_list): #given a list of evidence
        #get the table in DEFINITION, return a list of probabilities
        probabilities = ""
        for definition in self.network.findall('DEFINITION'):
            if query == definition.find('FOR').text:
                evids = []
                contains = True
                if evidence_list!=[]:
                    for evid in definition.findall('GIVEN'):
                        evids.append(evid.text)
                    for evidence in evidence_list:
                        if evidence not in evids:
                            contains = False
                            break
                if contains:
                    probabilities = definition.find('TABLE').text
                    break

        probabilities_list = re.findall(r'\S+', probabilities)
        return probabilities_list

    def get_property(self, name): #return property of a certain var with name "name"
        property = ""
        for variable in self.network.findall('VARIABLE'):
            if variable.find('NAME')==name:
                property = variable.find('PROPERTY').text
                break
        return property

    def get_variable(self):
        vars = []
        for variable in self.network.findall('VARIABLE'):
            name = variable.find('NAME').text
            vars.append(name.upper())
        return vars

    def prob_network(self): #[[for, [given], prob.]]
        prob_network = []
        new_i=[[]]
        for definition in self.network.findall('DEFINITION'):
            query = definition.find('FOR').text
            evidence = []
            for evid in definition.findall('GIVEN'):
                evidence.append(evid.text)

            probabilities = definition.find('TABLE').text
            probabilities_list = re.findall(r'\S+', probabilities)
            evidence_list = self.init_probtable(evidence)
            for e in range(len(evidence_list)):
                prob_network.append([[query], evidence_list[e], float(probabilities_list[2 * e])])
                not_query = '!'+query
                prob_network.append([[not_query], evidence_list[e], float(probabilities_list[2 * e + 1])])
        for i in range(len(prob_network)):
            if len(prob_network[i][0][0])==1:
                prob_network[i][0][0]=prob_network[i][0][0].lower()
            if len(prob_network[i][0][0])==2:
                prob_network[i][0][0]='!'+prob_network[i][0][0].strip('!').lower()

            if len(prob_network[i][1])!=0:
                for j in range(len(prob_network[i][1])):
                    if len(prob_network[i][1][j])==1:
                        prob_network[i][1][j]=prob_network[i][1][j].lower()
                    if len(prob_network[i][1][j])==2:
                        prob_network[i][1][j]='!'+prob_network[i][1][j].strip('!').lower()

        return prob_network

    def init_probtable(self, e):
        length = len(e)
        period = (2 ** len(e)) / 2
        flip = False
        probtable = []
        for i in range(2 ** length):
            probtable.append([])
        for col in range(length):
            j = 1
            for row in range(2 ** length):
                probtable[row].append(e[col])
                if flip:
                    probtable[row][col] = '!' + probtable[row][col]
                # print(row, col, probtable[row][col])
                j += 1
                if j > period:
                    flip = not flip
                    j = 1

            period = period / 2

        return probtable


    def is_empty(self,vars):
        if len(vars)==0:
            return True
        return False

    def get_first(self):
        #get the first variable and remove it from vars
        length = len(self.vars)
        first = self.vars[0]
        self.vars = self.vars[1:length]
        return first

    def get_parents(self, Y):
        parent = []
        network = parser.prob_network()
        for i in network:
            boo=False
            # print(len(i[1]))
            # print(i[0])
            if Y==i[0][0] and len(i[1])!= 0:
                count = 0
                for j in range(len(i[1])):
                    if i[1][j][0]!='!':
                        count+=1
                        if count == len(i[1]):
                            parent=i[1]
                            return parent
        return parent

    def split_list(self,vars_input):  # vars_input: input string
        # print(type(vars_input))
        vars_all=self.get_variable()
        input_list = vars_input.split(' ')
        hidden_vars=[]
        given_vars=[]
        split_vars=[]
        for i in vars_all:
            if i.upper() not in input_list:
                hidden_vars.append(i.upper())
        i=1
        while i<len(input_list)-1:
           if input_list[i+1] == 'true':
               given_vars.append(input_list[i].lower())
               i += 2
           elif input_list[i+1] == 'false':
               given_vars.append(('!'+input_list[i].lower()))
               i += 2
        if input_list[0][0]!='!':

            split_vars.append([input_list[0].lower()])
        else:
            split_vars.append(['!'+input_list[0].strip('!').lower()])
        split_vars.append(given_vars)
        split_vars.append(hidden_vars)
        return split_vars

    def ordered_list(self,variable_list):
        #variable_list=[]
        final_list=[]
       # variable_list=self.get_variable()
        #variable_parents=[]
        while len(variable_list)!=0:
            variable_parents = self.get_parents(variable_list[0].lower())
            if len(variable_parents)==0:
                final_list.append(variable_list[0])
                variable_list.pop(0)
            else:
                count=0
                for i in variable_parents:
                    if i.upper() in final_list:
                        count+=1
                if count==len(variable_parents):
                    final_list.append(variable_list[0])
                    variable_list.pop(0)
                else:
                    variable_list.append(variable_list[0])
                    variable_list.pop(0)

        return final_list


    def get_evidence(self,split_list):
        e=[]
        for i in range(len(split_list)-1):
            for j in split_list[i]:
                e.append(j)
        return e

#xmlparser('examples/aima-alarm.xml')

#parser = BayesianNetwork('examples/aima-wet-grass.xml')
parser = BayesianNetwork('examples/aima-alarm.xml')
#print(parser.get_probability('A', ['B', 'E']))
#print(parser.get_evidence_list())  # get parents
# print('all vars: ', parser.get_variable())
#print(parser.vars)
#print(parser.init_probtable(['A', 'B']))
# print('network: ', parser.prob_network())
#print(parser.get_parents(['!J']))
# print(parser.split_list(['B','A','J']))

#b = 'FAMILY-OUT LIGHT-ON true HEAR-BARK false'
b='B J true M false'
#print(type(b))
a = parser.split_list(b)
# e = parser.get_evidence(a)
# #print('input sentence: ', b)
print('splitted list: ', a)
# print('evidence: ', e)
# print('parents of light-on: ', parser.get_parents('light-on'))
# all_vars = parser.get_variable()
# ordered = parser.ordered_list(all_vars)
# print('ordered list: ', ordered)
