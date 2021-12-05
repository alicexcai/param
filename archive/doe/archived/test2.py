from doepy import build

params_tested = build.full_fact(
    {'liquidity': [100.0, 500.0, 1000.0],
    'num_rounds': [200, 800, 3000]}
)
params_const = {
    'outcomes': {'A': 0.0, 'B': 0.0, 'C': 0.0},
    'mechanism': 'logarithmic',
    'i_shares': {'A': 0.0, 'B': 0.0, 'C': 0.0},
                }
print(params_tested)


class TestClass:
    def __init__(self, params_const, params_tested):
        for param in params_const:
            self.__dict__[param] = params_const[param]
        for param in params_tested:
            self.__dict__[param] = params_tested[param][i]

    def __setattr__(self, name, value):
        raise Exception("It is read only!")
    
test_class = TestClass(params_const, params_tested)
print(test_class.__dict__)