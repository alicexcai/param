from collections import defaultdict
import math
import random
import pandas as pd

from components.history import History
from components.stats import Stats
from components.params import Params
from components.agent import Agent

# create table database -> sqlite
# params_const = pd.DataFrame(columns=['outcomes', 'mechanism', 'agents_list', 'i_shares'])
# params_tested = pd.DataFrame(columns=['liquidity', 'num_rounds'])
# results_primary = pd.DataFrame(columns=['cost', 'probabilities', 'shares']) # ommitted 'p_shares', 'payments' as nonprimary

# full_data = pd.DataFrame.join(params_const, params_tested, results_primary, how='outer') # should be equivelant to how='inner', by index
# print(full_data)

test_params = Params(
    outcomes=['A', 'B', 'C'],
    agents_list=[Agent(1, 'first', 1000), Agent(2, 'second', 1000), Agent(3, 'third', 1000)],
    mechanism='logarithmic',
    liquidity=100.0,
    i_shares={'A': 0.0, 'B': 0.0, 'C': 0.0},

    num_rounds=100,
    num_iterations=1,
)

def sim(params):
    
    # initiate
    round_num = 0
    
    # single set of parameters, per round
    full_results = pd.DataFrame(columns=['round_num', 'cost', 'probabilities', 'shares', 'p_shares', 'payments'])
    full_results['round_num'] = range(params.num_rounds+1)
    # round_num = full_results['round_num']
    # round_num[0] = 0

    outcomes = params.outcomes
    mechanism = params.mechanism
    liquidity = params.liquidity
    num_rounds = params.num_rounds
    
    # variable
    agents_list = params.agents_list
    
    # shares = defaultdict(dict)
    # shares[0] = params.i_shares
    # full_results.loc[0, 'shares'] = [params.i_shares]
    shares = full_results['shares']
    shares[0] = params.i_shares
    
    # payments = defaultdict(dict)
    # p_shares = defaultdict(dict)
    # payments[0] = {agent.id: {outcome: 0.0 for outcome in outcomes} for agent in agents_list}
    # p_shares[0] = {agent.id: {outcome: 0.0 for outcome in outcomes} for agent in agents_list}
    payments = full_results['payments']
    payments[0] = {agent.id: {outcome: 0.0 for outcome in outcomes} for agent in agents_list}
    p_shares = full_results['p_shares'] 
    p_shares[0] = {agent.id: {outcome: 0.0 for outcome in outcomes} for agent in agents_list}
    
    def Cost(shares):
        if mechanism == 'logarithmic':
            cost = liquidity * math.log(sum([math.exp(shares[outcome] / liquidity) for outcome in outcomes]))
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
        new_shares = {outcome: shares[outcome] + requested_purchase[outcome] for outcome in outcomes}
        after_cost = Cost(new_shares)
        cost_of_trans = after_cost - before_cost
        return cost_of_trans

    # probabilities = defaultdict(dict)
    # cost = defaultdict()
    # probabilities[0] = {outcome: Probabilities(shares[0]) for outcome in outcomes}
    # cost[0] = Cost(shares[0])
    probabilities = full_results['probabilities']
    probabilities[0] = Probabilities(shares[0])
    cost = full_results['cost']
    cost[0] = Cost(shares[0])

    # Introduce new agent mid-simulation - is this necessary?
    def init_agent(agents_list, newagent_name, newagent_balance):
        agents_list.update(
            Agent(len(agents_list)+1, newagent_name, newagent_balance))

    history = History(cost, shares, probabilities, p_shares, payments)

    # round is an arbitrary alias for a unit of time, agents can choose to trade in different round intervals, simulating trade frequency
    def run_round(shares, round_num):
        
        # # add round index to results
        # full_results.loc[round_num, 'round'] = round_num
        print("\n\n========\n\n", round_num, "\n\n========\n\n")
       
        # example signal
        signal = { outcome : random.random() for outcome in outcomes }
        print('SIGNAL', signal)
        
        # p_shares[round_num]= defaultdict(dict)
        # payments[round_num]= defaultdict(dict)
        p_shares[round_num]= {}
        payments[round_num]= {}
        
        # Log purchased shares determined by agents
        
        for agent in agents_list:
            requested_purchase = agent.purchase(mechanism, liquidity, outcomes, history, round_num, shares, signal)
            # p_shares[round_num][agent.id].append(requested_purchase if sum(requested_purchase.values()) <= agent.balance else {outcome: 0 for outcome in outcomes})
            p_shares[round_num][agent.id] = requested_purchase if sum(requested_purchase.values()) <= agent.balance else {outcome: 0 for outcome in outcomes}
            # p_shares[round_num].update({ agent.id : requested_purchase if sum(requested_purchase.values()) <= agent.balance else {outcome: 0 for outcome in outcomes})
            # update agent balance, calculate payments based on mechanism
            
            # payments[round_num][agent.id].append(CostOfTrans(shares[round_num-1], p_shares[round_num][agent.id]))
            cost_of_trans_dict = {}
            for outcome in outcomes:
                separated_shares = {out: 0.0 for out in outcomes}
                separated_shares[outcome] = shares[round_num-1][outcome]
                cost_of_trans_dict[outcome] = CostOfTrans(separated_shares, p_shares[round_num][agent.id])
            # print("\n\n===============\n\n", cost_of_trans_dict, "\n\n=============\n\n")
            
            payments[round_num][agent.id] = cost_of_trans_dict
            # print("\n\n===============\n\n", sum(list(payments[round_num][agent.id].values())), "\n\n===============\n\n")
            agent.balance -= sum(list(payments[round_num][agent.id].values()))
            shares[round_num] = { outcome: shares[round_num-1][outcome] + p_shares[round_num][agent.id][outcome] for outcome in outcomes }
        # new cost and probabilities post-purchase
        cost[round_num] = Cost(shares[round_num])
        probabilities[round_num] = Probabilities(shares[round_num])
        
        # for agent in agents_dict:
        #     requested_purchase = agent.purchase(mechanism, liquidity, outcomes, history, round_num, shares, signal)
        #     p_shares[round_num][agent.id] = requested_purchase if sum(requested_purchase.values()) <= agent.balance else {outcome: 0 for outcome in outcomes}
        #     # update agent balance, calculate payments based on mechanism
        #     payments[round_num][agent.id] = CostOfTrans(shares[round_num-1], p_shares[round_num][agent.id])
        #     agent.balance -= payments[round_num][agent.id]
        #     shares[round_num] = { outcome: shares[round_num-1][outcome] + p_shares[round_num][agent.id][outcome] for outcome in outcomes }
        # # new cost and probabilities post-purchase
        # cost[round_num] = Cost(shares[round_num])
        # probabilities[round_num] = Probabilities(shares[round_num])

        '''
        Introduce round-specific actions here:
        
        e.g. introduce new agents at certain rounds:
        if round_num == 10:
            init_agent(agents_list, agent)
            
        e.g. add balance to agents at certain rounds:
        if round_num == 10:
            for agent in agents_list:
                agents_list[agent].balance += 1000
        '''
        
        print("\n\t=== Round %d ===" % round_num)
        print("\tPurchased shares: %s" % p_shares[round_num])
        print("\tUpdated shares: %s" % shares[round_num])
        print("\tPayments made: %s" % payments[round_num])
        print("\tUpdated probabilities: %s" % probabilities[round_num])
        print("\tUpdated cost: %s\n" % cost[round_num])

    # RUN ROUNDS
    for round_num in range(1, params.num_rounds + 1):
        # Consider using 240 rounds to simulate a 4 hour game with trading every 1 sec?
        run_round(shares, round_num)

    print("\n\t=== Cumulative (%d Rounds) ===" % num_rounds)
    print("\tPurchased Shares History: %s" % p_shares)
    print("\tShares History: %s" % shares)
    print("\tPayments History: %s" % payments)
    print("\tProbabilities History: %s" % probabilities)
    print("\tCost History: %s\n" % cost)
    
    # print(history.get_data(cost, shares, probabilities, p_shares, payments))
    print("\n\nROUND NUM\n\n", full_results['round_num'], "\n\n============\n\n")
    print("\n\nCOST\n\n", full_results['cost'], "\n\n============\n\n")
    print("\n\nPROBABILITIES\n\n", full_results['probabilities'], "\n\n============\n\n")
    print("\n\nSHARES\n\n", full_results['shares'], "\n\n============\n\n")
    print("\n\nPSHARES\n\n", full_results['p_shares'], "\n\n============\n\n")
    print("\n\nPAYMENTS\n\n", full_results['payments'], "\n\n============\n\n")
    full_results.to_csv('improved.csv')  
    # print(full_results.columns.values)
    return history
# params = Params()

sim(test_params)