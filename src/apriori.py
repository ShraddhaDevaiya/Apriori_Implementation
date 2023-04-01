import pandas as pd
import numpy as np
import sys
import random
import math
import time
import json
import os
import ast

if __name__ == '__main__':
    db_name = sys.argv[1]
    ms = sys.argv[2]

def save_apriori_outputs(freq_items, Filename,ms):
  # Create the "output" folder if it doesn't exist
  if not os.path.exists("output"):
    os.mkdir("output")
  # Create the file inside the "output" folder
  filename = os.path.join("output", Filename)

  with open(filename, "w") as fp:
      fp.write("Min Support - %s\n" % ms)
      fp.write("Frequent Item - %s\n" % freq_items)


def sam_apriori(database, min_support):
    with open(database, 'r') as f:
        lines = f.readlines()
        result = [line.strip() for line in lines]
        data= []

    for s in result:
        l = ast.literal_eval(s)
        data.append(l)
    print("APRIORI LEN DB: ", len(data))
    unique_items = set()
    for row in data:
        for item in row:
            unique_items.add(item)
    # print("unique_items : ", unique_items)

    # create a binary matrix
    binary_matrix = []
    for row in data:
        binary_row = []
        for item in unique_items:
            if item in row:
                binary_row.append(1)
            else:
                binary_row.append(0)
        binary_matrix.append(binary_row)
    # print("binary_matrix : ", binary_matrix)

    # create a DataFrame
    df = pd.DataFrame(binary_matrix, columns=unique_items)
    # print(df)
    final_frequent_itemsets = []
    # find frequent itemsets
    frequent_itemsets = []

    for item in df.columns:
        support = df[item].sum() / len(df)
        # print("support: ", type(support))
        if str(support) >= min_support:
            # print(support)
            frequent_itemsets.append(frozenset([item]))
            final_frequent_itemsets.append(frozenset([item]))
    k = 2

    while len(frequent_itemsets) > 0:
        candidate_itemsets = set()
        for i, itemset1 in enumerate(frequent_itemsets):
            for j, itemset2 in enumerate(frequent_itemsets):
                if i < j and len(itemset1.union(itemset2)) == k:
                    candidate_itemsets.add(itemset1.union(itemset2))
        # print(k,"_for_itemset")
        # print("candidate_itemsets : ", candidate_itemsets)
        frequent_itemsets = []
        for itemset in candidate_itemsets:
            # print(candidate_itemsets)
            support = (df[list(itemset)].sum(axis=1) == len(itemset)).sum() / len(df)
            if str(support) >= min_support:
                # print(itemset)
                final_frequent_itemsets.append(itemset)
                frequent_itemsets.append(itemset)
        # print(k,"_itemset")
        # print(k, "final_frequent_itemsets : ", final_frequent_itemsets)
        k += 1

    # print frequent itemsets
    # for itemset in final_frequent_itemsets:
    #     support = (df[list(itemset)].sum(axis=1) == len(itemset)).sum() / len(df)
    #     print(itemset, support)
    return final_frequent_itemsets


def read_db_from_txtFile(file_name):
  # example for filename: "db1K.txt"
  # By default address is "../dbs/"
  # return bd_list which later will be passed to remove_i_from_DB function
  # open the text file in read mode
  filename = os.path.join("database", str(file_name) + '.txt')
  with open(filename, 'r') as f:
    # read the contents of the file into a string
    data = f.read()
    # print the contents of the file
    #print(data)
    return data
'''
def remove_i_from_DB(db_lst):
  #return a db list exactly like what Generate_db funcitons returns
  res = []
  if db_lst is not None:
    st = ""
    for trans in db_lst:
      st += str(trans.replace("i",""))
  return st
'''
uncleaned_db = read_db_from_txtFile(db_name)
#final_db = remove_i_from_DB(uncleaned_db)
final_db = uncleaned_db
freq_item_set = sam_apriori("database/DB1K.txt",ms)
print("DBG : ",freq_item_set)
print("LEN FREQ ITEM : ",len(freq_item_set))

output_file_name = "output_apriori.txt"
save_apriori_outputs(freq_item_set,output_file_name,ms)
