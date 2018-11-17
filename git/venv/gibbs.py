from bayesianNetwork import BayesianNetwork
from mybninferencer import MyBnInferencer
import random

class gibbssampling():

    def __init__(self, gib_bn, gib_mybninfer):
        self.gib_bn = gib_bn
        self.gib_mybinfer = gib_mybninfer
        self.bn_network = self.gib_bn.prob_network()
        self.variable_list = self.gib_bn.get_variable()
        self.split_list = []
        self.change_hidden_list=[]

    def get_random_value(self):  # split_list: comes from input
        change_list = []
        hiddenlist = []
        hiddenlist.append(self.split_list[0][0].upper())
        for i in self.split_list[2]:
            hiddenlist.append(i)  # upper letters
        for i in hiddenlist:
            boo_value = random.choice([True, False])
            if boo_value:
                change_list.append(i.lower())
            else:
                change_list.append('!' + i.lower())
        return change_list  # get [b,e,a]

    def get_children(self, var):
        children = []
        for i in self.bn_network:
            if var in i[1]:
                if i[0][0] not in children and i[0][0].strip('!') not in children:
                    children.append(i[0][0])
        return children

    def get_markov_blanket(self, variable):
        given = []
        given_list=[]
        children = self.get_children(variable)
        for i in children:
            given.append(i)  # get children
            children_parent = self.gib_bn.get_parents(i)  # get children's parents
            for j in children_parent:
                given.append(j)
        parents = self.gib_bn.get_parents(variable)
        for i in parents:
            given.append(i)

        for i in given:
            if i!=variable and i!=variable.strip('!'):
                given_list.append(i)
        for idx,i in enumerate(given_list):
            for j in self.change_hidden_list:
                if i.strip('!')==j.strip('!'):
                    given_list[idx]=j
        # given_s = set(given)
        # given_list = list(given_s)  # given_list is list of variable's parents and children and children's parents
        # for:variable , given:given_list
        # print('variable:',variable,'mb of variable:',given_list)
        # print(given_list)
        result = self.gib_mybinfer.run(variable, given_list)
        return result  # type is list

    def gibbs_ask(self, N):  # e is evidence list, X is query variable,
        x = []
        true_count = 0
        false_count = 0
        self.change_hidden_list = self.get_random_value()  # Z ,lower letter. each variable has a value
        # print(self.change_hidden_list)
        for j in range(int(N)):
            tmp_change_hidden_list = self.change_hidden_list.copy()
            for idx, i in enumerate(tmp_change_hidden_list):
                # print(self.change_hidden_list)
                p = self.get_markov_blanket(i)
                true = p[0]
                false = p[1]
                value_choose = random.random()
                if i[0] != '!' and value_choose >= true:
                    self.change_hidden_list[idx] = '!' + i
                if i[0] == '!' and value_choose <= true:
                    self.change_hidden_list[idx] = i.strip('!')
            for i in self.change_hidden_list:
                if i.strip('!') == self.split_list[0][0] and i[0] != '!':
                    true_count += 1
                if i.strip('!')== self.split_list[0][0] and i[0] == '!':
                    false_count += 1
        result_list=[]
        result_list.append(true_count)
        result_list.append(false_count)
        return result_list

    def run(self):
        # N=input('please input N: ')
        # input1 = input('please input query and evidence: ')  # input: B J true M true

        N=500
        input1= 'B J true M true'
        input_list=self.gib_bn.split_list(input1)
        # X=input_list[0][0].upper()
        # evidence_list=input_list[1]
        self.split_list=input_list
        result=self.gibbs_ask(N)
        final_result=self.gib_mybinfer.normalization(result[0],result[1])
        print(final_result)

def main():
    bn = BayesianNetwork('examples/aima-alarm.xml')
    myinfer = MyBnInferencer(bn)
    gibsampler = gibbssampling(bn, myinfer)
    gibsampler.run()


main()
