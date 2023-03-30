import os
import random
DB_sizes = [1000, 10000, 50000, 100000]

def generate_DB(num_trans, maximum_num_items = 100, min_trans_size = 5, max_trans_size = 15):
  all = [i for i in range(maximum_num_items)]
  DB = []
  for i in range(num_trans):
    num = random.randint(min_trans_size,max_trans_size)
    tr = random.sample(all, num)
    tr.sort()
    DB.append(tr)
    #print("SH_DBG: ",DB)
  return DB

'''
def add_i_to_DB(db_lst):
  #db: a list of transactions
  #trans sample: [18, 36, 47, 71, 96]
  #returns a list of strings each of which represents a trans
  #returned trans e.g: "i18,i36,i47,i71,i96"
  res = []
  for trans in db_lst:
    st= ""
    st += "i" + str(trans[0])
    for i in range(1,len(trans)):
      st+=","
      st+= "i" + str(trans[i])
    res.append(st)
    print("SHDBG: ",res)
  return res
'''

def save_db(db_lst, Filename):
  # Create the "db" subfolder if it doesn't exist
  if not os.path.exists("database"):
      os.mkdir("database")
  # Create the file inside the "db" subfolder
  #print(fileName)

  filename = os.path.join("database", str("DB"+'{:.0f}K'.format(Filename / 1000.0)) + '.txt')


  with open(filename, "w") as fp:
      for trans in db_lst:
        fp.write("%s\n" % trans)


def Gen_db(DB_sizes):

  for dbitem in DB_sizes:
    db_lst = generate_DB(dbitem)
    print(db_lst)
    # db_lst_updated = add_i_to_DB(db_lst)
    save_db(db_lst,dbitem)


Gen_db(DB_sizes)
