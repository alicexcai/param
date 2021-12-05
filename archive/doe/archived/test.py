from doepy import build
import pandas as pd

build = build.full_fact(
{'Pressure':[40,55,70],
'Flow rate':[0.2,0.4],
'Time':[5,11]},
)

# print(build, len(build))
# print(build['Pressure'])

for i in range(len(build)):
    # print(build[pd.DataFrame(build[i])])
    # print(build['Pressure'].iloc[[i]])
    # print(i)
    
    build.loc[i, 'Pressure'] = [{'pleeeez': 'work'}]
    
    # build.ix[i, 'Pressure'] = 'hi'
    # print(build)
    # build['Pressure'][i] = 'bye'
    # print(build)
print(build)

hi = build['Pressure']
hi[0] = {'a': 0, 'b': 1, 'c': 2}
print(hi)
print(hi[0]['b'])