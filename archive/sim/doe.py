from collections import defaultdict
import itertools
import pandas as pd
import market as tosim
from .components.params import Params
from .components.agent import Agent
# from gui import *

test_param_ranges = {
    'loglevel': ['info'], # ['info', 'debug']
    'mechanism': ['vcg'], # ['vcg', 'gsp', 'switch']
    'num_rounds': [3], # int
    'min_val': [25], # int
    'max_val': [175],
    'budget': [500000], # int
    'max_perms': [10],# int
    'iters': [1], # int
    'seed': [1, 2], # int
    'agent_names': [['Truthful', 'Truthful', 'Truthful']] # Truthful, NANewbb
}

config = Params(
    outcomes=['A', 'B', 'C'],
    # agents_dict={1: {'name': 'default', 'type': 'default', 'balance': 1000}, 2: {'name': 'default2',
    #                                                                              'type': 'default', 'balance': 1000}, 3: {'name': 'default3', 'type': 'default', 'balance': 1000}},
    agents_dict={Agent(1, 'first', 1000), Agent(2, 'second', 1000), Agent(3, 'third', 1000), Agent(4, 'fourth', 1000), Agent(5, 'fifth', 1000)},
    mechanism='logarithmic',
    liquidity=100.0,
    i_shares={'A': 0.0, 'B': 0.0, 'C': 0.0},

    num_rounds=100,
    loglevel='info',
    num_iterations=1,
)

def run_param_exp(param_ranges):
    
    output = defaultdict(dict)

    for index, params in enumerate(itertools.product(param_ranges['loglevel'], param_ranges['mechanism'], param_ranges['num_rounds'], param_ranges['min_val'], param_ranges['max_val'], param_ranges['budget'], param_ranges['max_perms'], param_ranges['iters'], param_ranges['seed'], param_ranges['agent_names'])):
        ParamsIn = Params(*params)
        print("keys", param_ranges.keys())
        test_dict = {list(param_ranges.keys())[i] : params[i] for i in range(len(params))}
        print("TEST", test_dict)
        output[index] = {'Parameters': test_dict, 'Results': tosim.sim(ParamsIn)}
        print("OUTPUT", output)

    import json
    outputf = json.dumps(output, sort_keys=True, indent=2)
    print(outputf)

    with open('Output.txt', 'w') as outfile:
        outfile.write(outputf)
        
run_param_exp(test_param_ranges)