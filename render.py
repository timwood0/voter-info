import re
import random
import twitter

from urlsbystate import URLS_BY_STATE, CITIES
from transport import api

TWITTER_SHORT_URL_LENGTH = len('https://t.co/XXXXXXXXXX?amp=1')  # XXX By observation only.
CHARACTER_LIMIT = 280  # XXX Can't find a constant in tweepy.Client

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


def build_voterinfo(campaign, state_name):
	"""Render a tweet of voting info for a state"""
	state = campaign.info_by_state[state_name]
	num_cities = len(state[CITIES])
	assert num_cities == len(set(state[CITIES])), f"Duplicate entries in CITIES for {state_name}."

	city_ct = 0
	effective_length = 0
	tweet_text = ""
	while city_ct < num_cities:
		# Iterate on building a tweet until it fits within the limit.
		# Return none if unsuccessful
		city_set = set(state[CITIES])
		try:
			# Select up to city_ct cities
			cities = []
			cities_found = 0
			while cities_found < city_ct:
				city_idx = select_city(campaign, state, num_cities)
				city = state[CITIES][city_idx]
				if city in city_set:
					cities.append(hashtag(city))
					city_set.remove(city)
					cities_found += 1

			effective_length, tweet_text = render_voterinfo(campaign, state_name, cities)
			city_ct += 1
		except AssertionError:
			# The last-returned tweet_text is at "max" capacity
			break

	return effective_length, tweet_text


def select_city(campaign, state_info, num_cities):
	# Simple function to pick a random index into the list of cities based on normal distribution of indexes.
	if campaign.CITIES_DISTRO in state_info:
		city_idx = (num_cities >> 1) + int(round(random.gauss(0.0, state_info[campaign.CITIES_DISTRO] * num_cities)))
		city_idx = min(max(0, city_idx), num_cities - 1)
	else:
		city_idx = random.randint(0, num_cities - 1)
	# print(f"city_idx: {city_idx}")

	return city_idx


def render_tweet(tweet: list):
	return '\n'.join(tweet[2:]) if tweet else ""


def render_voterinfo(campaign, state_name, cities):

	tweet = campaign.build_tweet(state=state_name, cities=cities)
	tweet_text = render_tweet(tweet)

	# Now try to guess the length of the resulting tweet.  Twitter imposes the
	# length limit after it shortens the links.
	effective_length = len(tweet_text) - tweet[0] + tweet[1] * TWITTER_SHORT_URL_LENGTH if tweet else 0
	assert effective_length <= twitter.api.CHARACTER_LIMIT
	return effective_length, tweet_text


def build_socialize(campaign, user_id):
	# Build a tweet asking for retweets
	try:
		screen_name = api.get_user(id=user_id).data.username
		print(f"Socialize: {screen_name}")
	except twitter.error.TwitterError:
		print(f"Twitter user {user_id} not found.")
		return 0, ""

	tweet = campaign.build_tweet(screen_name=screen_name)
	tweet_text = render_tweet(tweet)

	# Now try to guess the length of the resulting tweet.  Twitter imposes the
	# length limit after it shortens the links.
	effective_length = len(tweet_text) - tweet[0] + tweet[1] * TWITTER_SHORT_URL_LENGTH if tweet else 0
	# print(effective_length, tweet_text)
	assert effective_length <= CHARACTER_LIMIT
	return effective_length, tweet_text


def shell_string(chars):
	if ' ' in chars:
		# Ensure shell keeps words in a string
		return f'"{chars}" '
	else:
		return f'{chars} '


# For bot-driver script
def all_states(campaign=None):
	if campaign is None:
		keys = URLS_BY_STATE.keys()
	else:
		keys = campaign.info_by_state.keys()

	for state in keys:
		print(shell_string(state))

# For bot-driver script
def all_cities(campaign, state):
	for city in campaign.info_by_state[state][CITIES]:
		print(shell_string(city))
