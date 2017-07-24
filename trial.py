import operator
import sys
import csv
import random
random.seed(0)
from math import exp

method = raw_input("1.greedy \n2.mssv \n3.balance\n[Type 1 , 2 or 3]\n")

                        
def main():
    
    file_query = open("queries.txt","r")
    
    query = list()
    for queries in file_query:
        query.append(queries.strip('\n'))

    file_dataset = open("bidder_dataset.csv", 'rb')
    bidder_dataset = csv.reader(file_dataset)
    next(bidder_dataset, None)

    bid={}
    bid_list={}
    bid_value={}

    for bids in bidder_dataset:
        if int(bids[0]) not in bid:
            bid[int(bids[0])] = float(bids[3])
            bid_value[int(bids[0])] = float(0)
        if bids[1] in bid_list:
            bid_list[bids[1]].append((int(bids[0]),float(bids[2])))
        else:
            bid_list[bids[1]] = []
            bid_list[bids[1]].append((int(bids[0]),float(bids[2])))

   
   
    alg=0
    opt = sum(bid.values())
    revenue=0

    
    if method == "1":
        print "\nGreedy Method"
        for keys in bid_list:
            bid_list[keys].sort(key=operator.itemgetter(1), reverse = True)
        revenue = greedy(query,bid.copy(),bid_list.copy())

        for i in range(0,100):
            random.shuffle(query) 
            alg = alg+greedy(query,bid.copy(),bid_list.copy())

    if method == "2":
        print "\nBalance Method"	
        revenue = mssv(query,bid.copy(),bid_list.copy(),bid_value.copy())

        for i in range(0,100):
            random.shuffle(query) 
            alg = alg+mssv(query,bid.copy(),bid_list.copy(),bid_value.copy())    

    if method == "3":
        print "\nmssv method"
        revenue = balance(query,bid.copy(),bid_list.copy())

        for i in range(0,100):
            random.shuffle(query) 
            alg = alg+balance(query,bid.copy(),bid_list.copy())          
        
    print revenue
    print (alg/100)/opt 
    

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
