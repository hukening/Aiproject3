from bayesianNetwork import BayesianNetwork as BN

class MyBnApproxInferencer:
    def __init__(self, file, query, observation):
        self.bn = BN(file).prob_network()
        self.query = query
        self.observation = observation

    #prior_sample returns an event sampled from the prior specified by bn
    def prior_sample(self, bn): #bn, a Bayesian network specifying joint distribution P(X1, . . . , Xn)

        return []

    def rejection_sampling(self, X, e, bn, num_sample):
        N = []
        return normalize(N)

    def normalize(self, N):

        return 0.0
