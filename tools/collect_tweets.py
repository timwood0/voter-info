import time
import sys

import twitter
import keys

keys.loadKeys("./keys-livecut.xml")
api = twitter.Api(consumer_key=keys.API_KEY,
				  consumer_secret=keys.API_SECRET,
				  access_token_key=keys.ACCESS_TOKEN,
				  access_token_secret=keys.ACCESS_SECRET,
				  sleep_on_rate_limit=True)

vi_tweets = set(  # {
# 	1322341902612459520, ...
)
# Tweets: 1005
retweeters = set(#({811792770121666560, ...
)

def get_tweeps(name_a):
	a_followers = set(api.GetFollowerIDs(screen_name=name_a))
	a_following = set(api.GetFriendIDs(screen_name=name_a))
	# b_followers = set(api.GetFollowerIDs(screen_name=name_b))
	# b_following = set(api.GetFriendIDs(screen_name=name_b))
	tweeps = (a_followers & a_following)
	print(f"{name_a} followers {len(a_followers)}, {name_a} following {len(a_following)},"
		  f" tweeps {len(tweeps)}", file=sys.stderr)
	# sys.exit(0)
	return tweeps

def get_common(name_a, name_b):
	a_followers = set(api.GetFollowerIDs(screen_name=name_a))
	b_followers = set(api.GetFollowerIDs(screen_name=name_b))
	net_followers = (a_followers & b_followers)
	print(f"{name_a} followers {len(a_followers)}, {name_b} followers {len(b_followers)},"
		  f" common followers {len(net_followers)}", file=sys.stderr)
	return net_followers

# def collect_tweets():
# 	# next_res = 'q=%22Out%20of%20U.S.A.%22%20%22Vote%20by%20mail%3A%22&f=live'
# 	next_res = 'q=%22Please%20RT%20my%20voter%20info%20tweets%22&f=live'
# 	tweets = set()
# 	while next_res:
# 		search_res = api.GetSearch(raw_query=next_res, count=100, include_entities=False, return_json=True)
# 		for item in search_res['statuses']:
# 			tweets.add(item['id'])
#
# 		# Now fetch the next window
# 		if 'next_results' in search_res['search_metadata']:
# 			next_res = search_res['search_metadata']['next_results'][1:]
# 			# Stay under rate limit :(
# 			time.sleep(5)
# 		else:
# 			next_res = None
#
# 	return tweets

# if not vi_tweets:
# 	vi_tweets = collect_tweets()
#
# #print(vi_tweets)
# print(f"Tweets: {len(vi_tweets)}")
#
# # Now find who retweeted each tweet; save their ID in a set
# if not retweeters:
# 	for vi_tweet in vi_tweets:
# 		rt_set = set(api.GetRetweeters(vi_tweet))
# 		print(rt_set - retweeters)
# 		sys.stdout.flush()
# 		retweeters |= rt_set
# 		time.sleep(12.1)


# Compute our set of tweeps
ttc_followers = set(api.GetFollowerIDs(screen_name='tweetstocities'))
# sys.exit(0)
get_tweeps('livecut')
get_tweeps('balkingpoints')
net_followers = get_common('livecut', 'balkingpoints') - ttc_followers
print(f"net of ttc {len(net_followers)}", file=sys.stderr)
# sys.exit(0)

# # Subtract retweeters from the tweeps to get non-retweeters
# non_retweeters = tweeps - retweeters
#
# print(non_retweeters)
# print(f"Non-retweeters: {len(non_retweeters)}")

# Find locations/places of tweeps, if any XXX No, need to parse profile
# tweeps_at = 0
# for tweep in tweeps:
#     try:
#         tweet = ct.api.GetUserTimeline(user_id=tweep, count=1, trim_user=True)[0]
#     except IndexError:
#         continue

# Find non-back-followers
# non_tweeps = following - tweeps
# for non_tweep in non_tweeps:
# 	user = api.GetUser(non_tweep)
# 	if not user:
# 		continue
# 	print(f"{non_tweep}|{user.screen_name}|{user.description}")

# Clean up non-tweeps: list of IDs from stdin
# for line in sys.stdin:
# 	non_tweep = int(line[:-1])
# 	result = api.DestroyFriendship(non_tweep)
# 	if result:
# 		print(f"Deleted {non_tweep}.")
# 	else:
# 		print(f"Failed to delete {non_tweep}.")

for tweep in net_followers:
	user = api.GetUser(tweep)
	if not user:
		print("Rate limited.", sys.stderr)
		time.sleep(2.0)
		continue
	# print(f"{tweep}|{user.screen_name}|{user.location}|{user.description}")
	print(f"{tweep}|{user.screen_name}")
