import unittest
import mock
import sys
import os
import importlib

from twitter.models import User

import voterinfo, socialize
from render import *
from urlsbystate import URLS_BY_STATE, CODE, CITIES, REGDL, REG, POLLS, ABS
from campaign import campaigns


MY_TWITTER_UID = 16230307


class TestVoterInfo(unittest.TestCase):
	def tearDown(self):
		importlib.reload(socialize)
		importlib.reload(voterinfo)

	@mock.patch("transport.post_tweet")
	def test_01voterinfo_main(self, mock_post):
		mock_post.return_value = 0
		importlib.reload(voterinfo)
		arg0 = sys.argv[0]
		sys.argv = [arg0, '2020_presidential', 'Puerto Rico']
		self.assertEqual(voterinfo.main(), 0)

		sys.argv = [arg0, '2020_presidential', 'Arcadier']
		self.assertEqual(voterinfo.main(), 1)

		sys.argv = [arg0]
		with mock.patch("argparse.ArgumentParser.exit", side_effect=IndexError):
			self.assertRaises(IndexError, voterinfo.main)

		sys.argv = [arg0, '2021_georgia_runoff']
		self.assertEqual(voterinfo.main(), 0)
		# XXX Set & check a fake JSON return value for _mock_api.return_value.PostUpdate.return_value

		# MUST come last
		sys.argv = [arg0]

	def test_02hashtag(self):
		self.assertEqual(hashtag("North Dakota"), "#NorthDakota")
		self.assertEqual(hashtag("RI", True), "#RI")
		self.assertEqual(hashtag("dc"), "#Dc")
		self.assertEqual(hashtag("dc", True), "#dc")
		self.assertEqual(hashtag("wyoming"), "#Wyoming")
		self.assertEqual(hashtag("District of Columbia"), "#DistrictOfColumbia")
		self.assertEqual(hashtag("Oregon"), "#Oregon")

	def test_03urls_by_state(self):
		def _present(field):
			self.assertTrue(field in state_info, f"{field} missing from {state}")

		# Pick the original 2020 campaign
		campaign = campaigns['2020_presidential']
		for state, ref_state_info in URLS_BY_STATE.items():
			state_info = {}
			state_info.update(ref_state_info)
			state_info.update(campaign.info_by_state[state])
			print(state_info[ABS], state_info[REGDL])

			cities = state_info[CITIES]
			self.assertEqual(len(cities), len(set(cities)))  # Check no duplicates
			print(hashtag(state_info[CODE], plain=True))
			for city in cities:
				print(hashtag(city))

			_present(REG)
			_present(REGDL)
			_present(ABS)
			_present(POLLS)
			_present(CITIES)

	def test_04build_voterinfo(self):
		def _call_build_voterinfo(bound):
			effective_len, tweet = build_voterinfo(campaign, state)
			print(effective_len)
			print(tweet)
			assert len(tweet) > bound  # XXX This could flap

		random.seed(0)
		campaign = campaigns['2020_presidential']
		for state in ("Georgia", "California", "Idaho", "West Virginia", "Puerto Rico", "Guam"):
			_call_build_voterinfo(0)

		campaign = campaigns['2021_georgia_runoff']
		state = 'Georgia'
		_call_build_voterinfo(-1)

		campaign = campaigns['2021_california_recall']
		state = 'California'
		_call_build_voterinfo(0)

		self.assertRaises(KeyError, build_voterinfo, campaigns['2020_presidential'], ("Arcadia",))

	@mock.patch("twitter.Api.UsersLookup")
	@mock.patch("twitter.Api.GetFollowerIDs")
	@mock.patch("twitter.Api.GetFriendIDs")
	@mock.patch("transport.post_tweet")
	def test_05socialize_main(self, mock_post, mock_friends, mock_followers, _):
		mock_post.return_value = 0
		importlib.reload(socialize)

		mock_followers.return_value \
			= (157815060, 1230281, 13027572, 155295889, 26825139, 153942024, 153934792)
		mock_friends.return_value \
			= (26825139, 13027572, 823171093854912516, 54885400, 153942024)
		arg0 = sys.argv[0]
		campaign = campaigns['2020_presidential']
		sys.argv = [arg0, '2020_presidential']
		socialize.main()
		mock_post.assert_has_calls([mock.call(build_socialize, campaign, 13027572),
									mock.call(build_socialize, campaign, 153942024),
									mock.call(build_socialize, campaign, 26825139)], any_order=True)

		sys.argv = [arg0]

	def test_06build_socialize(self):
		for campaign_name in campaigns:
			campaign = campaigns[campaign_name]
			effective_length, tweet_text = build_socialize(campaign, MY_TWITTER_UID)
			print(effective_length)
			print(tweet_text)
			if campaign.SEARCH_URL in campaign.campaign_info:
				self.assertIn(campaign.campaign_info[campaign.SEARCH_URL], tweet_text,
							  "Search URL not found in tweet.")

	@staticmethod
	def _fake_users(*_, screen_name=None):
		# id is the wrong type here, but we just need unique objects
		return [User(id=n, screen_name=n) for n in screen_name]

	@mock.patch("twitter.Api.UsersLookup")
	def test_07process_do_not_call(self, mock_users_lookup):
		mock_users_lookup.side_effect = self._fake_users
		dnc = open(os.path.join(sys.path[0], "do_not_call.txt"))
		line_ct = 0
		for _ in dnc.readlines():
			line_ct += 1
		dnc.close()

		# Requires no duplicates in DNC list
		self.assertEqual(line_ct, len(socialize.process_do_not_call()))


if __name__ == '__main__':
	unittest.main()
