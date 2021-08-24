import sys
import os
import argparse

import render
from campaign import campaigns
from transport import api, post_tweet


def main():
	"""Walk my list of followers, tweet each with a suggestion to search my Voterinfo tweets and retweet them."""
	ret_status = 0

	parser = argparse.ArgumentParser()
	parser.add_argument('-l', '--limit', dest='limit', type=int, default=0)
	parser.add_argument('campaign', type=str, help='Symbolic name of campaign, e.g. 2020_presidential.')
	arg_group = parser.add_mutually_exclusive_group()
	arg_group.add_argument('-i', '--id', dest='user_id', type=int, default=0)
	arg_group.add_argument('tweep', type=str, nargs='?', help="Name of a Twitter user.")
	args = parser.parse_args()

	campaign = campaigns[args.campaign]
	user_id = 0
	if args.tweep:
		# Tweet an individual (ignoring DNC)
		user_id = api.GetUser(screen_name=args.tweep).id

	if args.user_id:
		user_id = args.user_id

	if user_id:
		# Ensure user not opted-out
		if ({user_id} - process_do_not_call()):
			ret_status = post_tweet(render.build_socialize, campaign, user_id)
	else:
		# Tweet our tweeps
		followers = set(api.GetFollowerIDs())
		following = set(api.GetFriendIDs())
		tweeps = (followers & following)
		len_tweeps = len(tweeps)

		tweeps -= process_do_not_call()

		# Post to the community
		count = 0
		print(f"Limit: {args.limit}, Followers: {len(followers)}, Following: {len(following)}, "
			  f"Tweeps: {len_tweeps}, Tweeps - DNC: {len(tweeps)}")
		for user_id in tweeps:
			ret_status = post_tweet(render.build_socialize, campaign, user_id)
			count += 1
			print(f'Count: {count}', file=sys.stderr)
			if count == args.limit:
				break

	return ret_status


def process_do_not_call():
	# Take away names on the DNC list
	dnc = open(os.path.join(sys.path[0], "do_not_call.txt"))
	dnc_tweeps = set()
	dnc_names = list()
	line_ct = 0
	for line in dnc.readlines():
		dnc_names.append(line[:-1])
		line_ct += 1
		if line_ct == 100:
			# Limit of 100 names to look up at once
			ul = api.UsersLookup(screen_name=dnc_names)
			dnc_tweeps.update(u.id for u in ul)
			dnc_names = list()
			line_ct = 0

	if line_ct > 0:
		ul = api.UsersLookup(screen_name=dnc_names)
		dnc_tweeps.update(u.id for u in ul)

	dnc.close()
	return dnc_tweeps


if __name__ == '__main__':
	sys.exit(main())
