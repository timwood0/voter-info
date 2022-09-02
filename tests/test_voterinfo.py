import unittest
import mock
import sys
import os
import importlib
import requests
import tweepy

from tweepy import User

import campaign
import voterinfo, socialize
from render import *
from urlsbystate import URLS_BY_STATE, CODE, CITIES, REGDL, REG, POLLS, ABS
from campaign import campaigns


MY_TWITTER_UID = 16230307


class TestVoterInfo(unittest.TestCase):
	def tearDown(self):
		importlib.reload(socialize)
		importlib.reload(voterinfo)

	@staticmethod
	def _fake_users(*, usernames=None):
		resp = requests.Response()
		users = []
		for n in usernames:
			users.append(User({"id": len(users),
							   "name": n,
							   "username": n,
							   "created_at": None,
							   "description": "",
							   "entities": None, "location": None, "pinned_tweet_id": None, "profile_image_url": None,
							   "protected": None, "public_metrics": None, "url": None, "verified": None, "withheld": None}
			))

		resp.data = users
		return resp

	@mock.patch("tweepy.Client.create_tweet")
	def test_01voterinfo_main(self, mock_create_tweet):
		mock_create_tweet.return_value = 0
		arg0 = sys.argv[0]
		sys.argv = [arg0, '2020_cerfvqragvny', 'Puerto Rico']
		self.assertEqual(voterinfo.main(), 0)

		sys.argv = [arg0, '2020_cerfvqragvny', 'Arcadier']
		self.assertEqual(voterinfo.main(), 1)

		sys.argv = [arg0]
		with mock.patch("argparse.ArgumentParser.exit", side_effect=IndexError):
			self.assertRaises(IndexError, voterinfo.main)

		sys.argv = [arg0, '2021_trbetvn_ehabss']
		self.assertEqual(voterinfo.main(), 0)

		mock_create_tweet.side_effect = tweepy.errors.HTTPException(requests.Response())
		sys.argv = [arg0, '2021_trbetvn_ehabss']
		self.assertEqual(voterinfo.main(), 1)

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
		campaign = campaigns['2020_cerfvqragvny']
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
		def _call_build_voterinfo(campaign, bound):
			for state in campaign.info_by_state:
				effective_len, tweet = build_voterinfo(campaign, state)
				print(effective_len)
				print(tweet)
				assert len(tweet) > bound  # XXX This could flap

		random.seed(0)
		_call_build_voterinfo(campaigns['2020_cerfvqragvny'], 0)

		_call_build_voterinfo(campaigns['2021_trbetvn_ehabss'], -1)

		_call_build_voterinfo(campaigns['2021_pnyvsbeavn_erpnyy'], 0)

		_call_build_voterinfo(campaigns['2021_aw_in_tbi'], 0)

		_call_build_voterinfo(campaigns['2022_xnafnf_pubvpr'], 0)

		self.assertRaises(KeyError, build_voterinfo, campaigns['2020_cerfvqragvny'], ("Arcadia",))

		distro_campaign = campaigns['2022_ggp_enzc_hc']
		_call_build_voterinfo(distro_campaign, 0)

		# Do some crude checking on the distribution selection
		set_size = len(distro_campaign.info_by_state['Georgia'][CITIES])
		sum_idx = 0
		for i in range(set_size >> 2):
			sum_idx += select_city(distro_campaign, distro_campaign.info_by_state['Georgia'], set_size)
		avg_idx = int(sum_idx / (set_size >> 2))
		print(f"Avg. index: {avg_idx}")
		self.assertTrue(60 < avg_idx < 70, "Avg. index out of range.")


	@mock.patch("tweepy.Client.follow_user")
	@mock.patch("tweepy.Client.get_users")
	@mock.patch("tweepy.Client.get_users_followers")
	@mock.patch("tweepy.Client.get_users_following")
	@mock.patch("tweepy.Client.get_user")
	@mock.patch("transport.post_tweet")
	def test_05socialize_main(self, mock_post, mock_get_user, mock_friends, mock_followers, _, mock_follow_user):
		mock_post.return_value = 0
		importlib.reload(socialize)

		mock_get_user.return_value.data.id = MY_TWITTER_UID
		mock_friends.return_value \
			= (26825139, 13027572, 823171093854912516, 54885400, 153942024)
		mock_followers.return_value \
			= (157815060, 1230281, 13027572, 155295889, 26825139, 153942024, 153934792)
		mock_follow_user.return_value = requests.Response()
		arg0 = sys.argv[0]

		campaign_name = '2020_cerfvqragvny'
		campaign = campaigns[campaign_name]
		sys.argv = [arg0, campaign_name]
		with mock.patch("socialize.process_opt_in") as mock_opt_in:
			mock_opt_in.return_value = {13027572, 153942024, 26825139}
			socialize.main()
		mock_post.assert_has_calls([mock.call(build_socialize, campaign, 13027572),
									mock.call(build_socialize, campaign, 153942024),
									mock.call(build_socialize, campaign, 26825139)], any_order=True)
		mock_post.reset_mock()
		# Test we don't tweet unless opted in
		with mock.patch("socialize.process_opt_in") as mock_opt_in:
			mock_opt_in.return_value = {153942024, 26825139}
			socialize.main()
		try:
			mock_post.assert_has_calls([mock.call(build_socialize, campaign, 13027572)], any_order=True)
			raise AssertionError("Should not have a call for 13027572.")
		except AssertionError:
			# The above call should not take place
			pass
		mock_post.reset_mock()

		campaign_name = '2021_pnyvsbeavn_erpnyy'
		campaign = campaigns[campaign_name]
		sys.argv = [arg0, campaign_name, '-i', '153942024']
		with mock.patch("socialize.process_opt_in") as mock_opt_in:
			mock_opt_in.return_value = {153942024}
			socialize.main()
		mock_post.assert_has_calls([mock.call(build_socialize, campaign, 153942024)])
		mock_post.reset_mock()
		with mock.patch("socialize.process_opt_in") as mock_opt_in:
			mock_opt_in.return_value = {}
			socialize.main()
		try:
			mock_post.assert_has_calls([mock.call(build_socialize, campaign, 153942024)])
			raise AssertionError("Should not have a call for 153942024.")
		except AssertionError:
			# The above call should not take place
			pass
		mock_post.reset_mock()

		sys.argv = [arg0, campaign_name, 'livecut']
		with mock.patch("socialize.process_opt_in") as mock_opt_in:
			mock_opt_in.return_value = {MY_TWITTER_UID}
			socialize.main()
		mock_post.assert_has_calls([mock.call(build_socialize, campaign, MY_TWITTER_UID)])
		mock_post.reset_mock()

		campaign_name = "2022_ggp_enzc_hc"
		sys.argv = [arg0, campaign_name, "livecut"]
		with mock.patch("socialize.process_opt_in") as mock_opt_in:
			mock_opt_in.return_value = {MY_TWITTER_UID}
			mock_follow_user.return_value.data = {'following': True, 'pending_follow': False}
			socialize.main()
		mock_follow_user.assert_has_calls([mock.call(MY_TWITTER_UID)])
		mock_post.reset_mock()

		sys.argv = [arg0, campaign_name, '-i', '153942024', 'livecut']
		with mock.patch("sys.exit"):
			with mock.patch("socialize.process_opt_in") as mock_opt_in:
				socialize.main()
		mock_post.assert_has_calls([])

		sys.argv = [arg0]

	@mock.patch("tweepy.Client.get_user")
	def test_06build_socialize(self, mock_get_user):
		mock_get_user.return_value.data.username = 'livecut'
		for campaign_name in campaigns:
			campaign = campaigns[campaign_name]
			effective_length, tweet_text = build_socialize(campaign, MY_TWITTER_UID)
			print(effective_length)
			print(tweet_text)
			if campaign.SEARCH_URL in campaign.campaign_info \
				and campaign.campaign_info[campaign.SEARCH_URL] is not None:
				self.assertIn(campaign.campaign_info[campaign.SEARCH_URL], tweet_text,
							  "Search URL not found in tweet.")

	@mock.patch("tweepy.Client.get_users")
	def test_07process_do_not_call(self, mock_users_lookup):
		mock_users_lookup.side_effect = self._fake_users
		dnc = open(os.path.join(sys.path[0], "do_not_call.txt"))
		line_ct = 0
		for _ in dnc.readlines():
			line_ct += 1
		dnc.close()

		# Requires no duplicates in DNC list
		self.assertEqual(line_ct, len(socialize.process_opt_list("do_not_call.txt")))


if __name__ == '__main__':
	unittest.main()
