## SI507 Final Project - Get your congresman's tweets
## yunongx

import requests
import sys
import json
import webbrowser
import secrets
# import random

PROPUBLICA_API_KEY = secrets.PROPUBLICA_API_KEY
CACHE1_FILENAME = "congressmen_cache.json"
CACHE2_FILENAME = "userid_cache.json"

#### SET UP CACHE FILES DETECTOR ###
try:
    with open(CACHE1_FILENAME, 'r') as file:
       congressmen_cache = json.load(file)
    print("Oh good local congressmen cache detected...")
except:
    congressmen_cache = {}
try:
    with open(CACHE2_FILENAME, 'r') as file:
       userid_cache = json.load(file)
    print("Oh great local tweets cache detected...")
except:
    userid_cache = {}

#### SET UP THE CONGRESSMEN FINDER ####
class Congressman:
    def __init__(self, first_name="Name Unknown", last_name="Name Unknown", short_title="Title Unknown", state="State Unknown", party ="Party Unknown", gender="Gender Unkown", twitter=" Twitter Unknown", votes_with_party=None, json1=None):
        if json1 is None:
            self.first_name = first_name
            self.last_name = last_name
            self.short_title = short_title
            self.state = state
            self.party = party
            self.gender = gender
            self.votes_with_party = votes_with_party
            self.twitter = twitter
        else:
            self.first_name = json1['first_name']
            self.last_name = json1['last_name']
            self.short_title = json1['short_title']
            self.state = json1['state']
            self.party = json1['party']
            self.gender = json1['gender']
            self.twitter = json1['twitter_account']
            if json1['twitter_account'] == '':
                self.twitter = "No Record"
            try:
                self.votes_with_party = json1['votes_with_party_pct']
            except KeyError:
                self.votes_with_party = "Not available"
    def info(self):
        return f'{self.first_name} {self.last_name}, {self.state}, [gender] {self.gender}, [party] {self.party}, [votes with party %] {self.votes_with_party}'

class Senator(Congressman):
    def __init__(self, first_name="Name Unknown", last_name="Name Unknown", short_title="Title Unknown", state="State Unknown", party="Party Unknown", twitter=" Twitter Unknown", gender="Gender Unknown", votes_with_party=None, state_rank=None, json1=None):
        super().__init__(first_name, last_name, short_title, state, party, gender, twitter, votes_with_party, json1)
        if json1 is None:
            self.state_rank = state_rank
        else:
            self.state_rank = json1['state_rank']
    def info(self):
        if self.state_rank == '':
            self.state_rank = "No data"
        return f'{super().info()}, [state_rank] {self.state_rank}'

class Representative(Congressman):
    def __init__(self, first_name="Name Unknown", last_name="Name Unknown", short_title="Title Unknown", state="State Unknown", party="Party Unknown", gender="Gender Unknown", twitter=" Twitter Unknown", votes_with_party=None, district=None, json1=None):
        super().__init__(first_name, last_name, short_title, state, party, gender, twitter, votes_with_party, json1)
        if json1 is None:
            self.district = district
        else:
            try:
                self.district = json1['district']
            except KeyError: 
                self.district = None 
    def info(self):
       return f'{super().info()}, [district] {self.district}'

def get_members(congress, chamber, state=None):
    '''return a list of congress members based on the selected number of congress, chamber, and state.
    
    Parameters
    ----------
    congress: int
        Number of congress, ranging from 114 to 117.
    chamber: str
        Chamber of Congress,'senate' or ' house'.
    state: str
        Two-digit abbreviation of a U.S. state.

    Returns
    -------
    list 
        A list of dictionaries of the Congress members' information
    '''
    Base_URL = f"https://api.propublica.org/congress/v1/{congress}/{chamber}/members.json"
    headers = {'X-API-Key': PROPUBLICA_API_KEY}
    response = requests.get(Base_URL, headers=headers)
    data = response.json()['results'][0]['members']
    if state:
        state_member = []
        for member in data:
            if member['state'] == state:
                state_member.append(member)
        return state_member
    else:
        return data

def congress_query():
    '''Prompt to ask the user to enter a Congress number
    The user will be prompted to enter a Congress number until they enter a valid integer from 114 to 117, \
    or choose to exit.
    
    Parameters
    ----------
    None

    Returns
    -------
    int
        The number of the Congress
    '''
    while True:
      congress = input("Please enter a Congress number of your interest [(114-117) available], or enter 'exit' to quit: ")
      if congress.lower() == 'exit':
        print("Bye!")
        sys.exit(0)
      elif congress.isnumeric() is False:
        print("Please enter a valid number.")
      else: 
            congress = int(congress)
            if congress not in [114, 115, 116, 117]:
                print("Only 114-117 are available. Please enter a valid number.")
            else:
                break
    # congress = random.randint(114,118) ### for auto-generating comprehensive cache
    return congress
            
def chamber_query():
    '''Prompt to ask the user to enter a chamber of Congress.
    The user will be prompted to enter a chamber of Congress until they enter 'house' or 'senate' (case-insensitive),\
    or choose to exit.
    
    Parameters
    ----------
    None2

    Returns
    -------
    itr
        The chamber of Congress, 'house' or 'senate'
    '''
    while True:
      chamber = input("Which chamber are you looking for? Enter 'senate' or 'house', or enter 'exit' to quit: ")
      
      if chamber.lower() == 'exit':
        print("Bye!")
        sys.exit(0)
      elif chamber.lower() not in ['senate', 'house']:
        print("Please check your spelling. Enter a valid chamber: ")
      else:
        chamber = chamber.lower()
        break
    # chamber = random.choice(['senate', 'house']) ### for auto-generating comprehensive cache
    return chamber

def state_query():
    '''Prompt to ask the user to enter a state abbreviation.
    The user will be prompted to enter a state until they enter a valid 2-digit U.S. state abbreviation (case-insensitive),\
    or choose to exit.
    
    Parameters
    ----------
    None

    Returns
    -------
    None or str
        If the user enter 'no'(case-insensitive), return None
        If the user enter a valid state abbreviation, return the uppercase if the state abbreviation.
    '''
    while True:
        state = input("Would you like to find members by state? \
        \n 1. Enter a 2-digit U.S. state abbreviation to get the members representing the state\
        \n 2. Enter 'no' to return all members.\
        \n 3. Enter 'exit' to quit.\
        \n: ")
        if state.lower() == 'exit':
            print("Bye!")
            sys.exit(0)
        elif state.lower() != "no" and state.upper() not in  ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
           "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
           "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
           "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
           "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]:
           print("Please enter the correct U.S. state abbreviation.")
        else:
            if state.lower() == "no":
                state = None
            else:
                state = state.upper()
            break
    # state = random.choice(["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
    #        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
    #        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
    #        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
    #        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]) ### for auto-generating comprehensive cache
    return state 


#### SET UP THE TWEETS STALKER ####
bearer_token = secrets.TWITTER_BEARER_TOKEN
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r

def get_user_id(username):
    '''return the user's id based on the username.

    Convert the Twitter's username to their user id.

    Parameters
    ----------
    username: str
        The Twitter user's username

    Returns
    -------
    str
        The Twitter user's user id.
    '''
    endpoint = f'https://api.twitter.com/2/users/by/username/{username}'
    response = requests.get(endpoint, auth=bearer_oauth)
    user_id =  response.json()['data']['id']
    return user_id

def get_user_tweets(user_id):    
    '''return the information of the user's recent 50 tweets based on the user id.

    Parameters
    ----------
    username: str
        The Twitter user's user id

    Returns
    -------
    list of dictionaries
        A list of 50 dictinaries containing the information of the user's tweet.
    '''
    params = {'max_results': 50}
    tweet_fields = "tweet.fields=created_at,text" 
    endpoint = 'https://api.twitter.com/2/users/{}/tweets?{}'.format(user_id,tweet_fields)
    response = requests.get(endpoint, auth=bearer_oauth, params=params)
    return response.json()['data']

def format_tweets(data):
    '''return the formatted output of the "get_user_tweets(user_id)" function.

    Parameters
    ----------
    list of dictionaries
        A list of 50 dictinaries containing the information of the user's tweet.

    Returns
    -------
    1. Print out 50 lines. Each line contains the information of the user's one tweet,\
    and formatted as "[{created_time}] {text}"

    2. list: a list of 50 lines. Used for caching the data.
    '''
    code = 1
    for line in data:
        x = f"{code} [{line['created_at'][:-8]}] {line['text']}"
        print(x)
        code += 1


#### SET UP THE PROGRAM EXECUTOR
def execute():
    '''execute the program

    Users will be asked to select congressmen based on their entries of the Congress number, chamber, or state.
    Then users are allowed to pick one congressman and get their most recent 50 tweets.
    Users can also choose if they want to open the twitter page on a web browser.

    Local cache is allowed for this function.

    Parameters
    ----------
    None

    Returns
    -------
    Print out a a list of the recent 50 tweets of the selected congressman.
    Open a web browser to display the twitter page. 
    '''
    congress= congress_query()
    chamber = chamber_query()
    state = state_query()
    if state is None:
        key = str(congress)+chamber+"NO"
    else:
        key = str(congress)+chamber+state
    try:
        with open(CACHE1_FILENAME,'r') as file:
            cache_data = json.load(file)
        print("Fetching data from the local cache...")
        results = cache_data[key]
        code = 1
        member_list = []
        for result in results:
            if chamber == 'senate':
                member_list.append(Senator(json1=result))
            else:
                member_list.append(Representative(json1=result))
        for member in member_list:
            print(f"{code} {member.info()}")
            code += 1
    except:
        print("No local cache found, or no requested data in the cache. Retreiving data with API...")
        results = get_members(congress, chamber, state)
        code = 1
        member_list = []
        for result in results:
            if chamber == 'senate':
                member_list.append(Senator(json1=result))
            else:
                member_list.append(Representative(json1=result))
        if len(member_list) != 0:
            for member in member_list:
                print(f"{code} {member.info()}")
                code += 1
            get_cache_congressmen(congress, chamber, member_list, state)
        else:
            print("ERROR: No data available yet. Try another Congress or chamber")
            sys.exit(0)
    while True:
        member_code = input(f"Which congressman are you interested in? Type the number to see their recent 50 tweets, or enter 'exit' to quit: ")
        # member_code = random.randint(1,code)
        if member_code.lower() == 'exit':
            print("Bye!")
            sys.exit(0)
        else:
            try:
                member_code = int(member_code)
                account = member_list[member_code-1].twitter
                if account != "No Record":
                    try:
                        with open(CACHE2_FILENAME,'r') as file:
                            cache_data = json.load(file)
                        user_id = cache_data[account]
                        print("Fetching data from the local cache...")
                    except:
                        print("No local cache found, or no requested user in the cache. Retreiving data with API...")
                        user_id = get_user_id(account)
                        get_cache_twitter_userid(account, user_id)
                    raw_tweets = get_user_tweets(user_id)
                    formatted_tweets = format_tweets(raw_tweets)
                    print(formatted_tweets)
                else: 
                    print("Sorry, this member does not have a record of the twitter account. Bye!")
                    sys.exit(0)
                break
            except:
                print("Please retry and choose a valid option.")
    browser = input("Wanna open the twitter page on a web browser? Enter 'exit' to quit or enter anything else to browse. ")
    if browser.lower() == 'exit':
        print("Bye!")
        sys.exit(0)
    else:
        try:
            account = member_list[member_code-1].twitter
            url = f"https://twitter.com/{account}"
            webbrowser.open(url)
            print(f"Launching\n{url}\nin web browser...")
        except:
            "Ope! Something went wrong here..."

#### SET UP THE CACHE BUILDERS ####
def get_cache_congressmen(congress, chamber, memberlist, state=None):
    '''Caching the congressmen data retrieved with Congress API into a local json file

    Parameters
    ----------
    congress: int
    chamber: str
    memberlist: list
    state: None or str

    Returns
    -------
    json file

    '''
    if state:
        unique_key = str(congress)+chamber+state
    else: 
        unique_key = str(congress)+chamber+"NO"
    for member in memberlist:
        member_dict = {
            'first_name': member.first_name,
            'last_name': member.last_name,
            'short_title':member.short_title,
            'state': member.state,
            'party': member.party,
            'gender': member.gender,
            'votes_with_party_pct': member.votes_with_party,
            'twitter_account': member.twitter,
        }
        if chamber == 'senate':
            member_dict['state_rank'] = member.state_rank
        if chamber == 'house':
            member_dict['district'] = member.district
        try:
            congressmen_cache[unique_key].append(member_dict)
        except: 
            congressmen_cache[unique_key] = []
            congressmen_cache[unique_key].append(member_dict)
    with open(CACHE1_FILENAME, 'w') as file:
        json.dump(congressmen_cache, file, indent = 4)

def get_cache_twitter_userid(username, user_id):
    '''Caching the congressmen data retrieved with Congress API into a local json file

    Parameters
    ----------
    congress: int
    chamber: str
    memberlist: list
    state: None or str

    Returns
    -------
    json file

    '''
    if user_id not in ['', None,' ']:
        userid_cache[username] = user_id
    with open(CACHE2_FILENAME, 'w') as file:
        json.dump(userid_cache, file, indent = 4)





#### Finally Done! EXECUTE THE PROGRAM BELOW ####
if __name__ == "__main__":
    execute()

