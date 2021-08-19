import re
import random
import twitter

from urlsbystate import URLS_BY_STATE
from transport import api

TWITTER_SHORT_URL_LENGTH = len('https://t.co/XXXXXXXXXX?amp=1')  # XXX By observation only.
VOTERINFO_SEARCH_URL = "https://twitter.com/search?q=%22Out%20of%20U.S.A.%22%20%22Vote%20by%20mail%3A%22&f=live"


def hashtag(phrase, plain=False):
	"""
	Generate hashtags from phrases.  Camelcase the resulting hashtag, strip punct.
	Allow suppression of style changes, e.g. for two-letter state codes.
	"""
	words = phrase.split(' ')
	if not plain:
		for i in range(len(words)):
			try:
				if not words[i]:
					del words[i]
				words[i] = words[i][0].upper() + words[i][1:]
				words[i] = re.sub(r"['./-]", "", words[i])
			except IndexError:
				break
	return '#' + ''.join(words)


def build_voterinfo(state):
	"""Render a tweet of voting info for a state"""
	state_info = URLS_BY_STATE[state]
	num_cities = len(state_info['cities'])
	city_ct = num_cities
	effective_length = 0
	tweet_text = ""

	while city_ct > 0:
		# Iterate on building a tweet until it fits within the limit.
		# Return none if unsuccessful
		city_set = set(state_info['cities'])
		try:
			# Select up to city_ct cities
			cities = []
			cities_found = 0
			while cities_found < city_ct:
				city_idx = random.randint(0, num_cities - 1)
				city = state_info['cities'][city_idx]
				if city in city_set:
					cities.append(hashtag(city))
					city_set.remove(city)
					cities_found += 1

			effective_length, tweet_text = render_voterinfo(cities, state)
			break
		except AssertionError:
			tweet_text = ""
			city_ct -= 1

	return effective_length, tweet_text


def render_voterinfo(cities, state):
	state_info = URLS_BY_STATE[state]

	# XXX Tweet text should go in external files and be selectable.  Interface back to code?
	tweet_text = f"""
		{hashtag(state)} {hashtag(state_info['code'], True)} {hashtag(state_info.get('vote', 'vote'))}
		{' '.join(cities)}
		Reg. deadline: {state_info['regdl']}
		Check registration: {state_info['reg']}
		Polling places: {state_info['polls']}
		Out of U.S.A.: {state_info['abroad']}
		Vote by mail: {state_info['abs']}
	"""

	# Clean up multi-line string
	tweet_text = re.sub('\t', '', tweet_text)

	# Now try to guess the length of the resulting tweet.  Twitter imposes the
	# length limit after it shortens the links.
	effective_length = (len(tweet_text)
		- len(state_info['regdl']) - len(state_info['reg'])
		- len(state_info['polls']) - len(state_info['abs'])
		- len(state_info['abroad'])
		+ 5 * TWITTER_SHORT_URL_LENGTH)
	assert effective_length <= twitter.api.CHARACTER_LIMIT
	return effective_length, tweet_text


def build_socialize(user_id):
	# Build a tweet asking for retweets
	try:
		screen_name = api.GetUser(user_id).screen_name
		print(f"Socialize: {screen_name}")
	except twitter.error.TwitterError:
		print(f"Twitter user {user_id} not found.")
		return 0, ""

	tweet_text = f"""
		@{screen_name}
		Hi, we follow each other on Twitter.
		Please RT my voter info tweets to help get out the vote!
		1. Search my tweets: {VOTERINFO_SEARCH_URL}
		2. Find a tweet for a state in the list, e.g., #Iowa or #NC.
		3. Retweet it.

		Thanks, and be sure to #vote!
	"""

	# Clean up multi-line string
	tweet_text = re.sub('\t', '', tweet_text)

	# Now try to guess the length of the resulting tweet.  Twitter imposes the
	# length limit after it shortens the links.
	effective_length = (len(tweet_text)
						- len(VOTERINFO_SEARCH_URL)
						+ TWITTER_SHORT_URL_LENGTH)
	# print(effective_length, tweet_text)
	assert effective_length <= twitter.api.CHARACTER_LIMIT
	return effective_length, tweet_text


def shell_string(chars):
	if ' ' in chars:
		# Ensure shell keeps words in a string
		return f'"{chars}" '
	else:
		return f'{chars} '


# For bot-driver script
def all_states():
	for state in URLS_BY_STATE.keys():
		print(shell_string(state))

# For bot-driver script
def all_cities(state):
	for city in URLS_BY_STATE[state]['cities']:
		print(shell_string(city))
