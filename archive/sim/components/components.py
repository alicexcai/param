import sympy
from sympy.abc import x
import math


class Agent:

    def __init__(self, id, name, balance):
        self.id = id
        self.name = name  # alias
        self.balance = balance
        self.type = 'default'
        
        # agent-centric history
    def get_history(self, history):
        # agent purchase history stored in a dictionary of dictionaries { round : { outcome : shares, ... }, ... } for each agent
        agent_history = { round : history.p_shares[self.id] for round in history.rounds }
        return agent_history

    def purchase(self, mechanism, liquidity, outcomes, history, round_num, shares, signal):
        
        # signal = {'outcome': 'probability', ... }, derived from change in information * weight
        # code for purchase strategy
        
        
        
        # def Probabilities(shares):
    
        #     if mechanism == 'logarithmic':
        #         probabilities = {outcome: math.exp(shares[round_num][outcome] / liquidity) / sum(
        #             [math.exp(shares[round_num][outcome] / liquidity) for outcome in outcomes]) for outcome in outcomes}
        #     elif mechanism == 'quadratic':
        #         # is this correct?
        #         probabilities = {outcome: (shares[round_num][outcome] / liquidity) ** 2 / sum(
        #             [(shares[round_num][outcome] / liquidity) ** 2 for outcome in outcomes]) for outcome in outcomes}
        #     return probabilities
        
        # target_shares = sympy.solve(Probabilities(x) - signal, 'x')
        
        # purchase = { outcome : target_shares[round_num][outcome] - shares[round_num][outcome] for outcome in shares[round_num].keys() }
        
        
        
        
        # purchase = {}
        # for outcome in shares[round_num].keys():
        #     purchase[outcome] = target_shares[round_num][outcome] - shares[round_num][outcome]
        
        purchase = signal
        
        return purchase
    
    # Is this necessary?
    def __repr__(self):
        return "%s(id = %d, name = %d, balance = %d)" % (
            self.__class__.__name__, self.id, self.name, self.balance)


class Params:

    def __init__(self,
                 outcomes=['Y', 'N'],
                 agents_dict={Agent(1, 'first', 1000)},
                 mechanism='logarithmic',
                 liquidity=100.0,
                 i_shares={0: {'Y': 0.0, 'N': 0.0}},

                 num_rounds=100,
                 loglevel='info',
                 num_iterations=1,
                 ):
        self.outcomes = outcomes
        self.agents_dict = agents_dict
        self.mechanism = mechanism
        self.liquidity = liquidity
        self.i_shares = i_shares
        self.num_rounds = num_rounds
        self.loglevel = loglevel
        self.num_iterations = num_iterations