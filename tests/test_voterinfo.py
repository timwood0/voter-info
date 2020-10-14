import unittest
import mock
import sys
import os
import importlib

import voterinfo, socialize
from render import *
from urlsbystate import URLS_BY_STATE


MY_TWITTER_UID = 16230307


class TestVoterInfo(unittest.TestCase):
	def tearDown(self):
		importlib.reload(socialize)
		importlib.reload(voterinfo)

	@mock.patch("transport.post_tweet")
	def test_voterinfo_main(self, mock_post):
		mock_post.return_value = 0
		importlib.reload(voterinfo)
		arg0 = sys.argv[0]
		sys.argv = [arg0, 'Puerto Rico']
		self.assertEqual(voterinfo.main(), 0)

		sys.argv = [arg0, 'Arcadier']
		self.assertEqual(voterinfo.main(), 1)

		sys.argv = [arg0]
		self.assertEqual(voterinfo.main(), 0)
		# XXX Set & check a fake JSON return value for _mock_api.return_value.PostUpdate.return_value

	def test_hashtag(self):
		self.assertEqual(hashtag("North Dakota"), "#NorthDakota")
		self.assertEqual(hashtag("RI", True), "#RI")
		self.assertEqual(hashtag("dc"), "#Dc")
		self.assertEqual(hashtag("dc", True), "#dc")
		self.assertEqual(hashtag("wyoming"), "#Wyoming")
		self.assertEqual(hashtag("District of Columbia"), "#DistrictOfColumbia")
		self.assertEqual(hashtag("Oregon"), "#Oregon")

	def test_urls_by_state(self):
		def _present(field):
			self.assertTrue(field in state_info, f"{field} missing from {state}")

		for state, state_info in URLS_BY_STATE.items():
			print(state_info['abs'], state_info['regdl'])
			cities = state_info['cities']
			print(hashtag(state_info['code'], plain=True))
			for city in cities:
				print(hashtag(city))

			_present("reg")
			_present("regdl")
			_present("abs")
			_present("polls")
			_present("cities")

	def test_build_voterinfo(self):
		random.seed(0)
		for state in ("California", "Idaho", "West Virginia", "Puerto Rico", "Guam"):
			effective_len, tweet = build_voterinfo(state)
			print(effective_len, tweet)
			assert len(tweet) > 0  # XXX This could flap

		self.assertRaises(KeyError, build_voterinfo, ("Arcadia",))

	@mock.patch("twitter.Api.GetFollowerIDs")
	@mock.patch("twitter.Api.GetFriendIDs")
	@mock.patch("transport.post_tweet")
	def test_socialize_main(self, mock_post, mock_friends, mock_followers):
		mock_post.return_value = 0
		importlib.reload(socialize)
		bs_fn = build_socialize
		mock_followers.return_value \
			= (157815060, 1230281, 13027572, 155295889, 26825139, 153942024, 153934792)
		mock_friends.return_value \
			= (26825139, 13027572, 823171093854912516, 54885400, 153942024)
		socialize.main()
		mock_post.assert_has_calls([mock.call(bs_fn, 13027572), mock.call(bs_fn, 153942024), mock.call(bs_fn, 26825139)],
									 any_order=True)

	def test_build_socialize(self):
		effective_length, tweet_text = build_socialize(MY_TWITTER_UID)
		print(effective_length)
		print(tweet_text)

	def test_process_do_not_call(self):
		dnc = open(os.path.join(sys.path[0], "do_not_call.txt"))
		line_ct = 0
		for line in dnc.readlines():
			line_ct += 1
		dnc.close()

		# Requires no duplicates in DNC list
		self.assertEqual(len(socialize.process_do_not_call()), line_ct)


if __name__ == '__main__':
	unittest.main()
