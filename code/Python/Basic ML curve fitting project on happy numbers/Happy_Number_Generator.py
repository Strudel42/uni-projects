import time
import datetime
import csv
import numpy as np
from itertools import zip_longest
start_time = time.time()


def ishappy(n):
    """
    Takes an input of a number to check if it is happy
    Returns bool values True for a happy number and False for unhappy numbers
    """
    cache=[1, 7, 10, 13, 19, 23, 28, 31, 32, 44, 49, 68, 70, 79, 82, 86, 91, 94, 97, 100, 103, 109, 129, 130, 133, 139,
         167, 176, 188, 190, 192, 193, 203, 208, 219, 226, 230, 236, 239, 262, 263, 280, 291, 293, 301, 302, 310, 313,
         319, 320, 326, 329, 331, 338, 356, 362, 365, 367, 368, 376, 379, 383, 386, 391, 392, 397, 404, 409, 440, 446,
         464, 469, 478, 487, 490, 496, 536, 556, 563, 565, 566, 608, 617, 622, 623, 632, 635, 637, 638, 644, 649, 653,
         655, 656, 665, 671, 673, 680, 683, 694, 700, 709, 716, 736, 739, 748, 761, 763, 784, 790, 793, 802, 806, 818,
         820, 833, 836, 847, 860, 863, 874, 881, 888, 899, 901, 904, 907, 910, 912, 913, 921, 923, 931, 932, 937, 940,
         946, 964, 970, 973, 989, 998, 1000] #static cache used as a lookup table
                                             # It was found that a dynamically appended list of happy numbers to
    # check against was much slower (about 3-5 times slower) why the first 1000? because  you need a 13 digit number
    # (9,999,999,999,996) to get over 1000 when you apply the algorithm seeing as performing the algorithm on the
    # first 10^11 numbers would take about 25 hours it seems like a good break point

    #This while loop will perform the happy number algorithm
    while True:
        n = sum(int(i)**2 for i in str(n))
        if n in cache:
            return True
        elif n>1000: #if the algorithm spits out a number larger than 1000 it basically performs it again to get below 1000 and therefore uses the lookup table
            n = sum(int(i) ** 2 for i in str(n))
        else:
            return False


happies = [] #empty array of happy numbers
a = (10**4)+1 #a is a constant  for the maximum number of number the algorithm is applied for (a is an exclusive limit so the last number will be a-1)
while (time.time() - start_time) != 57600: #this while loop is a timer where 57,600 is 16 hours ( this can be changed if you like
    for i in range(0,a): #basic for loop to feed numbers into the ishappy function
        if ishappy(i): happies.append(float(i)) #appends happy numbers to happies list
    if ishappy(a-1) in happies: #break condition where if the timer is not met it will break if the upper limit is reached
        break

index_array = np.linspace(1, len(happies), len(happies)) #this basically puts the index number next to the happy number i.e (1,1 7,2) where the 2nd happy number is 7

#print(index_array)

d = [happies, index_array] #this creates headers for the lists
export_data = zip_longest(*d, fillvalue = '') #zip_longset is used instead of zip because of the size of the data set ensures they are written to in seperate columns

with open('result-{}.csv'.format(datetime.datetime.now().strftime('%d-%m-%Y %H-%M-%S')), 'w',encoding="ISO-8859-1", newline='') as f: #makes a unique reult file
    wr = csv.writer(f) # write data to csv file
    wr.writerow(("Happies", "Index"))
    wr.writerows(export_data)
f.close()

print("--- %s seconds ---" % (time.time() - start_time)) # tells you how long the program took to run ( for me a= 10^8 +1 took 11 mins)

