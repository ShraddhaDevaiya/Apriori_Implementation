import sys
import time
import os
import ast
import pandas as pd
from mlxtend.frequent_patterns import apriori

if __name__ == "__main__":
    db_name = sys.argv[1]
    ms = sys.argv[2]
    partition_size = sys.argv[3]


def save_idea2_outputs(freq_items, Filename, ms, ts, partition):
    # Create the "output" folder if it doesn't exist
    if not os.path.exists("output"):
        os.mkdir("output")

    number = float(ms)
    form = "{:.2f}".format(number).lstrip("0").replace(".", "")

    filename2 = os.path.join("output", db_name + "_Idea2_" + form + ".freq")
    with open(filename2, "w") as fp:
        fp.write("Frequent itemsets are following: \n")
        fp.write("%s" % str(freq_items))

    filename3 = os.path.join("output", Filename)
    with open(filename3, "w") as fp:
        fp.write("The frequent itemsets are stored in %s.freq," % db_name)
        fp.write("under minimun support = %s\n" % ms)
        fp.write("The time spent is %f seconds to get the frequent itemsets.\n" % ts)
        fp.write("The number of the partitions used is %s" % partition)


file_path = "./database/" + db_name + ".txt"
with open(file_path, "r") as f:
    lines = f.readlines()
result = [line.strip() for line in lines]
data = []

for s in result:
    l = ast.literal_eval(s)
    data.append(l)
print(len(data))

# Apriori Implementation


def sam_apriori(data, min_support):
    # print("My:", data)

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

        if support >= float(min_support):
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
            support = (df[list(itemset)].sum(axis=1) == len(itemset)).sum() / len(df)
            if support >= float(min_support):
                final_frequent_itemsets.append(itemset)
                frequent_itemsets.append(itemset)
        k += 1
    return final_frequent_itemsets


# idea2 - partition
def find_frequent_itemsets_partitioning(database, min_sup, num_partitions):
    # Step 1: set the number of partitions and partition the database
    # num_partitions = 8  # set the number of partitions
    partition_size = len(database) // int(num_partitions)  # calculate partition size
    partitions = [
        database[i : i + partition_size]
        for i in range(0, len(database), partition_size)
    ]

    # Step 2: find local frequent itemsets for each partition and combine to form candidate itemsets
    candidate_itemsets = set()  # initialize empty set for candidate itemsets
    for partition in partitions:
        # print(partition)
        # local_frequent_itemsets = find_local_frequent_itemsets(partition, min_sup)
        local_frequent_itemsets = sam_apriori(partition, min_sup)
        candidate_itemsets.update(local_frequent_itemsets)

    # Step 3: count the support of candidate itemsets in the entire database
    frequent_itemsets = set()
    for itemset in candidate_itemsets:
        support_count = count_support(itemset, database)
        temp = 0.0
        temp = float(min_sup) * len(database)
        if support_count >= temp:
            frequent_itemsets.add(itemset)

    # Step 4: Validate Frequent Itemsets
    df = pd.DataFrame(data)
    df = pd.get_dummies(df.apply(pd.Series).stack()).sum(level=0)
    min_sup = float(min_sup)
    li_frequent_itemsets = apriori(df, min_support=min_sup, use_colnames=True)
    if len(frequent_itemsets) == len(li_frequent_itemsets["itemsets"]):
        if set(frequent_itemsets) == set(li_frequent_itemsets["itemsets"]):
            print("YOU WON :)")
        else:
            print("YOU LOST ! itemsets not matching with library output.")
    else:
        print("SAM ITEM: ", set(frequent_itemsets))
        print("LEN SAM ITEM: ", len(frequent_itemsets))
        print("YOU LOST ! itemsets not matching with library output.")

    # Step 5: return frequent itemsets
    return frequent_itemsets


def count_support(itemset, database):
    # count the number of transactions in the database that contain the itemset
    count = 0
    for transaction in database:
        if itemset.issubset(transaction):
            count += 1

    return count


# partition time comput
start_time = time.time()
sam_freq_item = find_frequent_itemsets_partitioning(data, ms, partition_size)
end_time = time.time()
temp_time = 0.0
temp_time = end_time - start_time

output_file_name = "output_idea2.txt"
save_idea2_outputs(sam_freq_item, output_file_name, ms, temp_time, partition_size)
print(
    "The frequent itemsets are stored in",
    db_name,
    ".freq, under minimun support = ",
    ms,
)
print("The time spent is ", temp_time, " seconds to get the frequent itemsets.")
print("The number of the partitions used is ", partition_size)
