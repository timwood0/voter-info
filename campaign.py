import re

from urlsbystate import (
	States, URLS_BY_STATE, CITIES, REGDL, REG, POLLS, ABROAD, ABS, CODE
)
from render import hashtag

# Class to model a tweeting campaign, generally in the context of elections taking place in
# one or more states.
class Campaign:
	PREAMBLE = 'pre'
	SEARCH_URL = 'search_url'
	TWEET_CONTENT = 'tweet_markup'
	VOTER_INFO = 'voter_info'
	SOCIALIZE = 'socialize'
	HEADER = 'header'
	SEARCH = 'search'
	PER_STATE = 'per_state'
	RT = 'rt'
	BE_SURE = 'be_sure'
	VOTE_MSG = 'vote'

	TWEET_TEMPLATES = {
		# Dicts of keys: tuples of strings parseable with eval().  Quick & dirty way to build a tweet
		# from a specification using runtime data.  XXX Fails security review. :o
		# Break out message elements that contain URLs to make accurate effective length calculations.
		# XXX This belongs in a file as configuration.
		VOTER_INFO: {
			PREAMBLE: ['f"{hashtag(state)} {hashtag(self.info_by_state[state][CODE], True)}"'
			"""f' {hashtag(self.info_by_state[state].get(Campaign.VOTE_MSG, "vote"))}'"""],
			CITIES: ["""f'{" ".join(cities)}'"""],
			REGDL: ['"Reg. deadline: "', 'f"{self.info_by_state[state][REGDL]}"'],
			REG: ['"Check registration: "', 'f"{self.info_by_state[state][REG]}"'],
			POLLS: ['"Polling places: "', 'f"{self.info_by_state[state][POLLS]}"'],
			ABROAD: ['"Out of U.S.A.: "', 'f"{self.info_by_state[state][ABROAD]}"'],
			ABS: ['"Vote by mail: "', 'f"{self.info_by_state[state][ABS]}"']
		},
		SOCIALIZE: {
			HEADER: ['''f"""@{screen_name}
				Hi, we follow each other on Twitter.
				Please RT my voter info tweets to help get out the vote!"""'''],
			SEARCH: ['"Search my tweets: "', 'f"{self.campaign_info.get(Campaign.SEARCH_URL)}"'],
			PER_STATE: ['"Find a tweet for a state in the list, e.g., #Iowa or #NC."'],
			RT: ['"Retweet."'],
			BE_SURE: ['"Thanks, and be sure to #vote!"']
		}
	}

	VI_TEMPLATE = TWEET_TEMPLATES[VOTER_INFO]
	SOC_TEMPLATE = TWEET_TEMPLATES[SOCIALIZE]

	@property
	def campaign_info(self):
		return self._campaign_info

	def voterinfo(self, state, cities) -> list:
		"""Build a voterinfo tweet.
		:param state State name, used in tweet content eval
		:param cities City/topics list, used in tweet content eval
		:return List, starts with total length of URLs in the tweet, number of URLs in the tweet,
		then the tweet lines.
		"""

		if not self._tweet_content or not self._tweet_content[Campaign.VOTER_INFO]:
			return []

		ret_tweet = [0, 0]
		for line_parts in self._tweet_content[Campaign.VOTER_INFO]:
			line = ""
			for part in line_parts:
				part_val = re.sub('\t', '', eval(part))
				if re.match('^http[s]?://.*', part_val):
					ret_tweet[0] += len(part_val)
					ret_tweet[1] += 1
				line += part_val
			ret_tweet.append(line)

		return ret_tweet

	def socialize(self, screen_name) -> list:
		"""Build a socialize tweet.
		:param screen_name Twitter user name, used in tweet content eval.
		:return List of tweet lines.
		"""
		if not self._tweet_content or not self._tweet_content[Campaign.SOCIALIZE]:
			return []

		ret_tweet = [0, 0]
		for line_parts in self._tweet_content[Campaign.SOCIALIZE]:
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
		self._tweet_content = self._campaign_info.get(Campaign.TWEET_CONTENT, None)


# Campaigns data.  XXX This should be modeled in a database or flat files instead.
campaigns = {
	"2020_presidential": Campaign(
		{
			"Alabama": {
				CITIES: ['Birmingham', 'Anniston', 'Montgomery', 'Tuscaloosa', 'Mobile', 'Muscle Shoals', 'Dothan']},
			"Alaska": {CITIES: ['Anchorage', 'Fairbanks', 'Juneau', 'Nome', 'Dillingham', 'Barrow', 'Kodiak']},
			"Arizona": {CITIES: ['Phoenix', 'Flagstaff', 'Tucson', 'Yuma', 'Bullhead City', 'Tuba City', 'Prescott']},
			"Arkansas": {CITIES: ['Little Rock', 'Hot Springs', 'Pine Bluff', 'Hope', 'Fort Smith', 'Fayetteville']},
			"California": {CITIES: ['Los Angeles', 'San Francisco', 'Sacramento', 'San Diego', 'Anaheim', 'Fresno',
				'Modesto', 'Salinas', 'Redding']},
			"Colorado": {CITIES: ['Colorado Springs', 'Denver', 'Boulder', 'Grand Junction', 'Pueblo',
								  'Greeley', 'Sterling']},
			"Connecticut": {
				CITIES: ['Hartford', 'Stamford', 'New Haven', 'Bridgeport', 'Waterbury', 'Danbury', 'Norwich']},
			"Delaware": {CITIES: ['Dover', 'Wilmington', 'New Castle', 'Milford', 'Slaughter Beach', 'Seaford']},
			"District of Columbia": {CITIES: ['Washington']},
			"Florida": {
				CITIES: ['Tampa', 'Orlando', 'Miami', 'Palm Beach', 'Tallahassee', 'Jacksonville', 'Pensacola']},
			"Georgia": {CITIES: ['Atlanta', 'Savannah', 'Athens', 'Macon', 'Augusta', 'Valdosta', 'Warner Robins']},
			"Guam": {CITIES: ['Tamuning', 'Santa Rita', 'Piti', 'Dededo']},
			"Hawaii": {CITIES: ['Honolulu', 'Kahului', 'Hilo', 'Kapaa', 'Kaunakakai', 'Lanai City']},
			"Idaho": {CITIES: ["Coeur d'Alene", 'Boise', 'Pocatello', 'Gooding', 'Salmon', 'Lewiston']},
			"Illinois": {CITIES: ['Chicago', 'Evanston', 'East St. Louis', 'Peoria', 'Springfield', 'Rockford',
								  'Decatur', 'Rock Island']},
			"Indiana": {CITIES: ['Indianapolis', 'Gary', 'Fort Wayne', 'Terre Haute', 'South Bend',
								 'Evansville', 'Lafayette']},
			"Iowa": {
				CITIES: ['Dubuque', 'Ames', 'Cedar Rapids', 'Des Moines', 'Sioux City', 'Ft. Dodge', 'Council Bluffs']},
			"Kansas": {CITIES: ['Kansas City', 'Topeka', 'Wichita', 'Dodge City', 'Manhattan', 'Salina', 'Concordia']},
			"Kentucky": {CITIES: ['Louisville', 'Lexington', 'Bowling Green', 'Frankfort', 'Paducah',
								  'Mayfield', 'Danville']},
			"Louisiana": {CITIES: ['New Orleans', 'Shreveport', 'Baton Rouge', 'Monroe', 'Lake Charles', 'Evangeline']},
			"Maine": {CITIES: ['Bangor', 'Lewiston', 'Augusta', 'Portland', 'Presque Isle', 'Waterville']},
			"Maryland": {CITIES: ['Baltimore', 'Annapolis', 'Hagerstown', 'Cumberland', 'Aberdeen', 'Salisbury']},
			"Massachusetts": {
				CITIES: ['Boston', 'Springfield', 'Newton', 'Worcester', 'New Bedford', 'Quincy', 'Holyoke']},
			"Michigan": {CITIES: ['Detroit', 'Flint', 'Ann Arbor', 'Grand Rapids', 'Lansing', 'Marquette', 'Saginaw']},
			"Minnesota": {CITIES: ['Minneapolis', 'St. Paul', 'Rochester', 'Grand Forks', 'Duluth',
								   'Bloomington', 'St. Cloud']},
			"Mississippi": {
				CITIES: ['Hattiesburg', 'Jackson', 'Biloxi', 'Gulfport', 'Greenwood', 'Columbus', 'Meridian']},
			"Missouri": {CITIES: ['St. Louis', 'Kansas City', 'Springfield', 'Independence', 'Jefferson City',
								  'Joplin', 'Ferguson']},
			"Montana": {CITIES: ['Bozeman', 'Butte', 'Great Falls', 'Billings', 'Missoula', 'Helena', 'Wolf Point']},
			"Nebraska": {CITIES: ['Omaha', 'Lincoln', 'North Platte', 'Valentine', 'Scottsbluff', 'Columbus']},
			"Nevada": {CITIES: ['Las Vegas', 'Carson City', 'Reno', 'Elko', 'Winnemucca', 'Henderson', 'Boulder City']},
			"New Hampshire": {CITIES: ['Berlin', 'Manchester', 'Nashua', 'Concord', 'Hanover', 'Portsmouth', 'Keene']},
			"New Jersey": {CITIES: ['Newark', 'Jersey City', 'Morristown', 'Trenton', 'New Brunswick',
									'Vineland', 'Camden', 'Paterson']},
			"New Mexico": {CITIES: ['Gallup', 'Albuquerque', 'Santa Fe', 'Las Cruces', 'Los Alamos', 'Roswell']},
			"New York": {
				CITIES: ['New York City', 'Albany', 'Rochester', 'Buffalo', 'Binghamton', 'Syracuse', 'Ithaca']},
			"North Carolina": {CITIES: ['Raleigh', 'Greensboro', 'Winston-Salem', 'Charlotte', 'Wilmington',
										'Asheville', 'Fayetteville']},
			"North Dakota": {CITIES: ['Grand Forks', 'Fargo', 'Bismarck', 'Jamestown', 'Dickinson', 'Minot']},
			"Ohio": {CITIES: ['Columbus', 'Akron', 'Cleveland', 'Toledo', 'Cincinnati', 'Dayton', 'Chillicothe']},
			"Oklahoma": {CITIES: ['Oklahoma City', 'Tulsa', 'Muskogee', 'Enid', 'Guymon', 'Ardmore']},
			"Oregon": {
				CITIES: ['Portland', 'Salem', 'Eugene', 'Ashland', 'Medford', 'Bend', 'Klamath Falls', 'Pendleton']},
			"Pennsylvania": {CITIES: ['Philadelphia', 'Pittsburgh', 'Scranton', 'Harrisburg',
									  'Allentown', 'Johnstown', 'Altoona', 'Gettysburg']},
			"Puerto Rico": {CITIES: ['San Juan', 'Mayaguez', 'Arecibo', 'Ponce', 'Caguas']},
			"Rhode Island": {CITIES: ['Providence', 'Cranston', 'Metunuck', 'Warwick', 'Newport', 'Woonsocket']},
			"South Carolina": {
				CITIES: ['Charleston', 'Columbia', 'Greenville', 'Augusta', 'Springfield', 'Orangeburg']},
			"South Dakota": {CITIES: ['Sioux Falls', 'Rapid City', 'Mitchell', 'Pierre', 'Springfield', 'Mobridge']},
			"Tennessee": {CITIES: ['Memphis', 'Nashville', 'Chattanooga', 'Knoxville', 'Springfield',
								   'Oak Ridge', 'Murfreesboro']},
			"Texas": {CITIES: ['Dallas', 'Fort Worth', 'Austin', 'Houston', 'Amarillo', 'Lubbock',
							   'El Paso', 'San Antonio', 'Big Spring']},
			"Utah": {CITIES: ['Provo', 'Salt Lake City', 'Ogden', 'Cedar City', 'Vernal', 'Logan']},
			"Vermont": {CITIES: ['Brattleboro', 'Rutland', 'Burlington', 'Barre', 'Montpelier', 'St. Albans']},
			"Virginia": {
				CITIES: ['Richmond', 'Vienna', 'Arlington', 'Norfolk', 'Portsmouth', 'Virginia Beach', 'Roanoke']},
			"Washington": {
				CITIES: ['Seattle', 'Tacoma', 'Bellingham', 'Spokane', 'Walla Walla', 'Olympia', 'Richland']},
			"West Virginia": {CITIES: ['Huntington', 'Charleston', 'Parkersburg', 'Wheeling', 'Clarksburg', 'Beckley']},
			"Wisconsin": {CITIES: ['Milwaukee', 'Kenosha', 'Green Bay', 'Eau Claire', 'Madison', 'Wausau', 'Duluth']},
			"Wyoming": {CITIES: ['Cheyenne', 'Sheridan', 'Cody', 'Rock Springs', 'Casper', 'Laramie']},
		},
		campaign_info={
			Campaign.SEARCH_URL:
				"https://twitter.com/search?q=%22Out%20of%20U.S.A.%22%20%22Vote%20by%20mail%3A%22&f=live",
			Campaign.TWEET_CONTENT: {
				Campaign.VOTER_INFO: [
					Campaign.VI_TEMPLATE[Campaign.PREAMBLE],
					Campaign.VI_TEMPLATE[CITIES],
					Campaign.VI_TEMPLATE[REGDL],
					Campaign.VI_TEMPLATE[REG],
					Campaign.VI_TEMPLATE[POLLS],
					Campaign.VI_TEMPLATE[ABROAD],
					Campaign.VI_TEMPLATE[ABS]
				],
				Campaign.SOCIALIZE: [
					Campaign.SOC_TEMPLATE[Campaign.HEADER],
					Campaign.SOC_TEMPLATE[Campaign.SEARCH],
					Campaign.SOC_TEMPLATE[Campaign.PER_STATE],
					Campaign.SOC_TEMPLATE[Campaign.RT],
					Campaign.SOC_TEMPLATE[Campaign.BE_SURE]
				]
			}
		}
	),
	"2021_georgia_runoff": Campaign(
		{
			States.GEORGIA: {CITIES: [
				'Albany', 'Morgan', 'Fort Gaines', 'Dawson', 'Cuthbert', 'Richland', 'Americus', 'Athens',
				'Carrollton', 'Fort Oglethorpe', 'Talbotton', 'Hinesville', 'Macon', 'Louisville', 'Sparta',
				'Warrenton', 'Crawfordville', 'Lawrenceville', 'Marietta', 'Douglasville', 'Jonesboro',
				'McDonough', 'Conyers', 'Covington', 'Decatur', 'North Decatur', 'Savannah', 'Kennesaw',
				'Statesboro', 'Dalton', 'Douglas', 'Tifton', 'Sandy Springs',
				# Colleges
				'Georgia State', 'Georgia Tech', 'Agnes Scott', 'South', 'Oglethorpe',
				'Univ. of Georgia', 'Strayer', 'Emory', 'Kennesaw State',
				'Georgia Southern', 'Clark Atlanta', 'Morehouse', 'Brenau',
				'Georgia Highlands', 'Spelman', 'Life', 'Savannah State',
				'Abraham Baldwin', 'Dalton State', 'Columbia State',
				'Georgia Gwinnet', 'Coastal Georgia', 'North Georgia', 'Clayton State',
				'Mercer', 'Middle Georgia', 'Georgia Southwestern', 'Albany State',
				'Georgia', 'Armstrong State', 'Point',
				# Things Georgia
				'6LACK', 'Ray Charles', 'Allman Bros.', 'Otis Redding', 'R.E.M.', 'The B-52s',
				'Alison Krauss', 'Atlanta Rhythm Section', 'CeeLo Green', 'Cat Power',
				'Confederate Railroad', 'Brenda Lee', 'Bubba Knight', 'Bob', 'Boyz \'N Da Hood',
				'TLC', 'Trisha Yearwood', 'Alan Jackson', 'Outkast', 'Little Richard', 'James Brown',
				'John Mayer', 'Pylon', 'Zac Brown', 'Luke Bryan', 'Gladys Night', 'Indigo Girls',
				'Tetrarch', 'Collective Soul', 'Ludacris', 'Goodie Mob', 'YoungBloodZ', 'Lil Nas X',
				'Black Crowes', 'Ciara', 'Jermaine Dupri', 'Mastodon', 'Usher', 'Sugarland',
				'Florida Georgia Line', 'Falcons', 'Foxes and Fossils',
				'Fort Benning', 'Marshall Tucker Band',
				# Pro athletes
				# Atlanta Falcons
				'Matt Ryan', 'Julio Jones', 'Alex Mack', 'Deion Jones', 'Grady Jarrett', 'James Carpenter',
				'Jake Matthews', 'Todd Gurley', 'Chris Lindstrom', 'Calvin Ridley', 'Kaleb McGary',
				'Tyeler Davison', 'Isaiah Oliver', 'Keanu Neal', 'Ricardo Allen', 'Dante Fowler',
				'Luke Stocker', 'Foyesade Oluokun', 'AJ Terrell', 'Hayden Hurst', 'Steven Means',
				'Hank Aaron'
			]}
		}
	),
	"2021_california_recall": Campaign(
		{
			States.CALIFORNIA: {CITIES: [
				# Supplied by @balkingpoints
				'Los Angeles', 'San Francisco', 'San Diego', 'Riverside', 'Sacramento', 'San Jose', 'Fresno',
				'Concord', 'Mission Viejo', 'Bakersfield', 'Murrieta', 'Long Beach', 'Oakland',
				# 'Indio',
				'Stockton', 'Oxnard', 'Modesto', 'Anaheim', 'Lancaster',
				# 'Victorville',
				# 'Santa Ana',
				'Santa Rosa', 'Santa Clarita', 'Antioch', 'Irvine', 'Chula Vista', 'Fremont',
				# 'Visalia',
				'Thousand Oaks', 'San Bernardino', 'Fontana', 'Moreno Valley', 'Santa Barbara', 'Glendale',
				'Huntington Beach', 'Salinas', 'Santa Cruz', 'Rancho Cucamonga',
				# 'Hemet',
				'Oceanside', 'Ontario',
				'Garden Grove', 'Vallejo', 'Elk Grove', 'Corona', 'Hayward', 'Palmdale', 'Sunnyvale', 'Pomona',
				'Escondido', 'Fairfield', 'Torrance', 'Merced', 'Pasadena',
				# 'Orange',
				'Fullerton', 'Santa Maria', 'Roseville',
				# 'Simi Valley',
				'Santa Clara', 'East Los Angeles', 'Berkeley',
				# 'Redding',
				# 'Yuba City',
				'Seaside', 'Gilroy', 'El Monte', 'Carlsbad', 'Temecula', 'Costa Mesa', 'Downey',
				'El Centro', 'San Buenaventura', 'Inglewood', 'Richmond', 'Clovis', 'West Covina',
				'Turlock',
				'Daly City', 'Chico', 'Norwalk', 'Jurupa Valley', 'Burbank', 'San Mateo', 'El Cajon', 'Rialto',
				'Vista', 'Vacaville', 'Manteca', 'Arden-Arcade', 'Compton', 'San Marcos', 'Tracy', 'South Gate',
				# 'Hesperia',
				'Carson', 'Santa Monica',
				# 'Hanford',
				'Westminster', 'Livermore',
				# Added by Tim
				'Mendocino', 'Eureka', 'Ukiah', 'Woodland', 'Davis', 'Petaluma',
				'San Luis Obispo', 'Paso Robles', 'Pismo Beach', 'Morro Bay', 'Monterey',
				'Delano', 'Ventura', 'Los Banos', 'Wasco', 'Coalinga', 'Atwater',
				'La Jolla', 'Madera', 'Hollister', 'Soledad'
			], Campaign.VOTE_MSG: "CA Recall", REGDL: "August 30, 2021!"}
		},
		campaign_info={
			Campaign.TWEET_CONTENT: {
				Campaign.VOTER_INFO: [
					Campaign.VI_TEMPLATE[Campaign.PREAMBLE],
					Campaign.VI_TEMPLATE[CITIES],
					Campaign.VI_TEMPLATE[POLLS],
					['"Completed your ballot?  Drop in the mail today, no postage necessary!"'],
					['"Find mailboxes: "', '"https://tools.usps.com/find-location.htm?locationType=collectionbox"'],
				],
				Campaign.SOCIALIZE: [
					# Initial contact message
					# ['''f"""@{screen_name}
					# Hi, we follow each other on Twitter.
					# Please RT my tweets for California recall turnout!"""'''],
					# Campaign.SOC_TEMPLATE[Campaign.SEARCH],
					# Campaign.SOC_TEMPLATE[Campaign.RT],
					# ['''"""For a 1 mention/day reminder, reply YES.
					# Otherwise this will be the last contact on this topic. Thank you!"""''']
					# Daily reminder message
					['''f"""@{screen_name}, here's that daily reminder to
					retweet my tweets for California recall turnout!"""'''],
					Campaign.SOC_TEMPLATE[Campaign.SEARCH],
					['''"""Reply STOP to stop reminders, which end Sept. 14th.
					Thanks again for helping."""''']
				]
			},
			Campaign.SEARCH_URL: "https://twitter.com/search?q=%23California%20%23CA%20%23CARecall&f=live"
		}
	)
}
