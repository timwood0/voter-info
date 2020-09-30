# voter-info
Simple app. to automate tweeting of voting resources for the U.S. 2020 election.

Synopsis:
`python voterinfo.py [["]U.S.-state-or-territory-specifier["]]`

`voterinfo.py` by default issues a tweet on Twitter containing
links to on-line resources for voters for a single random U.S. state or territory.
The optional argument causes issuance of a tweet with that information for the given state or territory.
States and territories are spelled as their official proper names (capitalized words separated by spaces).

This tool currently requires the user to have a Twitter developer account.
The `keys.py` file must contain the _consumer keys_ and _access tokens_ for the developer account under
whose user ID the tweets will be posted. The user of the script must set the variables in `keys.py`
to valid values issued by Twitter.

The script will exit with non-zero status if it cannot compose a tweet in its standard format
that fits within Twitter's length limit for a tweet.  This is a rare occurrence, only happening when
`voterinfo.py` cannot include at least one city in the state or territory in the tweet without exceeding the limit.

Acknowledgement and thanks are due [vote.org](https://vote.org) for their carefully-assembled pages of state-by-state
voter resources, which facilitated building this tool.
