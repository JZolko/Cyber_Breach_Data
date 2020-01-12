"""
    This program looks at a file containing data from 2004 to present about any cyber security breaches.
    It can return records lost per website, per year, per sector, and can also display article titles.
"""

import csv
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy as np
def open_file(prompt_str):
    '''
        This function will take an input and try to open that file. 
        It'll keep asking until the file can be opened, and it will return the file pointer
    '''
    while True:
        test = input(prompt_str) # this prompts until the file can be opened and it'll return the file pointer
        if not(test):
            test = 'breachdata.csv'
        try:
            fp = open(test, encoding = 'utf-8' )
            reader = csv.reader(fp)
            return reader
        
        except IOError:
            print("File not found. Try again.")
    
    
def build_dict(reader):
    '''
        This takes a reader file with encoding and puts all the line data in a dict
    '''
    dic = {}
    next(reader,None)
    
    for line in reader:
        #print(line[11])
        elvdic,d1 = {},{}
        year = int(line[3])
        if not(line[1]or line[2]or line[3]\
               or line[4]or line[5]or line[6]): # if any of the lines are empty it passes
            # i couldnt think of a better way to do this 
            pass
        if len(line[11]) < 1: # if the website is empty
            pass
        
        else:
            if line[2]: # commas get replaced with nothing to make the int conversion
                lost = line[2].replace(',',  '')
            else:
                lost = 0
    
            elvdic[year] = (line[5], line[6]) # creates a dict with the words as the dict elements
            
            d1[line[0]] = (int(lost),year,line[4],[line[11]])
            entity = line[0]
            if entity in dic:
                dic[entity] += [(d1,elvdic)] #this adds stuff to the dictionary that isnt alreadt in the dict
            else:
                dic[entity] = [(d1,elvdic)]
    return dic

def top_rec_lost_by_entity(dic):
    '''
     This will show the top records lost by entity
    '''
    doc = {}
    final = []
    for key in dic.keys():
        for lst in dic[key]:
            d = lst[0]
            for tup in d: # this long process gets the tuples of the website
                if not (tup in doc):
                    doc[tup] = d[tup][0]
                
                else:
                    doc[tup] += d[tup][0]
                
    for key in doc.keys(): # this puts the values into a list of tuples to be returned
        item = (key, doc[key])
        final.append(tuple(item))            
    final = sorted(final, key= itemgetter(1,0), reverse= True) # this sorts the tuples by name and then value
    
    return final[:10]

def records_lost_by_year(dic):
    '''
        This looks through a dict and pulls out the year and number of records lost
        and puts them into a sorted tuple.
        
        This is basically the same as the previous function except the entity is replaced by a year
        and the values for that year are summed up
    '''
    doc = {}
    final = []
    for key in dic.keys():
        for lst in dic[key]:
            d = lst[0]
            for tup in d:
                #print(d)
                if not (d[tup][1] in doc): # this adds the values to get the max value
                    doc[d[tup][1]] = d[tup][0]
                
                else:
                    doc[d[tup][1]] += d[tup][0]
                
    for key in doc.keys(): # this goes through and adds them to a list that will be returned
        item = (key, doc[key])
        final.append((item))            
    final = sorted(final, key= itemgetter(1), reverse= True)
    
    return final


def top_methods_by_sector(dic):
    '''
        This function sorts through a dict and pulls out the key words of the sectors
        and sorts them based on number of occurences
    '''
    
    dec = {}
    final = []
    
    for key in dic.keys():
        for lst in dic[key]: #this breaaks apart the dict into two parts and only looks at the second dict
            d = lst[1]
            for key in d:
                final.append(d[key])
    #final = sorted(final, key= itemgetter(0, 1))
    for i in final:
        
        if not i[0] in dec.keys(): # makes a dict for the key
            dec[i[0]] = {}
        if not i[1] in dec[i[0]].keys(): # sets the second word value to 1 initially
            dec[i[0]][i[1]] = 1
        else:
            dec[i[0]][i[1]] += 1  # adds 1 to an existing word value
    
    return dec
        
def top_rec_lost_plot(names,records):
    ''' Plots a bargraph pertaining to
        the cybersecurity breaches data '''
        
    y_pos = np.arange(len(names)) #this does some stuff

    plt.bar(y_pos, records, align='center', alpha=0.5,
            color='blue',edgecolor='black')
    plt.xticks(y_pos, names, rotation=90)
    plt.ylabel('#Records lost')
    plt.title('Cybersecurity Breaches',fontsize=20)
    plt.show()
    
def top_methods_by_sector_plot(methods_list):
    ''' Plots the top methods used to compromise
        the security of a sector '''
    methods = [] ; quantities = []
    for tup in methods_list:
        methods.append(tup[0])
        quantities.append(tup[1])
    labels = methods
    sizes = quantities
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']

    plt.pie(sizes, labels=labels, colors = colors,
    autopct='%1.1f%%', shadow=True, startangle=140)
    
    plt.axis('equal')
    plt.show()
 
def main():
    BANNER = '''
    
                 _,.-------.,_
             ,;~'             '~;, 
           ,;                     ;,
          ;                         ;
         ,'                         ',
        ,;                           ;,
        ; ;      .           .      ; ;
        | ;   ______       ______   ; | 
        |  `/~"     ~" . "~     "~\'  |
        |  ~  ,-~~~^~, | ,~^~~~-,  ~  |
         |   |        }:{        |   | 
         |   l       / | \       !   |
         .~  (__,.--" .^. "--.,__)  ~. 
         |     ---;' / | \ `;---     |  
          \__.       \/^\/       .__/  
           V| \                 / |V  
            | |T~\___!___!___/~T| |  
            | |`IIII_I_I_I_IIII'| |  
            |  \,III I I I III,/  |  
             \   `~~~~~~~~~~'    /
               \   .       .   /
                 \.    ^    ./   
                   ^~~~^~~~^ 
                   
           
           ~~Cybersecurity Breaches~~        
                   @amirootyet    
                
    '''
    
    print(BANNER)
    
    MENU = '''  
[ 1 ] Most records lost by entities
[ 2 ] Records lost by year
[ 3 ] Top methods per sector
[ 4 ] Search stories
[ 5 ] Exit

[ ? ] Choice: '''
    
    prompt_str = "[ ? ] Enter the file name: "
    choice = input(MENU) # this takes the menu and makes it so the user can inout a value
    good = [1,2,3,4,5]
    
    while not(choice.isdigit()) or choice.isalpha()\
        or not(int(choice) in good): # only accepts numbers 1-5
            print('[ - ] Incorrect input. Try again.')
            choice = input(MENU)
    
    if choice == '5': # if the num is 5 it wont promopt for a file to be opened
        pass
    else:
        reader = open_file(prompt_str)
        dic= build_dict(reader)
    
    while True:
        while not(choice.isdigit()) or choice.isalpha()\
        or not(int(choice) in good): # only accepts nums 1-5
            print('[ - ] Incorrect input. Try again.')
            choice = input(MENU)
        
        if int(choice) == 1: # this is the records lost by entity
            yeet = top_rec_lost_by_entity(dic) # calls entity function for the items
            print("[ + ] Most records lost by entities...")
            
            for i in range(len(yeet)): # loops through the values and prints them in order
                print("-"*45)
                print("[ {:2d} ] | {:15.10s} | {:10d}"\
                      .format(i+1, yeet[i][0], yeet[i][1]))
            
            
            plot = input("[ ? ] Plot (y/n)? ") # if the user wants to graph the data
            
            if plot.lower() == 'y': # this plots the data into a graph
                d0,d1 = [],[]
                for item in yeet:
                    d0.append(item[0]) # puts the stuff into 2 different lists that can be used by
                    # the plot function
                    d1.append(item[1])
                final = [d0,d1]
                top_rec_lost_plot(final[0], final[1]) # plots the data
            
        
        elif int(choice) == 2: # records lost by year
            yeet = records_lost_by_year(dic) # calls lost by year function
            print("[ + ] Most records lost in a year...")
            
            for i in range(len(yeet)): # loops through the tuples and prints the data accordingly
                print("-"*45)
                print("[ {:2d} ] | {:<15d} | {:10d}"\
                      .format(i+1, yeet[i][0], yeet[i][1]))
            
            plot = input("[ ? ] Plot (y/n)? ")
            
            if plot.lower() == 'y':
                d0,d1 = [],[]
                for item in yeet:
                    d0.append(item[0]) # puts the stuff into 2 different lists that can be used by\
                    d1.append(item[1]) # the plot function
                final = [d0,d1]
                top_rec_lost_plot(final[0], final[1]) # plots the data 
            
        elif int(choice) == 3:
            yeet = top_methods_by_sector(dic) # calls the top methods by sector function

            print("[ + ] Loaded sector data.") # prints stuff
            
            keys = sorted(yeet.keys(), key= itemgetter(0, 1), reverse= False)
            print(*keys) # prints the keys that are sorted alphabetically
            
            sector = input("[ ? ] Sector (case sensitive)? ") # the key input
            
            while sector not in yeet: # if its not in the list, it reprompts
                print("[ - ] Invalid sector name. Try again.")
                sector = input("[ ? ] Sector (case sensitive)? ")
            
            lst = sorted(yeet[sector].items(), key= itemgetter(1), reverse= True)
            #print(lst)
            
            print("[ + ] Top methods in sector {}".format(sector))
            i = 0
            
            for item in lst: # this prints all the data neatly
                i += 1
                print("-"*45)
                print("[ {:2d} ] | {:15.10s} | {:10d}"\
                      .format(i,item[0], item[1]))
            
            plot = input("[ ? ] Plot (y/n)? ")
            
            if plot.lower() == 'y': # plots the values if the user wants the values plotted
                top_methods_by_sector_plot(lst)
                
        elif int(choice) == 4:
            lst = []
            ent = input("[ ? ] Name of the entity (case sensitive)? ") # name input
            while ent not in dic.keys(): # if the entity doesnt exist, it reprompts
                print("[ - ] Entity not found. Try again.")
                ent = input("[ ? ] Name of the entity (case sensitive)? ")
                
            for item in dic[ent]: # puts all the stories into a list to be printed
                for key in item[0].keys():
                    lst.append(item[0][key][2]) # adds the story to the list
            
            print("[ + ] Found {} stories:".format(len(lst)))
            for i in range(len(lst)): # prints all the stuff neatly
                print("[ + ] Story {}: {:10s}".format(i+1, lst[i]))
        
        elif int(choice) == 5: # if the user wants to exit they select 5
            print("[ + ] Done. Exiting now...")
            break
        choice = input(MENU)
    
if __name__ == "__main__":
     main()