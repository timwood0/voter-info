import re
from enum import auto

from lxml import etree, sax

from urlsbystate import (
	States, URLS_BY_STATE, CITIES, REGDL, REG, POLLS, ABROAD, ABS, CODE
)
from render import hashtag  # NOTE: Used in eval()


PREAMBLE = auto()
SEARCH_URL = auto()
TWEET_CONTENT = auto()
VOTER_INFO = auto()
SOCIALIZE = auto()
HEADER = auto()
SEARCH = auto()
PER_STATE = auto()
RT = auto()
BE_SURE = auto()
VOTE_MSG = auto()
ELECTION_DAY = auto()
USPO = auto()
MAILBOX = auto()
FOLLOW = auto()


def tweet_entry(*text):
	# Add an entry to the tweet suitable for input to eval().
	# Multi-line string and variable expansion with f"... is automatic.
	text_entry = []
	for item in text:
		text_entry.append("f'''" + item + "'''")

	return text_entry


# Class to model a tweeting campaign, generally in the context of elections taking place in
# one or more states.
class Campaign:

	@property
	def campaign_info(self):
		return self._campaign_info

	def build_tweet(self, state=None, cities=None, screen_name=None) -> list:
		"""Build a tweet.
		:param state State name, used in tweet content eval
		:param cities City/topics list, used in tweet content eval
			OR
		:screen_name Twitter user name, used in tweet content eval.

		:return List, starts with total length of URLs in the tweet, number of URLs in the tweet,
		then the tweet lines.
		"""

		if screen_name:
			template = SOCIALIZE
		else:
			template = VOTER_INFO
		if not self._tweet_content or not self._tweet_content[template]:
			return []

		ret_tweet = [0, 0]
		for line_parts in self._tweet_content[template]:
			line = ""
			for part in line_parts:
				part_val = re.sub('\t', '', eval(part))
				if re.match('^http[s]?://.*', part_val):
					ret_tweet[0] += len(part_val)
					ret_tweet[1] += 1
				line += part_val
			ret_tweet.append(line)

		return ret_tweet

	def __init__(self, info_by_state, campaign_info=None):
		# Build up a private aggregate of the reference data (s/b immutable) with our campaign specifics
		self.info_by_state = {}
		for state in info_by_state:
			self.info_by_state[state] = {}
			self.info_by_state[state].update(URLS_BY_STATE[state])
			self.info_by_state[state].update(info_by_state[state])

		# Configure which URL fields we're using
		self._campaign_info = campaign_info if campaign_info else {}
		self._tweet_content = self._campaign_info.get(TWEET_CONTENT, None)


# Campaigns data, loaded at initialization
campaigns = dict()


# Finally, supplement or define the Campaigns table from an XML campaign specification.
# XXX XSD to do this safely.
class CampaignXmlHandler(object):
	def __init__(self):
		self.campaigns = None
		self.campaign_info = None
		self.state_info = None
		self.state = None
		self.cities = None
		self.tweet_content = None
		self.voter_info = None
		self.socialize = None
		self.follow = None

		self.cur_data = None
		self.entry_target = None
		self.tweet_target = None

	def start(self, name, attrs):
		if name == "campaigns":
			self.campaigns = dict()
		if name == "campaign":
			self.campaign_name = attrs["name"]  # Used to create Campaign() at end of element
		elif name == "campaign-info":
			self.campaign_info = dict()
		elif name == "state-info":
			self.state_info = dict()
		elif name == "state":
			self.state = dict()
			self.state_info[attrs["name"]] = self.state
		elif name == "cities":
			self.cities = list()
		elif name == "city":
			self.cities.append(attrs["name"])
		elif name == "vote-msg":
			self.cur_data = None
		elif name == "reg-deadline":
			self.cur_data = None
		elif name == "search-url":
			self.cur_data = None
		elif name == "tweet-content":
			self.tweet_content = dict()
		elif name == "voter-info":
			self.voter_info = list()
			self.entry_target = self.voter_info
		elif name == "socialize":
			self.socialize = list()
			self.entry_target = self.socialize
		elif name == "entry":
			self.cur_data = None
		elif name == "follow":
			self.campaign_info[FOLLOW] = True

	def end(self, name):
		if name == "campaign":
			campaign = Campaign(self.state_info, self.campaign_info)
			self.campaigns[self.campaign_name] = campaign
		elif name == "cities":
			self.state[CITIES] = self.cities
		elif name == "vote-msg":
			self.state[VOTE_MSG] = self.cur_data
		elif name == "reg-deadline":
			self.state[REGDL] = self.cur_data
		elif name == "search-url":
			self.campaign_info[SEARCH_URL] = self.cur_data
		elif name == "tweet-content":
			self.campaign_info[TWEET_CONTENT] = self.tweet_content
		elif name == "voter-info":
			self.tweet_content[VOTER_INFO] = self.voter_info
		elif name == "socialize":
			self.tweet_content[SOCIALIZE] = self.socialize
		elif name == "entry":
			self.entry_target.append(eval(f"tweet_entry({self.cur_data})"))

	def data(self, content):
		self.cur_data = content

	def comment(self, text):
		pass

	def close(self):
		return self.campaigns


with open('./campaigns.xml') as campaigns_fd:
	campaign_data = campaigns_fd.read()
	# print(campaign_data)
	xml_campaigns = etree.XML(campaign_data, etree.XMLParser(target=CampaignXmlHandler()))
	campaigns.update(xml_campaigns)
	pass
