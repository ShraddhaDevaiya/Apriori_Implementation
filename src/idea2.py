import pandas as pd
import sys
import random
import math
import time
import json
import os
import ast
import numpy as np
from mlxtend.frequent_patterns import apriori

if __name__ == '__main__':
    db_name = sys.argv[1]
    ms = sys.argv[2]
def save_idea2_outputs(freq_items, Filename,ms):
  # Create the "output" folder if it doesn't exist
  if not os.path.exists("output"):
    os.mkdir("output")
  # Create the file inside the "output" folder
  filename = os.path.join("output", Filename)

  with open(filename, "w") as fp:
      fp.write("Min Support - %s\n" % ms)
      fp.write("Frequent Item - %s\n" % freq_items)

def sam_apriori(data, min_support):
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
    #print(df)
    final_frequent_itemsets = []
    # find frequent itemsets
    frequent_itemsets = []

    for item in df.columns:
        support = df[item].sum() / len(df)

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

def find_frequent_itemsets_partitioning(database, min_sup):
    #print(database)
    with open(database, 'r') as f:
        lines = f.readlines()
        result = [line.strip() for line in lines]
        data= []

    for s in result:
        l = ast.literal_eval(s)
        data.append(l)
        #print("SHDBG: ", len(data))
    # Step 1: set the number of partitions and partition the database
    num_partitions = 8  # set the number of partitions
    partition_size = len(data) // num_partitions  # calculate partition size
    print("LEN_DB: ",len(data))
    partitions = [data[i:i + partition_size] for i in range(0, len(data), partition_size)]
    # print("PARTITIONS: ",partitions)
    # Step 2: find local frequent itemsets for each partition and combine to form candidate itemsets
    candidate_itemsets = set()  # initialize empty set for candidate itemsets
    for partition in partitions:
        # print("my: ",partition)
        # local_frequent_itemsets = find_local_frequent_itemsets(partition, min_sup)
        local_frequent_itemsets = sam_apriori(partition, min_sup)
        candidate_itemsets.update(local_frequent_itemsets)

    # Step 3: count the support of candidate itemsets in the entire database
    frequent_itemsets = set()
    for itemset in candidate_itemsets:
        support_count = count_support(itemset, data)
        if str(support_count) >= min_sup * len(data):
            frequent_itemsets.add(itemset)

    # Step 4: return frequent itemsets
    return frequent_itemsets


def count_support(itemset, database):
    #print("COUNT DB: ", itemset)
    # count the number of transactions in the database that contain the itemset
    count = 0
    for transaction in database:
        if itemset.issubset(transaction):
            count += 1
    return count

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
# library output for comparison

with open("database/DB1K.txt", 'r') as f:
    lines = f.readlines()
    result = [line.strip() for line in lines]
    s_data= []

for s in result:
    l = ast.literal_eval(s)
    s_data.append(l)

df = pd.DataFrame(s_data)
df = pd.get_dummies(df.apply(pd.Series).stack()).sum(level=0)

li_frequent_itemsets = apriori(df, min_support=0.05, use_colnames=True)

def validate_itemsets(my, library_set):
    if my == library_set:
        print("YOU WON :)")
    else:
        print("YOU LOST ! itemsets not matching with library output.")


uncleaned_db = read_db_from_txtFile(db_name)
final_db = uncleaned_db
# print("DBG: ",final_db)
# final_db = remove_i_from_DB(uncleaned_db)
#print("DB : ",final_db)
freq_item_set = find_frequent_itemsets_partitioning("database/DB1K.txt",ms)
sets_list = []
for frozenset_item in freq_item_set:
    sets_list.append(set(frozenset_item))
sorted_sets_list = sorted(sets_list, key=list)
print("DBG: ",len(sorted_sets_list))
#print("DBG: ",sorted_sets_list)
#validate_itemsets(li_frequent_itemsets['itemsets'], sorted_sets_list)

output_file_name = "output_idea2.txt"
save_idea2_outputs(freq_item_set,output_file_name,ms)
