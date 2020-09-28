import sys
import random

import twitter

import keys
import render
from urlsbystate import URLS_BY_STATE


def main():
	"""Post a single message to Twitter via the API."""
	api = twitter.Api(consumer_key=keys.API_KEY,
					  consumer_secret=keys.API_SECRET,
					  access_token_key=keys.ACCESS_TOKEN,
					  access_token_secret=keys.ACCESS_SECRET)

	# status = api.PostUpdate('I love python-twitter!')
	# print(status.text)
	ret_status = 0

	# Pick a random state & tweet out its voter info
	random.seed()
	idx = random.randint(0, len(URLS_BY_STATE) - 1)
	states = list(URLS_BY_STATE.keys())
	state = states[idx]
	effective_len, tweet_text = render.build_tweet(state)

	if tweet_text:
		print(effective_len, tweet_text)
		post_result = api.PostUpdate(tweet_text)
		print(post_result)
	else:
		print("Error: Failed to generate tweet (most likely exceeded size limit).")
		ret_status = 1

	return ret_status


if __name__ == '__main__':
	sys.exit(main())
