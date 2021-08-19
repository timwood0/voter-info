# voter-info
Simple app. to automate tweeting of voting resources for the U.S. 2020 election.

Synopses:

Voter info facet:
`python voterinfo.py campaign [["]U.S.-state-or-territory-specifier["]]`

Socialize facet:
`python socialize.py [-l limit] campaign [tweep]`

Driver:
`./tweet_vi [-h] [-s state] [-q number-of-tweets] [-w time-period(max 86400 sec.)] campaign`

This tool contains two main facets, or executable entry-points, one to tweet voter info by U.S. states and territories,
the other to tweet mutual followers asking them to search up and retweet the voter-info tweets.  It includes a
driver script, `tweet_vi`, to automate tweeting to many states, or repeatedly to a single state.

The `campaign` argument refers to configurations of campaign-specific data, found in `campaign.campaigns`.
Planned work will move the campaign configurations out of the code and into resource files.

`voterinfo.py` by default issues a tweet on Twitter containing
links to on-line resources for voters for a single random U.S. state or territory.
The optional argument causes issuance of a tweet with that information for the given state or territory.
States and territories are spelled as their official proper names (capitalized words separated by spaces).

`socialize.py` by default issues a tweet on Twitter to each of the user's mutual followers that asks each follower
to search and retweet voter-info tweets, or to a single mutual follower if given.  If a mutual follower appears in
the `do_not_call.txt` file, that follower is not sent a tweet.  With no arguments, `socialize.py` tweets all mutual
followers.  The `-l` argument limits the number of tweets to the given number of mutual followers, randomly-chosen.
This facet outputs a header line with the user's follower and following counts, the count of mutual followers,
and the number of remaining mutuals not in `do_not_call.txt`.  It then outputs a line with each follower's name
that it send a tweet.  Currently, you must manually maintain `do_not_call.txt` with the names of mutual followers
already tweeted (see output for recipients), if you want to prevent duplicate tweeting.

This tool currently requires the user to have a Twitter developer account.
The `keys.py` file must contain the _consumer keys_ and _access tokens_ for the developer account under
whose user ID the tweets will be posted. The user of the script must set the variables in `keys.py`
to valid values issued by Twitter.

The script will exit with non-zero status if it cannot compose a tweet in its standard format
that fits within Twitter's length limit for a tweet.  This is a rare occurrence, only happening when
`voterinfo.py` cannot include at least one city in the state or territory in the tweet without exceeding the limit.

Acknowledgement and thanks are due [voteamerica.com](https://voteamerica.com) for their carefully-assembled
pages of state-by-state voter resources, which facilitated building this tool; also to Twitter:@balkingpoints for
developing the tweets-to-cities targeting strategy.

Requirements:  
- Python >=3.6
- Virtualenv >=15.1.0
- See `requirements.txt`

License:
   Copyright 2020-21, Timothy E. Wood

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
