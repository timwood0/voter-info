# voter-info
Simple app. to automate tweeting of voting resources for the U.S. 2020 election.

## Synopses:

Voter info facet:
`python voterinfo.py campaign [["]U.S.-state-or-territory-specifier["]]`

Socialize facet:
`python socialize.py [-l limit] campaign [tweep]`

Driver:
`./tweet_vi [-q number-of-tweets(min 4)] [-w time-period(max 86400 sec)] [-b base-interval(default 600)] { [-S tweep_file] | [-s state] } campaign`

Run tests:
`pytest`

This tool contains two main facets, or executable entry-points, one to tweet voter info by U.S. states and territories,
the other to tweet mutual followers asking them to search up and retweet the voter-info tweets.  It includes a
driver script, `tweet_vi`, to automate tweeting to many states, or repeatedly to a single state, or to mutual followers,
or to a list of users.

The `campaign` argument refers to configurations of campaign-specific data found in `campaigns.xml` in the top-level
directory, a resource file you create.  You can use `campaigns-template.xml` as a guideline to the configuration schema.

`voterinfo.py` by default issues a tweet on Twitter containing
links to on-line resources for voters for a single random U.S. state or territory.
The optional argument causes issuance of a general tweet with that information for the given state or territory.
States and territories are spelled as their official proper names (capitalized words separated by spaces).

`socialize.py` by default issues a tweet on Twitter to each of the user's mutual followers that asks each follower
to search and retweet voter-info tweets, or to a single user if given.  If a user appears in
the `do_not_call.txt` file, that user is not sent a tweet.  Per Twitter rules, Twitter automated apps ("bots") may
not @-mention a user without prior contact from that user; `socialize.py` will not tweet a user unless the username appears
in the `opt_in.txt` file.  The `-l` argument limits the number of tweets to the given number of mutual followers, randomly-chosen.
This facet outputs a header line with the user's follower and following counts, the count of mutual followers,
and the number of remaining mutual followers in `opt_in.txt` and not in `do_not_call.txt`.  It then outputs a line
with each follower's name that it sends a tweet.  Currently, you must manually maintain `opt_in.txt` and
`do_not_call.txt` to track opt-ins and opt-outs.

## Configuration

### Credentials

This tool currently requires the user to have a Twitter developer account.
The `keys.py` file requires a `keys.xml` file in the top-level directory with the structure
```
<credentials>
  <twitterCredentials>
    <apiKey>...
    <apiSecret>...
    <bearerToken>...
    <accessToken>...
    <accessSecret>...
  </twitterCredentials>
</credentials>
```
with the _consumer keys_ and _access tokens_ for the developer account under
whose user ID the tweets will be posted. The user of the package must set the element contents in `keys.xml`
to valid values issued by Twitter.

The script will exit with non-zero status if it cannot compose a tweet in its standard format
that fits within Twitter's length limit for a tweet.  This is a rare occurrence, only happening when
`voterinfo.py` cannot include at least one city in the state or territory in the tweet without exceeding the limit.

### Campaigns - Meta-Programming

Recent changes have moved the definitions of campaigns out of Python code and into a resource file, `campaigns.xml`.
The program loads the campaign definitions from this file at startup.

The included `campaigns-template.xml` contains elaborate examples of single- and multi-state campaign definitions.  Note the
contents of the `<entry>` elements.  `<entry>` element CDATA contains a list of Python formatted-string arguments passed
verbatim to the `campaign.tweet_entry()` function to render data and other content conveniently.  Python symbolic references
within these CDATA blocks must be visible to `campaign.tweet_entry()` at runtime.  Also note, before you can run
the tests successfully, you should first rename or make a copy of any existing `campaigns.xml`, then symlink
`campaigns.xml` to `campaigns-template.xml`.

## Requirements
- Python >=3.6
- Pytest >=3.3.2
- Virtualenv >=15.1.0
- See `requirements.txt`

## License
   Copyright 2020-21, Timothy E. Wood

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a [copy of the License online](http://www.apache.org/licenses/LICENSE-2.0).

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

## Acknowledgements
Thanks are due [voteamerica.com](https://voteamerica.com) for their carefully-assembled
pages of state-by-state voter resources, which facilitated building this tool; also to Twitter:@balkingpoints for
developing the tweets-to-cities targeting strategy.
