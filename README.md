# Fall 2022 SI507 Final Project - Yunong Xue
## Indroduction
This project built an interactive command-line-based tool that allows users to retrieve the recent tweets of U.S. Congressmen of their interests. The users are first prompted to enter a Congress number, chamber, and state (optional) to get a list of Congress members affiliated with their selections. Returned congressman information comprises name, state, title, party, gender, the percentage they voted with the party, state rank (Senators only), and district (Representatives only). Then the users are allowed to pick one member to fetch their most recent 50 tweets structured as "[sending time] text" and given the option to open the member's Twitter page on a web browser.
## Data Sources
1. Congress members data: ProPublica Congress API    
https://projects.propublica.org/api-docs/congress-api/members/
2. Tweets data: Twitter API v2   
https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/api-reference/get-users-id-tweets
## Getting Started
#### 1. Required Python Packages:
```
$ pip install requests
```
#### 2. Apply for API Keys and Authorizations
 1) Get an API key for Congress data: https://projects.propublica.org/api-docs/congress-api/
 2) Get authorization packages for tweets data: https://developer.twitter.com/en/docs/twitter-api
 3) Store the Congress API key and twitter bearer token in a python file names "secrets.py"
```
PROPUBLICA_API_KEY = {your own API key here}
TWITTER_BEARER_TOKEN = {your own token here} 
```
#### 3. Running the program
```
$ python congressmen.py
```
## Interactions
The users will be prompted to enter a Congress number, chamber, and state respectively to get the information of congress members of their choice. Then the users can enter a number shown on the screen to get a specific member's most recent 50 tweets. Finally, the users can choose whether to open the member's Twitter page on a web browser.

Specific interactions are as below:
#### 1. Please enter a Congress number of your interests [(114-117) available], or enter 'exit' to quit: 

User entry options: [114, 115, 116, 117, 'exit' ]
(The entry is not case-sensitive)

#### 2. Which chamber are you looking for? Enter 'senate' or 'house', or enter 'exit' to quit: 

User entry options: ['senate', 'house', 'exit' ]
(The entry is not case-sensitive)

#### 3. Would you like to find members by state? 
- 1. Enter a 2-digit U.S. state abbreviation to get the members representing the state   
- 2. Enter 'no' to return all members   
- 3. Enter 'exit' to quit  

User entry options: ["no", "exit", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
(The entry is not case-sensitive)

#### 4. Which congressman are you interested in? Type the number to see their recent 50 tweets, or enter 'exit' to quit: 

User entry options: 1. An integer representing a Congress member shown on the screen. 2. 'exit'
(The number of integer options is up to the user's previous entries.)

#### 5. Wanna open the Twitter page on a web browser? Enter 'exit' to quit or enter anything else to browse. 

User entry options: 1. 'exit' 2. Anything else
