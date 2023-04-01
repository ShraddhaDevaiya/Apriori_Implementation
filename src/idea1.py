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

def save_idea1_outputs(freq_items,num_of_rounds, Filename,ms):
  # Create the "output" folder if it doesn't exist
  print(freq_items)
  if not os.path.exists("output"):
    os.mkdir("output")
  # Create the file inside the "output" folder
  filename = os.path.join("output", Filename)

  with open(filename, "w") as fp:
      fp.write("Min Support - %s\n" % ms)
      fp.write("Round - %s\n" % num_of_rounds)
      for item in freq_items:
        start = time.time()
        end = time.time()
        fp.write("Frequency -  %s\n" % item)
        fp.write("Time -  %s\n" % float(end - start))


def check_stop_condition(cands):
  for time in cands.keys():
    for n_val in cands[time]:
      return False
  return True

def add_newFreq_to_allFreqs(new_freq, freqs):
  if freqs.get(new_freq[1],-1) == -1:
    freqs[new_freq[1]] = []
  freqs[new_freq[1]].append(new_freq[2])

def add_new_cands_with_their_freq(new_cands_info,cands ,trans, timestamp):
  if(cands.get(timestamp,-1) == -1):
    cands[timestamp] = {}
  for item in new_cands_info:
    n = len(item)
    if(cands[timestamp].get(n,-1) == -1):
      cands[timestamp][n] = {}
    cands[timestamp][n][item] = 0
    if checkSubset(item, trans):
      cands[timestamp][n][item] += 1

def merge_sorted_lists(lst1, lst2):
  a = list(set(lst1 + lst2))
  a.sort()
  return tuple(a)

def try_to_merge(freq_item, new_freq):
  if len(freq_item) == 1:
    return merge_sorted_lists(freq_item, new_freq)
  if (freq_item[:-1] == new_freq[:-1]):
    return merge_sorted_lists(freq_item, new_freq)
  return tuple()

def merge_and_produce_new_cands(freqs, new_freq_info):
  new_cands = []
  new_freq = new_freq_info[2]
  m = len(new_freq)
  if freqs.get(m,-1)==-1:
    return []
  for freq_item in freqs[m]:
    res = try_to_merge(freq_item, new_freq)
    if (not (res==tuple())):
      new_cands.append(res)
  return new_cands

def remove_new_freq_from_candidates(ids_became_freq, cands):
  for info in ids_became_freq:
    del cands[info[0]][info[1]][info[2]]

def checkSubset(obj1, obj2):
  return set(obj1).issubset(obj2)

def update_freq(trans, cands, mf):
  ids = []
  m = len(trans)
  times = list(cands.keys())
  for time in times:
    for n in range(1,m+1):
      if (cands[time].get(n,False)):
        for k in cands[time][n].keys():
          if(checkSubset(k, trans)):
            cands[time][n][k] +=1
            if cands[time][n][k] >= mf:
              ids.append((time,n,k,cands[time][n][k]))
  return ids

def drop(cands,i):
  if not(cands.get(i,-1) ==-1):
    del cands[i]

def init_candidates(db, cands):
  uniques = [numb for trans in db for numb in trans]
  cands[0] = {}
  cands[0][1] = {}
  for s in set(uniques):
    cands[0][1][(s,)] = 0

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

def idea1(dbase, ms):
  #print("DB LEN: ", dbase)
  size = len(dbase)
  mf = math.ceil(int(size) * float(ms))
  cands = {}
  freqs = {}
  stop = False
  round = 0
  with open(dbase, 'r') as f:
    lines = f.readlines()
    result = [line.strip() for line in lines]
    db= []

  for s in result:
    l = ast.literal_eval(s)
    db.append(l)
  #print("DB LEN: ", db)

  init_candidates(db, cands)

  while(not stop):
    round +=1
    #print(f"{round=}")

    for i in range(size):

      if(round==1):
        pass
      else:
        drop(cands,i)

      ids_became_freq=update_freq(db[i],cands,mf)
      remove_new_freq_from_candidates(ids_became_freq, cands)

      for new_freq in ids_became_freq:
        new_cand_info = merge_and_produce_new_cands(freqs, new_freq)
        add_new_cands_with_their_freq(new_cand_info,cands, db[i], i)
        add_newFreq_to_allFreqs(new_freq, freqs)

      stop = check_stop_condition(cands)
      if stop:
        break
    print("IDEA1 OUT: ",freqs)
  return round, freqs


uncleaned_db = read_db_from_txtFile(db_name)
#final_db = remove_i_from_DB(uncleaned_db)
num_of_rounds , freq_dict = idea1("database/DB1K.txt",ms)


## Now you have to print the number of rounds as well as savign the resutls\

output_file_name = "output_idea1.txt"
save_idea1_outputs(freq_dict,num_of_rounds,output_file_name,ms)
print("TYPE OF FREQUENT ITEM: ", len(freq_dict.values()))
temp = []
total_length = 0
temp = freq_dict.values()

for sublist in temp:
    for element in sublist:
        total_length += 1
print("LEN freq item: ", total_length)     