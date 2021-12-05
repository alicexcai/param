import pandas as pd

df = pd.DataFrame({"A":[{1: {'A': 1, 'B': 2, 'C': 3}, 2: {'A': 4, 'B': 5, 'C': 6}, 3: {'A': 7, 'B': 8, 'C': 9}}, 
                        {1: {'A': 0, 'B': 0, 'C': 0}, 2: {'A': 0, 'B': 0, 'C': 0}, 3: {'A': 0, 'B': 0, 'C': 0}}], "B":[10, 10]})
# print(df)

new = df["A"].apply(pd.Series)
new = new.add_prefix('purchase_agent')

newnew = new.copy()
for col in new.columns.values:
    newin = new[col].apply(pd.Series)
    newin = newin.add_prefix('%s_'%col)
    newnew = pd.concat([newnew, newin], axis=1)
newnew = newnew.drop(new.columns.values, axis=1)
print("=======",newnew)

final = pd.concat([df.drop('A', axis=1), newnew], axis=1)
print(final)

# ok = df.replace({'A' : {'B' : 1, 'C':2}})


# bye = pd.DataFrame({'a':[1, 2, 3]})

# ok = bye.replace({ 'Medium' : [0, 0, 0], 'Small' : [1, 1, 1], 'High' : [2, 2, 2] })

# df.replace({'A' : {col : new[col] for col in new.columns.values}})

# print(newnew)