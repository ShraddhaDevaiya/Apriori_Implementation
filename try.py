#this is using apriori
import pandas as pd
import numpy as np
import ast
from mlxtend.frequent_patterns import apriori

with open("database/DB1K.txt", 'r') as f:
    lines = f.readlines()
    result = [line.strip() for line in lines]
    s_data= []

for s in result:
    l = ast.literal_eval(s)
    s_data.append(l)

print("len LI DB: ",len(s_data))
df = pd.DataFrame(s_data)
df = pd.get_dummies(df.apply(pd.Series).stack()).sum(level=0)

li_frequent_itemsets = apriori(df, min_support=0.05, use_colnames=True)
#print("LEN: ", len(li_frequent_itemsets['itemsets']))
print("LEN: ", len(li_frequent_itemsets))
print("LI_SET: ", sorted(set(li_frequent_itemsets['itemsets'])))
