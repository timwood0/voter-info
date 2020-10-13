import twitter

import keys


"""Post a single message to Twitter via the API."""
api = twitter.Api(consumer_key=keys.API_KEY,
				  consumer_secret=keys.API_SECRET,
				  access_token_key=keys.ACCESS_TOKEN,
				  access_token_secret=keys.ACCESS_SECRET)


def post_tweet(post_func, *post_args):
	ret_status = 0

	effective_len, tweet_text = post_func(*post_args)

	if tweet_text:
		print(effective_len, tweet_text)
		post_result = api.PostUpdate(tweet_text)
		print(post_result)
	else:
		print("Error: Failed to generate tweet (most likely exceeded size limit).")
		ret_status = 1

	return ret_status
