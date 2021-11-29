from collections import defaultdict
import itertools
import pandas as pd
import market as tosim
from components.params import Params
from components.agent import Agent
# from gui import *
from doepy import build

# mvp - full factorial, custom intervals

param_ranges = build.full_fact(
    {'liquidity': [100.0, 500.0, 1000.0],
    'num_rounds': [200, 800, 3000]}
)

print(param_ranges)

params = list()
for i in range(len(param_ranges)):
    params.append(Params(
        outcomes=['A', 'B', 'C'],
        agents_list=[Agent(1, 'first', 1000), Agent(
            2, 'second', 1000), Agent(3, 'third', 1000)],
        mechanism='logarithmic',
        liquidity=param_ranges['liquidity'][i],
        i_shares={'A': 0.0, 'B': 0.0, 'C': 0.0},
        num_rounds=param_ranges['num_rounds'][i],
        num_iterations=1,
    ))
    results = pd.DataFrame(columns=['cost', 'probabilities'])
    data = tosim.sim(params[i])

# def run_param_exp(param_ranges):

#     output = defaultdict(dict)

#     for index, params in enumerate(itertools.product(param_ranges['loglevel'], param_ranges['mechanism'], param_ranges['num_rounds'], param_ranges['min_val'], param_ranges['max_val'], param_ranges['budget'], param_ranges['max_perms'], param_ranges['iters'], param_ranges['seed'], param_ranges['agent_names'])):
#         ParamsIn = Params(*params)
#         print("keys", param_ranges.keys())
#         test_dict = {list(param_ranges.keys())[
#             i]: params[i] for i in range(len(params))}
#         print("TEST", test_dict)
#         output[index] = {'Parameters': test_dict,
#                          'Results': tosim.sim(ParamsIn)}
#         print("OUTPUT", output)

#     import json
#     outputf = json.dumps(output, sort_keys=True, indent=2)
#     print(outputf)

#     with open('Output.txt', 'w') as outfile:
#         outfile.write(outputf)


# run_param_exp(test_param_ranges)
