from collections import defaultdict
import math
import random
import pandas as pd

from components.history import History
from components.stats import Stats
from components.params import MetaParams, Params
from components.agent import Agent

def sim(params, meta_params):
    
    # initiate
    round_num = 0
    # single set of parameters, per round
    results_full = pd.DataFrame(columns=meta_params.results_full)
    results_full['round_num'] = range(int(params.num_rounds)+1) # Is this necessary? Just use index?

    outcomes = params.outcomes
    mechanism = params.mechanism 
    liquidity = params.liquidity
    num_rounds = params.num_rounds
    
    # variable
    agents_list = params.agents_list
    shares = results_full['shares']
    shares[0] = params.i_shares 
    payments = results_full['payments']
    payments[0] = {agent.id: {outcome: 0.0 for outcome in outcomes} for agent in agents_list}
    p_shares = results_full['p_shares'] 
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

    probabilities = results_full['probabilities']
    probabilities[0] = Probabilities(shares[0])
    cost = results_full['cost']
    cost[0] = Cost(shares[0])

    # Introduce new agent mid-simulation - is this necessary?
    def init_agent(agents_list, newagent_name, newagent_balance):
        agents_list.update(
            Agent(len(agents_list)+1, newagent_name, newagent_balance))

    history = History(cost, shares, probabilities, p_shares, payments)

    # round is an arbitrary alias for a unit of time, agents can choose to trade in different round intervals, simulating trade frequency
    def run_round(shares, round_num):
        
       
        # example signal
        signal = { outcome : random.random() for outcome in outcomes }
        # print('SIGNAL', signal)

        p_shares[round_num]= {}
        payments[round_num]= {}
        
        # Log purchased shares determined by agents
        for agent in agents_list:
            requested_purchase = agent.purchase(mechanism, liquidity, outcomes, history, round_num, shares, signal)
            p_shares[round_num][agent.id] = requested_purchase if sum(requested_purchase.values()) <= agent.balance else {outcome: 0 for outcome in outcomes}
            # update agent balance, calculate payments based on mechanism
            
            cost_of_trans_dict = {}
            for outcome in outcomes:
                separated_shares = {out: 0.0 for out in outcomes}
                separated_shares[outcome] = shares[round_num-1][outcome]
                cost_of_trans_dict[outcome] = CostOfTrans(separated_shares, p_shares[round_num][agent.id])
            
            payments[round_num][agent.id] = cost_of_trans_dict
            agent.balance -= sum(list(payments[round_num][agent.id].values()))
            shares[round_num] = { outcome: shares[round_num-1][outcome] + p_shares[round_num][agent.id][outcome] for outcome in outcomes }
        # new cost and probabilities post-purchase
        cost[round_num] = Cost(shares[round_num])
        probabilities[round_num] = Probabilities(shares[round_num])

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
        
        # print("\n\t=== Round %d ===" % round_num)
        # print("\tPurchased shares: %s" % p_shares[round_num])
        # print("\tUpdated shares: %s" % shares[round_num])
        # print("\tPayments made: %s" % payments[round_num])
        # print("\tUpdated probabilities: %s" % probabilities[round_num])
        # print("\tUpdated cost: %s\n" % cost[round_num])

    # RUN ROUNDS
    for round_num in range(1, int(params.num_rounds) + 1):
        # Consider using 240 rounds to simulate a 4 hour game with trading every 1 sec?
        # print("\nInitiating round %d"%round_num)
        run_round(shares, round_num)

    # print("\n\t=== Cumulative (%d Rounds) ===" % num_rounds)
    # print("\tPurchased Shares History: %s" % p_shares)
    # print("\tShares History: %s" % shares)
    # print("\tPayments History: %s" % payments)
    # print("\tProbabilities History: %s" % probabilities)
    # print("\tCost History: %s\n" % cost)
    
    # UNPACKING DATATYPES =====================================================================================================================
    
    results_full_unpkd = results_full.copy()
    
    # results_primary_unpkd = results_full_unpkd[meta_params.results_primary]
    
    shares_unpkd = results_full_unpkd["shares"].apply(pd.Series)
    shares_unpkd = shares_unpkd.add_prefix('shares_')
    results_full_unpkd = pd.concat([results_full_unpkd.drop('shares', axis=1), shares_unpkd], axis=1)  
    
    probabilities_unpkd = results_full_unpkd["probabilities"].apply(pd.Series)
    probabilities_unpkd = probabilities_unpkd.add_prefix('probability_')
    results_full_unpkd = pd.concat([results_full_unpkd.drop('probabilities', axis=1), probabilities_unpkd], axis=1)
    
    # results_primary_unpkd = pd.concat([results_primary_unpkd.drop('shares', axis=1), shares_unpkd], axis=1)  
    # results_primary_unpkd = pd.concat([results_primary_unpkd.drop('probabilities', axis=1), probabilities_unpkd], axis=1)
    
    pshares_unpkd = results_full_unpkd["p_shares"].apply(pd.Series)
    pshares_unpkd = pshares_unpkd.add_prefix('purchase_agent')

    pshares_unpkd_unpkd = pshares_unpkd.copy()
    for col in pshares_unpkd.columns.values:
        newcol = pshares_unpkd[col].apply(pd.Series)
        newcol = newcol.add_prefix('%s_outcome'%col)
        pshares_unpkd_unpkd = pd.concat([pshares_unpkd_unpkd, newcol], axis=1)
    pshares_unpkd_unpkd = pshares_unpkd_unpkd.drop(pshares_unpkd.columns.values, axis=1)
    
    results_full_unpkd = pd.concat([results_full_unpkd.drop('p_shares', axis=1), pshares_unpkd_unpkd], axis=1)

    payments_unpkd = results_full_unpkd["payments"].apply(pd.Series)
    payments_unpkd = payments_unpkd.add_prefix('payment_agent')

    payments_unpkd_unpkd = payments_unpkd.copy()
    for col in payments_unpkd.columns.values:
        newcol = payments_unpkd[col].apply(pd.Series)
        newcol = newcol.add_prefix('%s_outcome'%col)
        payments_unpkd_unpkd = pd.concat([payments_unpkd_unpkd, newcol], axis=1)
    payments_unpkd_unpkd = payments_unpkd_unpkd.drop(payments_unpkd.columns.values, axis=1)
    
    results_full_unpkd = pd.concat([results_full_unpkd.drop('payments', axis=1), payments_unpkd_unpkd], axis=1)
    
    results_primary = results_full_unpkd.iloc[-1][meta_params.results_primary]
    
    # ==========================================================================================================================================
    
    return results_full_unpkd, results_primary


# # TEST

# meta_params = MetaParams(
#     params_tested=['liquidity', 'num_rounds'],
#     params_const=['outcomes', 'agents_list', 'mechanism', 'i_shares'],
#     results_primary=['cost', 'probabilities', 'shares'],
#     results_full=['cost', 'probabilities', 'shares', 'p_shares', 'payments']
# )
            
# params = Params({
#     'liquidity': 100.0,
#     'num_rounds': 200.0,
#     'outcomes': ['A', 'B', 'C'],
#     'agents_list': [Agent(1, 'first', 10000), Agent(2, 'second', 10000), Agent(3, 'third', 10000)],
#     'mechanism': 'logarithmic',
#     'i_shares': {'A': 0.0, 'B': 0.0, 'C': 0.0},
#     })

# results_full, results_primary = sim(params, meta_params)

# print(results_full, "\n\n=================\n\n", results_primary)
# print(results_full.dtypes, "\n\n=================\n\n", results_primary.dtypes)