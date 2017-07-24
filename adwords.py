import operator
import sys
import csv
import random
random.seed(0)
from math import exp

# Done along with Rutvij Mehta - rmehta4


method = raw_input("1.greedy \n2.mssv \n3.balance\n[Type greedy , balance or mssv]\n")
                     
def main():

    query = list()
    
    with open('queries.txt','r') as txtfile:
      for q in txtfile:
        query.append(q.strip('\n'))

    file_dataset = open("bidder_dataset.csv", 'rb')
    bidder_dataset = csv.reader(file_dataset)
    next(bidder_dataset, None)

    adv={}
    keyword={}
    bid_value={}
    
    with open('bidder_dataset.csv', 'rb') as csvfile:
      #csvfile.next()
      csv_reader = csv.reader(csvfile)
      next(csv_reader,None)
      for row in csv_reader:
        if int(row[0]) not in adv:
          adv[int(row[0])] = float(row[3])
          bid_value[int(row[0])] = float(0)
        if row[1] in keyword:
          keyword[row[1]].append((int(row[0]),float(row[2])))
        else:
          keyword[row[1]] = []
          keyword[row[1]].append((int(row[0]),float(row[2]))) 
    
    revenue = 0
    if method=="greedy":
      func = greedy
      for keys in keyword:
         keyword[keys].sort(key=operator.itemgetter(1), reverse = True)
         revenue = greedy(query,adv.copy(),keyword.copy())  
    elif method=="balance":	
      func = balance
      revenue = balance(query,adv.copy(),keyword.copy())
    elif method=="mssv":
        func = mssv
        revenue = mssv(query,adv.copy(),keyword.copy(),bid_value.copy())
    
    print "Revenue: %.2f" % (revenue)
    
    ALG=0
    revenues = []
    for i in range(100):
        random.shuffle(query)
        if func == mssv:
          revenues.append(func(query,adv.copy(),keyword.copy(),bid_value.copy()))
        else:
          revenues.append(func(query,adv.copy(),keyword.copy()))
    ALG = float(sum(revenues))/len(revenues)
    
    print "Competitve Ratio:", ALG/sum(adv.values())
    

def greedy(queryList,bid,bid_list):

    revenue = 0
    for q in queryList:
        bids = bid_list[q]
        for x in bids:
            bid_temp = bid[x[0]]
            if (bid_temp-x[1])>=0:
                bid[x[0]] = bid_temp - x[1] 
                revenue = revenue + x[1]               
                break
    return revenue 
    
    
def balance(queryList,bid,bid_list):

    revenue = 0  
    
    for q in queryList:
        bids = bid_list[q]
        bid_temp = -1
        max_bid = 0
        ind_bid = 0
        
	for x in bids:
            if bid[x[0]] > bid_temp:
                bid_temp = bid[x[0]]
                ind_bid = x[1]
                max_bid = x[0]
        if (bid_temp-ind_bid) >= 0:
            revenue = revenue + ind_bid
            bid[max_bid] = bid[max_bid] - ind_bid
          
    return revenue

def mssv(queryList,bid,bid_list,bid_value):

    revenue = 0  
    
    for q in queryList:
        bids = bid_list[q]
        bid_temp = -1
        max_bid = 0
        ind_bid = 0
        for it in bids:
            mssv_fun = (1-exp((bid_value[it[0]]/bid[it[0]]) - 1)) * it[1]
            if mssv_fun > bid_temp and (bid_value[it[0]]+it[1]) <= bid[it[0]]:
                bid_temp = mssv_fun
                max_bid = it[0]
                ind_bid = it[1]
       
        revenue = revenue + ind_bid
        bid_value[max_bid] = bid_value[max_bid] + ind_bid
           
    return revenue
    
if __name__ == "__main__":
	main()
