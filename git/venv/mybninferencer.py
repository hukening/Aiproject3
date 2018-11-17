from bayesianNetwork import BayesianNetwork
import copy


class MyBnInferencer():
    split_list=[]


    def __init__(self, bn):
        self.bn = bn
        self.bn_network = self.bn.prob_network()


    def enumerate_ask(self, X, e, bn):
        bn_vars_tmp=self.bn.get_variable()
        bn_vars=self.bn.ordered_list(bn_vars_tmp)

        #x=X.lower()
        tmp1=e.copy()
        tmp1.append(X.lower())
        # final_bn_vars=self.bn.ordered_list(bn_vars)
        # print(str(tmp1))
        qx1=self.enumerate_all(copy.deepcopy(bn_vars),tmp1)
        tmp2=e.copy()
        tmp2.append('!'+X.lower())
        # print(str(tmp2))
        qx2=self.enumerate_all(copy.deepcopy(bn_vars),tmp2)
        Q = self.normalization(qx1,qx2)
        return Q

        # x_true=enumerate_all(bn,exi1)
        # x_false=enumerate_all(bn,exi2)
        # y: string, e: list ([string, ...])
    def get_probability(self,y,e):  # y is variable's value, e is evidence value
        given_parents_y=[]
       # bn_network = self.bn.prob_network()
        # p = -1
        p=1
        if y[0]=='!':
            y1=y.strip('!')
            parents_of_y=self.bn.get_parents(y1)
        else:
            parents_of_y=self.bn.get_parents(y)
        if len(parents_of_y)!=0:
            for i in parents_of_y:
                if i in e:
                    given_parents_y.append(i)
                if '!'+i in e:
                    given_parents_y.append('!'+i)
            for i in self.bn_network:
                if i[0][0]==y:
                    if len(given_parents_y)==0:
                        p=i[2]
                    else:
                        given_parents_y_set=set(given_parents_y)
                        i_set=set(i[1])
                        if given_parents_y_set==i_set:
                            p=i[2]
                            break
        else:
            for i in self.bn_network:
                if i[0][0]==y and len(i[1])==0:
                    p=i[2]
                    break
        # if p == -1:
        #      print('!!!', y, e)
        #  else:
        #      print('---', y, e)
        return p

    def enumerate_all(self,vars,e):

        if self.bn.is_empty(vars):
            return 1.0
        Y=vars.pop(0)
        if Y.lower() in e :
            P=self.get_probability(Y.lower(),e)
            return P*self.enumerate_all(vars,e)
        elif '!'+Y.lower() in e:
            P = self.get_probability('!'+Y.lower(), e)
            return P * self.enumerate_all(vars, e)
        else:
            e1=e.copy()
            e1.append(Y.lower())
            p1=self.get_probability(Y.lower(),e1)*self.enumerate_all(vars.copy(),e1)
            e3=e.copy()
            e3.append('!'+Y.lower())
            p2=self.get_probability('!'+Y.lower(),e3)*self.enumerate_all(vars.copy(),e3)
            p=p1+p2


            return p

    def normalization(self, true, false):
        true_rate = true / (true + false)
        false_rate = false / (true + false)

        return [true_rate, false_rate]

    def run(self,query,given):
      #  input1 = input('input:')  # input: B J True M True
      #   input1='B J true M true'
        #input1 = 'B J true M true'
        if query[0]!='!':
            input1=query.upper()+' '
        else:
            input1='!'+query.strip('!').upper()+' '
        for i in given:
            if i[0]!='!':
                input1+=i.upper()+' '+'true'+' '
            else:
                input1+= i.strip('!').upper()+' '+'false'+' '
        input_list=self.bn.split_list(input1)     #[[for_variable] , [given_list] , [hidden_list]]
        self.split_list=input_list  # get [['b'], ['j', '!m'], ['E', 'A']]
        X = self.split_list[0][0].upper()  # query variable
        bn = self.bn.prob_network()  # get prob_network {for, given, p]
        evidence_list=self.bn.get_evidence(input_list)  # get evidence list
        tmp=[]
        for i in range(1,len(evidence_list)):
            tmp.append(evidence_list[i])
        #tmp=evidence_list.pop(0) # *** get evidence list except query variable
        normalize=self.enumerate_ask(X,tmp,bn)
        return normalize



        #print (self.enumeration_ask(X))
        # for i in range(1,len(input_list)):

def main():
    bn = BayesianNetwork('examples/aima-alarm.xml')
    bnInferencer = MyBnInferencer(bn)
    #bnInferencer.run()
#main()
