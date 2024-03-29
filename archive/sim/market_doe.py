import h5py
from pypet import Environment
from collections import defaultdict
import math
import random

from components.history import History
from components.stats import Stats
from components.params import Params
from components.agent import Agent


def sim(config, config_constant):

    outcomes = config_constant.outcomes
    mechanism = config.mechanism
    liquidity = config.liquidity
    num_rounds = config.num_rounds

    # variable
    agents_dict = config_constant.agents_dict
    shares = defaultdict(dict)
    shares[0] = config_constant.i_shares
    payments = defaultdict(dict)
    p_shares = defaultdict(dict)
    payments[0] = {agent.id: {outcome: 0.0 for outcome in outcomes}
                   for agent in agents_dict}
    p_shares[0] = {agent.id: {outcome: 0.0 for outcome in outcomes}
                   for agent in agents_dict}
    

    def Cost(shares):
        if mechanism == 'logarithmic':
            cost = liquidity * \
                math.log(sum([math.exp(shares[outcome] / liquidity)
                         for outcome in outcomes]))
        elif mechanism == 'quadratic':
            # is this correct?
            cost = liquidity * \
                sum([(shares[outcome] / liquidity) ** 2 for outcome in outcomes])
        return cost

    def Probabilities(shares):

        if mechanism == 'logarithmic':
            probabilities = {outcome: math.exp(shares[outcome] / liquidity) / sum(
                [math.exp(shares[outcome] / liquidity) for outcome in outcomes]) for outcome in outcomes}
        elif mechanism == 'quadratic':
            # is this correct?
            probabilities = {outcome: (shares[outcome] / liquidity) ** 2 / sum(
                [(shares[outcome] / liquidity) ** 2 for outcome in outcomes]) for outcome in outcomes}
        return probabilities

    def CostOfTrans(shares, requested_purchase):
        before_cost = Cost(shares)
        new_shares = {
            outcome: shares[outcome] + requested_purchase[outcome] for outcome in outcomes}
        after_cost = Cost(new_shares)
        cost_of_trans = after_cost - before_cost
        return cost_of_trans

    probabilities = defaultdict(dict)
    cost = defaultdict()
    probabilities[0] = {outcome: Probabilities(
        shares[0]) for outcome in outcomes}
    cost[0] = Cost(shares[0])

    # Introduce new agent mid-simulation - is this necessary?
    def init_agent(agents_dict, newagent_name, newagent_balance):
        agents_dict.update(
            Agent(len(agents_dict)+1, newagent_name, newagent_balance))

    history = History(cost, shares, probabilities, p_shares, payments)

    # round is an arbitrary alias for a unit of time, agents can choose to trade in different round intervals, simulating trade frequency
    def run_round(shares, round_num):

        # example signal
        signal = {outcome: random.random() for outcome in outcomes}
        print('SIGNAL', signal)

        # Log purchased shares determined by agents
        for agent in agents_dict:
            requested_purchase = agent.purchase(
                mechanism, liquidity, outcomes, history, round_num, shares, signal)
            p_shares[round_num][agent.id] = requested_purchase if sum(
                requested_purchase.values()) <= agent.balance else {outcome: 0 for outcome in outcomes}
            # update agent balance, calculate payments based on mechanism
            payments[round_num][agent.id] = CostOfTrans(
                shares[round_num-1], p_shares[round_num][agent.id])
            agent.balance -= payments[round_num][agent.id]
            shares[round_num] = {outcome: shares[round_num-1][outcome] +
                                 p_shares[round_num][agent.id][outcome] for outcome in outcomes}
        # new cost and probabilities post-purchase
        cost[round_num] = Cost(shares[round_num])
        probabilities[round_num] = Probabilities(shares[round_num])

        '''
        Introduce round-specific actions here:
        
        e.g. introduce new agents at certain rounds:
        if round_num == 10:
            init_agent(agents_dict, agent)
            
        e.g. add balance to agents at certain rounds:
        if round_num == 10:
            for agent in agents_dict:
                agents_dict[agent].balance += 1000
        '''

        print("\n\t=== Round %d ===" % round_num)
        print("\tPurchased shares: %s" % p_shares[round_num])
        print("\tUpdated shares: %s" % shares[round_num])
        print("\tPayments made: %s" % payments[round_num])
        print("\tUpdated probabilities: %s" % probabilities[round_num])
        print("\tUpdated cost: %s\n" % cost[round_num])

    # RUN ROUNDS
    for round_num in range(1, config.num_rounds + 1):
        # Consider using 240 rounds to simulate a 4 hour game with trading every 1 sec?
        run_round(shares, round_num)

    print("\n\t=== Cumulative (%d Rounds) ===" % num_rounds)
    print("\tPurchased Shares History: %s" % p_shares)
    print("\tShares History: %s" % shares)
    print("\tPayments History: %s" % payments)
    print("\tProbabilities History: %s" % probabilities)
    print("\tCost History: %s\n" % cost)
    
    # config.f_add_result('shares', p_shares)
    # config.f_add_result('probabilities', probabilities)
    config.f_add_result('cost', list(cost.values()))
    # return cost[num_rounds-1]
    # return {'Shares History': p_shares, 'Probabilities History': probabilities, 'Cost History': cost}


h5py.Dataset.__doc__ = ''

# config = Params(
#     outcomes=['A', 'B', 'C'],
#     agents_dict={Agent(1, 'first', 1000), Agent(2, 'second', 1000), Agent(3, 'third', 1000), Agent(4, 'fourth', 1000), Agent(5, 'fifth', 1000)},
#     mechanism='logarithmic',
#     liquidity=100.0,
#     i_shares={'A': 0.0, 'B': 0.0, 'C': 0.0},
#     num_rounds=100,
# )

class Config:
    
    def __init__(self,
                 outcomes=['Y', 'N'],
                 agents_dict={Agent(1, 'first', 1000)},
                 i_shares={0: {'Y': 0.0, 'N': 0.0}},
                 ):
        self.outcomes = outcomes
        self.agents_dict = agents_dict
        self.i_shares = i_shares


config_constant = Config(
    outcomes=['A', 'B', 'C'],
    agents_dict={Agent(1, 'first', 1000), Agent(2, 'second', 1000), Agent(3, 'third', 1000)},
    i_shares={'A': 0.0, 'B': 0.0, 'C': 0.0})

env = Environment()
config = env.traj
config.f_add_parameter('liquidity', 100, comment='1st dim')
config.f_add_parameter('num_rounds', 100, comment='2nd dim')
# config.f_add_parameter('outcomes', ['A', 'B', 'C'], comment='3rd dim')
# config.f_add_parameter('budgets', [1000, 1000], comment='4th dim')
config.f_add_parameter('mechanism', 'logarithmic', comment='6th dim')
config.f_explore(
    dict(liquidity=[100, 200, 300, 400], num_rounds=[100, 500, 1000, 5000]))


env.run(sim(config, config_constant))
config.f_load(load_data=2)

