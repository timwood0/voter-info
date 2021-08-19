import sys
import random
import argparse

import render
from transport import post_tweet
from urlsbystate import URLS_BY_STATE
from campaign import campaigns


def _choose_state(args):
	if args.state:
		if args.state not in URLS_BY_STATE:
			print(f"Did not recognize {args.state} in the United States.")
			return None

		state = args.state
	else:
		# Pick a random state & tweet out its voter info
		random.seed()
		idx = random.randint(0, len(URLS_BY_STATE) - 1)
		states = list(URLS_BY_STATE.keys())
		state = states[idx]

	return state


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('campaign', type=str, help='Symbolic name of campaign, e.g. 2020_presidential.')
	parser.add_argument('state', type=str, nargs='?', help='State as listed in urlsbystate.States.')
	args = parser.parse_args()

	campaign = campaigns[args.campaign]
	state = _choose_state(args)
	if not state:
		return 1

	ret_status = post_tweet(render.build_voterinfo, campaign, state)

	return ret_status


if __name__ == '__main__':
	sys.exit(main())
