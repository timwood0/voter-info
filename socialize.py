import sys
import os
import argparse

import render
from transport import api, post_tweet


def main():
	"""Walk my list of followers, tweet each with a suggestion to search my Voterinfo tweets and retweet them."""
	ret_status = 0

	parser = argparse.ArgumentParser()
	parser.add_argument('tweep', type=str, nargs='?')
	args = parser.parse_args()

	if args.tweep:
		# Tweet an individual (ignoring DNC)
		user_id = api.GetUser(screen_name=args.tweep).id
		ret_status = post_tweet(render.build_socialize, user_id)
	else:
		# Tweet our tweeps
		followers = set(api.GetFollowerIDs())
		following = set(api.GetFriendIDs())
		tweeps = (followers & following)

		tweeps = process_do_not_call(tweeps)

		# Post to the community
		for user_id in tweeps:
			ret_status = post_tweet(render.build_socialize, user_id)

	return ret_status


def process_do_not_call(tweeps):
	# Take away names on the DNC list
	dnc = open(os.path.join(sys.path[0], "do_not_call.txt"))
	dnc_names = list()
	line_ct = 0
	for line in dnc.readlines():
		dnc_names.append(line[:-1])
		line_ct += 1
		if line_ct == 100:
			# Limit of 100 names to look up at once
			ul = api.UsersLookup(screen_name=dnc_names)
			tweeps -= set([u.id for u in ul])
			dnc_names = list()
			line_ct = 0

	if line_ct > 0:
		ul = api.UsersLookup(screen_name=dnc_names)
		tweeps -= set([u.id for u in ul])

	dnc.close()
	return tweeps


if __name__ == '__main__':
	sys.exit(main())
