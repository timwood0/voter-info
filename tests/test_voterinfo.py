import unittest
import mock
import random

import voterinfo
from render import hashtag, build_tweet
from urlsbystate import URLS_BY_STATE



class TestVoterInfo(unittest.TestCase):
	@mock.patch("twitter.Api", autospec=True)
	def test_main(self, _mock_api):
		voterinfo.main()
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

	# @mock.patch("twitter.Api", autospec=True)
	def test_build_tweet(self):
		random.seed(0)
		for state in ("California", "Idaho", "West Virginia"):
			effective_len, tweet = build_tweet(state)
			print(effective_len, tweet)
			assert len(tweet) > 0  # XXX This could flap

		self.assertRaises(KeyError, build_tweet, ("Arcadia",))


if __name__ == '__main__':
	unittest.main()
