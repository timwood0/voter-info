import sys

import tweepy

import keys


"""Post a single message to Twitter via the API."""
keys.loadKeys("./keys.xml")
api = tweepy.Client(consumer_key=keys.API_KEY,
				consumer_secret=keys.API_SECRET,
				bearer_token=keys.BEARER_TOKEN,
				access_token=keys.ACCESS_TOKEN,
				access_token_secret=keys.ACCESS_SECRET)


def post_tweet(post_func, *post_args):
	ret_status = 0

	effective_len, tweet_text = post_func(*post_args)

	if tweet_text:
		print(effective_len, tweet_text, file=sys.stderr)
		try:
			post_result = api.create_tweet(text=tweet_text)
			print(post_result, file=sys.stderr)
		except tweepy.errors.TweepyException as e:
			print(f"Failed to send tweet: {str(e)}", file=sys.stderr)
			ret_status = 1
	else:
		print("Error: Failed to generate tweet (most likely exceeded size limit).")
		ret_status = 1

	return ret_status
