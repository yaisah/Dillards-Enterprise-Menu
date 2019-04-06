#Yaisah Granillo
##
##Remember to install the necessary modules below
from sys import exit
#this will import prettytable 
from prettytable import PrettyTable as pt
#this will import our SQL module
import pypyodbc
#this will import the necessary modules we need for the twitter feed
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import time
#this will import the image at the beginning of the program
from tkinter import *
import base64
import urllib.request

print("Welcome to our Dillard's database")
print("To prove you are not a robot - close the image to begin")

#this will import our "captcha" image 
root = Tk()
URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Dillard%27s_Logo.svg/1200px-Dillard%27s_Logo.svg.png"
link = urllib.request.urlopen(URL)
raw_data = link.read()
link.close()
next = base64.encodestring(raw_data)
image = PhotoImage(data = next)
label = Label(image=image)
label.pack()
root.mainloop()
print("\nThank you for verifying that.")

#this is the connection to the Dillards database 
db_host = 'xxx.xxx.xxx'
db_name = 'UA_DILLARDS_2016'
db_user = 'xxx'
db_password = 'xxx'
connection_string = 'Driver={SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';'
db = pypyodbc.connect(connection_string)

#Variables that contains the user credentials to access Twitter API 
consumer_key="hhmJUidFQd6zPpL0fzuHXAiBj"
consumer_secret="U8KwqDjCYfY30FBw72WvKQzvHhu3jmge7XOUL5PyZKEnD2phDb"
access_token="224449678-lkWJyXruTEh5NidnSB3LTRnWcQX9hWYNSSr6HRGT"
access_token_secret="3YEGmCWOgqQmMDffCl43X4uqtGYavfxPSq5VimQG9qxPY"
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#the below classes are necessary for our loop to function
class Scene(object): 
    def enter(self):
        exit()
#this will initialize our loop
class initialize(object):
    def __init__(self, scene_map):
        self.scene_map = scene_map
   
    def userloop(self):
        current_scene = self.scene_map.opening_scene()
        while True:
            next_scene_name = current_scene.enter()
            current_scene = self.scene_map.next_scene(next_scene_name)

#This class will be the main menu for the Enterprise user
class Central(Scene):
    def enter(self):
        print("\n       CENTRAL DATABASE")
        print("Enter 1 for the amount of transactions within a particular store.")
        print("Enter 2 for Returns information of MENS in NM")
        print("Enter 3 for Total Customers in each store")
        print("Enter 4 for Customers with bigger purchases")
        print("Enter 5 for Items not on sale")
        print("Enter 6 for Transactions by state")
        print("Enter 7 for our twitter data feed")
        print("Enter q to exit")

        user_action = input("\nWhat information or report are you interested in displaying: ")

        if user_action == '1': 
            print("\nAmount of transactions")
            return 'query1'
        elif user_action == '2': 
            print("\nReturns")
            return 'query2'
        elif user_action == '3': 
            print("\nTotal Customers")
            return 'query3'
        elif user_action == '4': 
            print("\nCustomers with bigger purchases")
            return 'query4'
        elif user_action == '5': 
            print("\nItems not on sale")
            return 'query5'
        elif user_action == '6': 
            print("\nTransactions by state")
            return 'query6'
        elif user_action == '7':
            print("\nOur live twitter feed")
            return 'twitterfeed'
        elif user_action == 'q':
            print("Goodbye")
            exit()
        else:
            print("\nSorry, the system doesn't recognize your input. Please try again")
            return 'central'
            
class TwitterFeed(Scene):   
    def enter(self):
        print("\nRemember this is a live feed... which means the program will continue to run")
        print(" ")
        #listener that receives tweets from stream
        class StdOutListener(tweepy.StreamListener):
            def on_data(self, data):
                print("NEW TWEET!")
                try:
                    tweet=json.loads(data)
                    tweets = ('@%s: %s' % (tweet['user']['screen_name'], tweet['text'].encode('ascii', 'ignore')))
                    print (tweets)
                    saveFile = open('twitDB.csv', 'a')
                    saveFile.write(tweets)
                    saveFile.write('\n')
                    saveFile.close()
                    return True
                
                except BaseException as e:
                    print ('failed ondata,',str(e))
                    time.sleep(5)
                    return True
                
            def on_error(self, status):
                print (status)
                return True
        #This handles Twitter authetification and the connection to Twitter Streaming API
        l = StdOutListener()
        stream = Stream(auth, l)
        #This streams the live feed based on this word 
        stream.filter(track=['dillards'])

#Queries 1-6 all have the same context (only different queries of course), thus we will use Query1 as our main
#comment section for cexplaining the significance of the code
class Query1(Scene):          
    def enter(self):
        print("\nOkay. You are interested in knowing the amount of transactions within a particular store.")          
     
        #We need to define our cursor object to manage the context of a fetch and execute operation
        cursor = db.cursor()
        action = input("Which store do you want? (i.e. 140): ")
        #Defining our SQL query
        sqlcommand =("select count(TRAN_NUM) as TRANSACTIONS from TRANSACT where STORE =?")
        #this cursor object ".execute()" will execute our SQL query with the specific action of our user
        #AKA their desired store. 
        cursor.execute(sqlcommand, [action])
        #this defines the headers of our expected result
        col_names = [cn[0] for cn in cursor.description]
        #this will fetch all our table rows of a query result
        rows = cursor.fetchall()
        #Now we are defining our prettytable styles
        y1 = pt()
        #this is desired padding width for our table
        y1.padding_width = 1
        #this will add all our columns into one table format, otherwise the columns are individual with no style
        #as you can see we are only expecting one column to display
        y1.add_column(col_names[0],[row[0] for row in rows])
        print(y1)
        return 'central'

class Query2(Scene):          
    def enter(self):
        print("\nThis is the amount of returns from the MENS department in New Mexico state")          
     
        cursor = db.cursor()
        sqlcommand =("SELECT * from Dillards_Returns_L where DeptCent_Desc = 'MENS' AND State_Loc = 'NM'")
        cursor.execute(sqlcommand)
        col_names = [cn[0] for cn in cursor.description]
        rows = cursor.fetchall()
        y1 = pt()
        y1.padding_width = 1
        y1.add_column(col_  names[0],[row[0] for row in rows])
        y1.add_column(col_names[1],[row[1] for row in rows])
        y1.add_column(col_names[2],[row[2] for row in rows])
        y1.add_column(col_names[3],[row[3] for row in rows])
        y1.add_column(col_names[4],[row[4] for row in rows])
        y1.add_column(col_names[5],[row[5] for row in rows])
        y1.add_column(col_names[6],[row[6] for row in rows])
        y1.add_column(col_names[7],[row[7] for row in rows])

        print(y1)
        return 'central'

class Query3(Scene):          
    def enter(self):
        print("\nThis is the total customers we've had in each store")          
     
        cursor = db.cursor()
        sqlcommand =("SELECT Count(CUST_ID) as TotalCustomers, STORE FROM TRANSACT GROUP BY STORE ORDER BY TotalCustomers DESC;")
        cursor.execute(sqlcommand)
        col_names = [cn[0] for cn in cursor.description]
        rows = cursor.fetchall()
        y1 = pt()
        y1.padding_width = 1
        y1.add_column(col_names[0],[row[0] for row in rows])
        y1.add_column(col_names[1],[row[1] for row in rows])
        print(y1)
        return 'central'

class Query4(Scene):          
    def enter(self):
        print("\nOkay, you want to know how many customers spent more than $500")          
     
        cursor = db.cursor()
        sqlcommand =("SELECT COUNT(CUST_ID) as TotalCustomers, TRAN_DATE as TransactionDate FROM TRANSACT WHERE TRAN_AMT > 500 GROUP BY TRAN_DATE ORDER BY TRAN_DATE desc")
        cursor.execute(sqlcommand)
        col_names = [cn[0] for cn in cursor.description]
        rows = cursor.fetchall()
        y1 = pt()
        y1.padding_width = 1
        y1.add_column(col_names[0],[row[0] for row in rows])
        y1.add_column(col_names[1],[row[1] for row in rows])
        print(y1)
        return 'central'
     
class Query5(Scene):          
    def enter(self):
        print("Okay, you want to know which items were NOT ON SALE when purchased")          
     
        cursor = db.cursor()
        sqlcommand =("SELECT ITEM_ID, SKU, ORIG_PRICE FROM TRANSACT WHERE ORIG_PRICE != SALE_PRICE;")
        cursor.execute(sqlcommand)
        col_names = [cn[0] for cn in cursor.description]
        rows = cursor.fetchall()
        y1 = pt()
        y1.padding_width = 1
        y1.add_column(col_names[0],[row[0] for row in rows])
        y1.add_column(col_names[1],[row[1] for row in rows])
        y1.add_column(col_names[2],[row[2] for row in rows])
        print(y1)
        return 'central'
      

class Query6(Scene):          
    def enter(self):
        print("Okay, you want to know the amount of transactions in a particular state")
        
        action = input("what state do you want information on (i.e. TX)?")
        cursor = db.cursor()
        sqlcommand =("SELECT count(t.TRANSACTION_ID) as transactions, s.state from TRANSACT t LEFT OUTER JOIN STORE s ON t.store = s.STORE where s.state =? group by  s.state;")
        cursor.execute(sqlcommand, [action])
        col_names = [cn[0] for cn in cursor.description]
        rows = cursor.fetchall()
        y1 = pt()
        y1.padding_width = 1
        y1.add_column(col_names[0],[row[0] for row in rows])
        y1.add_column(col_names[1],[row[1] for row in rows])
        print(y1)
        return 'central'

#For the loop to work, we need to define each of our classes here and make sure it talks to our initialize class so that it knows what to return.    
class queries(object):
    scenes = {
        'central': Central(),
        'twitterfeed':TwitterFeed(),
        'query1':Query1(),
        'query2':Query2(),
        'query3':Query3(),
        'query4':Query4(),
        'query5':Query5(),
        'query6':Query6(),
        }
        
    def __init__(self, start_scene):
        self.start_scene = start_scene
    def next_scene(self, scene_name):
        return queries.scenes.get(scene_name)
    def opening_scene(self):
        return self.next_scene(self.start_scene)

x = queries('central')
y = initialize(x)
y.userloop()


 
