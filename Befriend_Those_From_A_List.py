#### A script for copying the twitter users you follow into one of your twitter lists
import json
import tweepy
import time
import re
import random

#### Set Twitter API key dictionary
try:    #### Attempt to load API keys file
    keys_json = json.load(open('/usr/local/keys.json'))
    #### Specify key dictionary wanted (generally [Platform][User][API])
    #Keys = keys_json["Twitter"]["ClimateCong_Bot"]["ClimatePolitics"]
    Keys = keys_json["Twitter"]["AGreenDCBike"]["HearHerVoice"]
except Exception as e:
    er = e
    if er.errno == 2: #File not found enter key dictionary values manually
        print("\nNo twitter API key was found in /usr/local/keys.json\n",
             "Acquire an API key at https://apps.twitter.com/\n",
             "to supply key manually press Enter\n")
        Keys = {}
        Keys['Consumer Key (API Key)'] = input('Enter the Twitter API Consumer Key\n')
        Keys['Consumer Secret (API Secret)'] = input('Enter the Twitter API Consumer Secret Key\n')
        Keys['Access Token'] = input('Enter the Twitter API Access Token\n')
        Keys['Access Token Secret'] = input('Enter the Twitter API Access Token Secret\n')
        Keys['Owner'] = input('Enter your Twitter username associated with the API keys\n')
    else:
        print(e)


#### Access API using key dictionary definitions
auth = tweepy.OAuthHandler( Keys['Consumer Key (API Key)'], Keys['Consumer Secret (API Secret)'] )
auth.set_access_token( Keys['Access Token'], Keys['Access Token Secret'] )
api = tweepy.API(auth)
user = Keys['Owner']

#### Specify list to befriend
url = input("Enter the URL of the list you would like to befriend\n") #leaders #favs-always-follow
list_owner = url.split("/")[3]
list_name = url.split("/")[5]


#### Define twitter rate determining loop
#Follow add rate limited to 1000 per 24hrs: https://support.twitter.com/articles/15364
def twitter_rates():
    stats = api.rate_limit_status()  #stats['resources'].keys()
    for akey in stats['resources'].keys():
        if type(stats['resources'][akey]) == dict:
            for anotherkey in stats['resources'][akey].keys():
                if type(stats['resources'][akey][anotherkey]) == dict:
                    #print(akey, anotherkey, stats['resources'][akey][anotherkey])
                    limit = (stats['resources'][akey][anotherkey]['limit'])
                    remaining = (stats['resources'][akey][anotherkey]['remaining'])
                    used = limit - remaining
                    if used != 0:
                        print("  Twitter API used:", used, "requests used,", remaining, "remaining, for API queries to", anotherkey)
                    else:
                        pass
                else:
                    pass  #print("Passing")  #stats['resources'][akey]
        else:
            print(akey, stats['resources'][akey])
            print(stats['resources'][akey].keys())
            limit = (stats['resources'][akey]['limit'])
            remaining = (stats['resources'][akey]['remaining'])
            used = limit - remaining
            if used != 0:
                print("  Twitter API:", used, "requests used,", remaining, "remaining, for API queries to", akey)
                pass

twitter_rates()




#### Get the list of users
#followers = api.followers_ids(user)
list1 = friends = api.friends_ids(user)
print("The number of users followed is: " +str(len(list1)))


#### Get list of user ids from those within the list of interest
listed = []
for page in tweepy.Cursor(api.list_members, list_owner, list_name).pages():
    listed.extend(page)
    #time.sleep(2)
    ##twitter_rates()
    #print(len(listed))

list2=[]
for one in listed:
    list2.append(one.id)

print("The number of users in " + list_owner +"'s list", list_name, "is: " +str(len(list2)))


#### Remove those user ids which are already in the list
list3 = []
befriend =  [x for x in list2 if x not in list1]
newfriends = str(len(befriend))
print("The number of users that are not allready followed: " + newfriends)

random.shuffle(befriend)

for newfriend in befriend:
    print(str(len(befriend)), "remaining friends to be added, of", newfriends, "total", end='\r')
    #print(newfriend)
    try:
        api.create_friendship(newfriend)
        befriend.remove(newfriend)
        time.sleep(random.uniform(1,180))
    except Exception as e:
        er = e
        if e.api_code == 160:
            print("Request to befriend made, pending approval")
            befriend.remove(newfriend)
        if e.api_code == 50:
            print("User not found")
            pass
        else:
            print(e)
            input("Press Enter to continue...")
            befriend.remove(newfriend)
            pass


print("Completed")
twitter_rates()
sys.exit() #End app
