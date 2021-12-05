import simpy
import random
import statistics
from collections import defaultdict
import logging
import csv
import math
import numpy as np


# parameters = defaultdict()
# outcomes = []
total_shares = defaultdict(list)
# total_payments = defaultdict(list)
total_costs = []
# total_probabilities = defaultdict(list)
# revenue = 0
# utilities = []

# ag_total_payments = []
# ag_total_probabilities = []
# ag_total_costs = []
# ag_revenue = []
# ag_utilities = []

def IncrementRound(purchased_shares, shares, round):
    round += 1
    for outcome in outcomes:
        shares[outcome] += purchased_shares[outcome]
    return shares

def Cost(shares, liquidity):
    cost = liquidity * \
        math.log(sum([math.exp(shares[outcome] / liquidity)
                 for outcome in outcomes]))
    return cost

def Probabilities(shares, liquidity):
    probabilities = {outcome: math.exp(shares[outcome] / liquidity) / sum(
        [math.exp(shares[outcome] / liquidity) for outcome in outcomes]) for outcome in outcomes}
    return probabilities


# initiate parameters
outcomes = ["A", "B", "C"]
shares = {"A": 0, "B": 0, "C": 0}

# number of shares for each outcome { outcome : shares, ... }

def simulation(liquidity, rounds):
    # demo
    for round_num in rounds:
        # randomly instantiate ps
        ps = {outcome: random.randint(1, 50) for outcome in outcomes}

        # increment round via updating shares
        IncrementRound(ps, shares, round_num)
        
        # calculate and update cost list
        cost = Cost(shares, liquidity)
        probability = Probabilities(shares, liquidity)["A"]
        
        print(round_num, cost, probability)
        
    return round_num, cost, probability
        
        # total_costs.append(Cost(shares, liquidity))
        
        # for outcome in outcomes:
        #     # update shares dictionary
        #     total_shares[outcome].append(shares[outcome])
        
# simulation(100, 100)