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
	parser.add_argument('-l', '--limit', dest='limit', type=int, default=0,
						help="Max number of tweets (in community mode.)")
	parser.add_argument('campaign', type=str, help='Symbolic name of campaign, e.g. 2020_presidential.')
	arg_group = parser.add_mutually_exclusive_group()
	arg_group.add_argument('-i', '--id', dest='user_id', type=int, default=0,
						   help="A Twitter user ID, overrides tweep.")
	arg_group.add_argument('tweep', type=str, nargs='?', help="Name of a Twitter user."
						   "  If missing, tweet to community of mutual followers.")
	args = parser.parse_args()

	campaign = campaigns[args.campaign]
	user_id = 0
	if args.tweep:
		# Tweet an individual
		user_id = api.get_user(username=args.tweep).data.id

	if args.user_id:
		# Tweet to ID overrides name
		user_id = args.user_id

	if user_id:
		# Ensure user not opted-out
		if (user_id not in process_do_not_call()) and (user_id in process_opt_in()):
			ret_status = post_tweet(render.build_socialize, campaign, user_id)
			if campaign.FOLLOW in campaign.campaign_info:
				res = api.follow_user(user_id)
				if 'following' not in res.data or not res.data['following']:
					print(f"Warning: Failed to follow {user_id}.")
	else:
		# Tweet our tweeps
		followers = set(api.get_users_followers())
		following = set(api.get_users_following())
		tweeps = (followers & following)
		len_tweeps = len(tweeps)

		tweeps -= process_do_not_call()
		tweeps = tweeps & process_opt_in()

		# Post to the community
		count = 0
		print(f"Limit: {args.limit}, Followers: {len(followers)}, Following: {len(following)}, "
			  f"Tweeps: {len_tweeps}, Tweeps - DNC: {len(tweeps)}")
		for user_id in tweeps:
			ret_status = post_tweet(render.build_socialize, campaign, user_id)
			if campaign.FOLLOW in campaign.campaign_info:
				res = api.follow_user(user_id)
				if 'following' not in res.data or not res.data['following']:
					print(f"Warning: Failed to follow {user_id}.")
			count += 1
			print(f'Count: {count}', file=sys.stderr)
			if count == args.limit:
				break

	return ret_status


# Return a list of users who have opted in to @-mentions, a Twitter requirement.
def process_opt_in():
	return process_opt_list("opt_in.txt")


# Return a list of users IDs who have opted out of contact
def process_do_not_call():
	return process_opt_list("do_not_call.txt")


# Look up user IDs for a usernames in a file, return the user IDs in a set.
def process_opt_list(opt_file):
	opt_fd = open(os.path.join(sys.path[0], opt_file))
	opt_tweeps = set()
	opt_names = list()
	line_ct = 0
	for line in opt_fd.readlines():
		opt_names.append(line[:-1])
		line_ct += 1
		if line_ct == 100:
			# Limit of 100 names to look up at once
			resp = api.get_users(usernames=opt_names)
			opt_tweeps.update(u.id for u in resp.data)
			opt_names = list()
			line_ct = 0

	if line_ct > 0:
		resp = api.get_users(usernames=opt_names)
		opt_tweeps.update(u.id for u in resp.data)

	opt_fd.close()
	return opt_tweeps


if __name__ == '__main__':
	sys.exit(main())
