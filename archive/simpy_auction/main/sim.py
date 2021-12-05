from collections import defaultdict
import itertools
import pandas as pd
import auction as tosim
from gui import *

runGUI()

def runParamExplore():
    
    output = defaultdict(dict)

    for index, params in enumerate(itertools.product(param_ranges['loglevel'], param_ranges['mechanism'], param_ranges['num_rounds'], param_ranges['min_val'], param_ranges['max_val'], param_ranges['budget'], param_ranges['reserve'], param_ranges['max_perms'], param_ranges['iters'], param_ranges['seed'], param_ranges['agent_class_names'])):
        ParamsIn = Params(*params)
        print("keys", param_ranges.keys())
        test_dict = {list(param_ranges.keys())[i] : params[i] for i in range(len(params))}
        print("TEST", test_dict)
        output[index] = {'Parameters': test_dict, 'Results': tosim.main(ParamsIn)}
        print("OUTPUT", output)

    import json
    outputf = json.dumps(output, sort_keys=True, indent=2)
    print(outputf)

    with open('Output.txt', 'w') as outfile:
        outfile.write(outputf)
