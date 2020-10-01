import re
import random
import twitter

from urlsbystate import URLS_BY_STATE

TWITTER_SHORT_URL_LENGTH = len('https://t.co/XXXXXXXXXX?amp=1')  # XXX By observation only.


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


def build_tweet(state):
	"""Render a tweet of voting info for a state"""
	state_info = URLS_BY_STATE[state]
	num_cities = len(state_info['cities'])
	city_ct = random.randint(1, 3)
	effective_length = 0
	tweet_text = ""

	while city_ct > 0:
		# Iterate on building a tweet until it fits within the limit.
		# Return none if unsuccessful
		city_set = set(state_info['cities'])
		try:
			# Select up to city_ct cities
			cities = []
			for i in range(0, city_ct):
				city_idx = random.randint(0, num_cities - 1)
				city = state_info['cities'][city_idx]
				if city in city_set:
					cities.append(hashtag(city))
					city_set.remove(city)

			effective_length, tweet_text = render_tweet(cities, state, state_info)
			break
		except AssertionError:
			tweet_text = ""
			city_ct -= 1

	return effective_length, tweet_text


def render_tweet(cities, state, state_info):
	tweet_text = f"""
				{hashtag(state)} {hashtag(state_info['code'], True)} {hashtag('vote')}
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
