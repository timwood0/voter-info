VO = "https://www.vote.org"


def url_encode_state(state):
	return '-'.join(state.split(' ')).lower()


def absentee_ballot(state):
	return VO + f"/absentee-ballot/{url_encode_state(state)}"


def reg_deadline(state):
	return VO + f"/voter-registration-deadlines/#{url_encode_state(state)}"


def abroad(state):
	return f"https://www.votefromabroad.org/states/{URLS_BY_STATE[state]['code']}"


# Static info, extended with initializers below
URLS_BY_STATE = {
	"Alabama": {"code": "AL",
				"reg": "https://myinfo.alabamavotes.gov/VoterView/RegistrantSearch.do",
				"polls": "https://myinfo.alabamavotes.gov/VoterView/PollingPlaceSearch.do",
				"cities": ['Birmingham', 'Anniston', 'Montgomery', 'Tuscaloosa', 'Mobile', 'Muscle Shoals', 'Dothan']},
	"Alaska": {"code": "AK",
			   "reg": "https://myvoterinformation.alaska.gov/",
			   "polls": "https://myvoterinformation.alaska.gov/",
			   "cities": ['Anchorage', 'Fairbanks', 'Juneau', 'Nome', 'Dillingham', 'Barrow', 'Kodiak']},
	"Arizona": {"code": "AZ",
				"reg": "https://voter.azsos.gov/VoterView/RegistrantSearch.do",
				"polls": "https://my.arizona.vote/PortalList.aspx",
				"cities": ['Phoenix', 'Flagstaff', 'Tucson', 'Yuma', 'Bullhead City', 'Tuba City', 'Prescott']},
	"Arkansas": {"code": "AR",
				 "reg": "https://www.voterview.ar-nova.org/voterview",
				 "polls": "https://www.voterview.ar-nova.org/voterview",
				 "cities": ['Little Rock', 'Hot Springs', 'Pine Bluff', 'Hope', 'Fort Smith', 'Fayetteville']},
	"California": {"code": "CA",
				   "reg": "https://www.sos.ca.gov/elections/registration-status/",
				   "polls": "https://www.sos.ca.gov/elections/polling-place/",
				   "cities": ['Los Angeles', 'San Francisco', 'Sacramento', 'San Diego', 'Anaheim', 'Fresno',
							  'Modesto', 'Salinas', 'Redding']},
	"Colorado": {"code": "CO",
				 "reg": "https://www.sos.state.co.us/voter/pages/pub/olvr/findVoterReg.xhtml",
				 "polls": "https://www.sos.state.co.us/pubs/elections/Resources/CountyElectionOffices.html",
				 "cities": ['Colorado Springs', 'Denver', 'Boulder', 'Grand Junction', 'Pueblo',
							'Greeley', 'Sterling']},
	"Connecticut": {"code": "CT",
					"reg": "https://www.dir.ct.gov/sots/LookUp.aspx",
					"polls": "https://portaldir.ct.gov/sots/LookUp.aspx",
					"cities": ['Hartford', 'Stamford', 'New Haven', 'Bridgeport', 'Waterbury', 'Danbury', 'Norwich']},
	"Delaware": {"code": "DE",
				 "reg": "https://ivote.de.gov/voterview",
				 "polls": "https://ivote.de.gov/VoterView",
				 "cities": ['Dover', 'Wilmington', 'New Castle', 'Milford', 'Slaughter Beach', 'Seaford']},
	"District of Columbia": {"code": "DC",
						"reg": "https://www.dcboe.org/Voters/Register-To-Vote/Check-Voter-Registration-Status",
						"polls": "https://www.dcboe.org/Voters/Where-to-Vote/Find-Out-Where-to-Vote",
						"cities": ['Washington']},
	"Florida": {"code": "FL",
				"reg": "http://registration.elections.myflorida.com/CheckVoterStatus",
				"polls": "https://registration.elections.myflorida.com/CheckVoterStatus",
				"cities": ['Tampa', 'Orlando', 'Miami', 'Palm Beach', 'Tallahassee', 'Jacksonville', 'Pensacola']},
	"Georgia": {"code": "GA",
				"reg": "http://www.mvp.sos.ga.gov/",
				"polls": "https://www.mvp.sos.ga.gov/MVP/mvp.do",
				"cities": ['Atlanta', 'Savannah', 'Athens', 'Macon', 'Augusta', 'Valdosta', 'Warner Robins']},
	"Guam": {"code": "GU",
				"abs": "https://gec.guam.gov/index.php/in-office/in-office-absentee-voting",
				"reg": "https://gec.guam.gov/validate",
				"regdl": "https://gec.guam.gov/index.php/gec-2018-election-important-dates",
				"polls": "https://drive.google.com/file/d/1w6pdGRrjwqVMa8cRbx_-9zObMCVQQ3aR/view",
				"cities": ['Tamuning', 'Santa Rita', 'Piti', 'Dededo']},
	"Hawaii": {"code": "HI",
			   "reg": "https://olvr.hawaii.gov/register.aspx",
			   "polls": "https://olvr.hawaii.gov/altpollingplacesearch.aspx",
			   "cities": ['Honolulu', 'Kahului', 'Hilo', 'Kapaa', 'Kaunakakai', 'Lanai City']},
	"Idaho": {"code": "ID",
			  "reg": "https://elections.sos.idaho.gov/ElectionLink/ElectionLink/VoterSearch.aspx",
			  "polls": "https://elections.sos.idaho.gov/ElectionLink/ElectionLink/ViewPollingLocation.aspx",
			  "cities": ["Coeur d'Alene", 'Boise', 'Pocatello', 'Gooding', 'Salmon', 'Lewiston']},
	"Illinois": {"code": "IL",
				 "reg": "https://ova.elections.il.gov/RegistrationLookup.aspx",
				 "polls": "https://ova.elections.il.gov/PollingPlaceLookup.aspx",
				 "cities": ['Chicago', 'Evanston', 'East St. Louis', 'Peoria', 'Springfield', 'Rockford',
							'Decatur', 'Rock Island']},
	"Indiana": {"code": "IN",
				"reg": "https://indianavoters.in.gov/",
				"polls": "https://indianavoters.in.gov/",
				"cities": ['Indianapolis', 'Gary', 'Fort Wayne', 'Terre Haute', 'South Bend',
						   'Evansville', 'Lafayette']},
	"Iowa": {"code": "IA",
			 "reg": "https://sos.iowa.gov/elections/VoterReg/RegToVote/search.aspx",
			 "polls": "https://sos.iowa.gov/elections/voterreg/pollingplace/search.aspx",
			 "cities": ['Dubuque', 'Ames', 'Cedar Rapids', 'Des Moines', 'Sioux City', 'Ft. Dodge', 'Council Bluffs']},
	"Kansas": {"code": "KS",
			   "reg": "https://myvoteinfo.voteks.org/VoterView/RegistrantSearch.do",
			   "polls": "https://myvoteinfo.voteks.org/VoterView/PollingPlaceSearch.do",
			   "cities": ['Kansas City', 'Topeka', 'Wichita', 'Dodge City', 'Manhattan', 'Salina', 'Concordia']},
	"Kentucky": {"code": "KY",
				 "reg": "https://vrsws.sos.ky.gov/VIC/",
				 "polls": "https://www.sos.ky.gov/elections/Pages/Polling-Locations.aspx",
				 "cities": ['Louisville', 'Lexington', 'Bowling Green', 'Frankfort', 'Paducah',
							'Mayfield', 'Danville']},
	"Louisiana": {"code": "LA",
				  "reg": "https://voterportal.sos.la.gov/",
				  "polls": "https://voterportal.sos.la.gov/",
				  "cities": ['New Orleans', 'Shreveport', 'Baton Rouge', 'Monroe', 'Lake Charles', 'Evangeline']},
	"Maine": {"code": "ME",
			  "reg": "http://www.maine.gov/portal/government/edemocracy/voter_lookup.php",
			  "polls": "https://www1.maine.gov/portal/government/edemocracy/voter_lookup.php",
			  "cities": ['Bangor', 'Lewiston', 'Augusta', 'Portland', 'Presque Isle', 'Waterville']},
	"Maryland": {"code": "MD",
				 "reg": "https://voterservices.elections.maryland.gov/votersearch",
				 "polls": "https://elections.maryland.gov/voting/where.html",
				 "cities": ['Baltimore', 'Annapolis', 'Hagerstown', 'Cumberland', 'Aberdeen', 'Salisbury']},
	"Massachusetts": {"code": "MA",
					  "reg": "https://www.sec.state.ma.us/VoterRegistrationSearch/MyVoterRegStatus.aspx",
					  "polls": "https://www.sec.state.ma.us/wheredoivotema/bal/MyElectionInfo.aspx",
					  "cities": ['Boston', 'Springfield', 'Newton', 'Worcester', 'New Bedford', 'Quincy', 'Holyoke']},
	"Michigan": {"code": "MI",
				 "reg": "https://mvic.sos.state.mi.us/",
				 "polls": "https://mvic.sos.state.mi.us/",
				 "cities": ['Detroit', 'Flint', 'Ann Arbor', 'Grand Rapids', 'Lansing', 'Marquette', 'Saginaw']},
	"Minnesota": {"code": "MN",
				  "reg": "https://mnvotes.sos.state.mn.us/VoterStatus.aspx",
				  "polls": "https://pollfinder.sos.state.mn.us/",
				  "cities": ['Minneapolis', 'St. Paul', 'Rochester', 'Grand Forks', 'Duluth',
							 'Bloomington', 'St. Cloud']},
	"Mississippi": {"code": "MS",
					"reg": "https://www.msegov.com/sos/voter_registration/AmIRegistered",
					"polls": "https://www.sos.ms.gov/PollingPlace/Pages/default.aspx",
					"cities": ['Hattiesburg', 'Jackson', 'Biloxi', 'Gulfport', 'Greenwood', 'Columbus', 'Meridian']},
	"Missouri": {"code": "MO",
				 "reg": "https://s1.sos.mo.gov/elections/voterlookup/",
				 "polls": "https://voteroutreach.sos.mo.gov/PRD/VoterOutreach/VOSearch.aspx",
				 "cities": ['St. Louis', 'Kansas City', 'Springfield', 'Independence', 'Jefferson City',
							'Joplin', 'Ferguson']},
	"Montana": {"code": "MT",
				"reg": "https://app.mt.gov/voterinfo/",
				"polls": "https://app.mt.gov/voterinfo/",
				"cities": ['Bozeman', 'Butte', 'Great Falls', 'Billings', 'Missoula', 'Helena', 'Wolf Point']},
	"Nebraska": {"code": "NE",
				 "reg": "https://www.votercheck.necvr.ne.gov/VoterView/RegistrantSearch.do",
				 "polls": "https://www.votercheck.necvr.ne.gov/VoterView/PollingPlaceSearch.do",
				 "cities": ['Omaha', 'Lincoln', 'North Platte', 'Valentine', 'Scottsbluff', 'Columbus']},
	"Nevada": {"code": "NV",
			   "reg": "https://nvsos.gov/votersearch/",
			   "polls": "https://www.nvsos.gov/votersearch/",
			   "cities": ['Las Vegas', 'Carson City', 'Reno', 'Elko', 'Winnemucca', 'Henderson', 'Boulder City']},
	"New Hampshire": {"code": "NH",
					  "reg": "https://app.sos.nh.gov/Public/PartyInfo.aspx",
					  "polls": "https://app.sos.nh.gov/Public/PollingPlaceSearch.aspx",
					  "cities": ['Berlin', 'Manchester', 'Nashua', 'Concord', 'Hanover', 'Portsmouth', 'Keene']},
	"New Jersey": {"code": "NJ",
				   "reg": "https://voter.njsvrs.com/PublicAccess/jsp/UserLogin/Login.jsp",
				   "polls": "https://voter.svrs.nj.gov/polling-place-search",
				   "cities": ['Newark', 'Jersey City', 'Morristown', 'Trenton', 'New Brunswick',
							  'Vineland', 'Camden', 'Paterson']},
	"New Mexico": {"code": "NM",
				   "reg": "https://voterportal.servis.sos.state.nm.us/WhereToVote.aspx",
				   "polls": "https://voterportal.servis.sos.state.nm.us/WhereToVoteAddress.aspx",
				   "cities": ['Gallup', 'Albuquerque', 'Santa Fe', 'Las Cruces', 'Los Alamos', 'Roswell']},
	"New York": {"code": "NY",
				 "reg": "https://voterlookup.elections.ny.gov/",
				 "polls": "https://voterlookup.elections.ny.gov/",
				 "cities": ['New York City', 'Albany', 'Rochester', 'Buffalo', 'Binghamton', 'Syracuse', 'Ithaca']},
	"North Carolina": {"code": "NC",
					   "reg": "https://vt.ncsbe.gov/RegLkup/",
					   "polls": "https://vt.ncsbe.gov/PPLkup/",
					   "cities": ['Raleigh', 'Greensboro', 'Winston-Salem', 'Charlotte', 'Wilmington',
								  'Asheville', 'Fayetteville']},
	"North Dakota": {"code": "ND",
					 "reg": "https://vip.sos.nd.gov/PortalListDetails.aspx?ptlhPKID=79&ptlPKID=7",
					 "polls": "https://vip.sos.nd.gov/wheretovote.aspx",
					 "cities": ['Grand Forks', 'Fargo', 'Bismarck', 'Jamestown', 'Dickinson', 'Minot']},
	"Ohio": {"code": "OH",
			 "reg": "https://voterlookup.ohiosos.gov/voterlookup.aspx",
			 "polls": "https://voterlookup.ohiosos.gov/VoterLookup.aspx",
			 "cities": ['Columbus', 'Akron', 'Cleveland', 'Toledo', 'Cincinnati', 'Dayton', 'Chillicothe']},
	"Oklahoma": {"code": "OK",
				 "reg": "https://services.okelections.us/voterSearch.aspx",
				 "polls": "https://okvoterportal.okelections.us/",
				 "cities": ['Oklahoma City', 'Tulsa', 'Muskogee', 'Enid', 'Guymon', 'Ardmore']},
	"Oregon": {"code": "OR",
			   "reg": "https://secure.sos.state.or.us/orestar/vr/showVoterSearch.do?source=SOS",
			   "polls": "https://sos.oregon.gov/voting/Pages/drop-box-locator.aspx",
			   "cities": ['Portland', 'Salem', 'Eugene', 'Ashland', 'Medford', 'Bend', 'Klamath Falls', 'Pendleton']},
	"Pennsylvania": {"code": "PA",
					 "reg": "https://www.pavoterservices.state.pa.us/Pages/VoterRegistrationStatus.aspx",
					 "polls": "https://www.pavoterservices.pa.gov/Pages/PollingPlaceInfo.aspx",
					 "cities": ['Philadelphia', 'Pittsburgh', 'Scranton', 'Harrisburg',
								'Allentown', 'Johnstown', 'Altoona', 'Gettysburg']},
	"Puerto Rico": {"code": "PR",
					"reg": "http://consulta.ceepur.org/",
					"regdl": "http://ww2.ceepur.org/Home/EducacionElectoral",
					"abs": "http://ww2.ceepur.org/Home/SolicituddeVoto#VotoAusente",
					"polls": "http://www.ceepur.org/directorio.htm",
					"cities": ['San Juan', 'Mayaguez', 'Arecibo', 'Ponce', 'Caguas']},
	"Rhode Island": {"code": "RI",
					 "reg": "https://vote.sos.ri.gov/Home/UpdateVoterRecord?ActiveFlag=0",
					 "polls": "https://vote.sos.ri.gov/Home/PollingPlaces?ActiveFlag=2",
					 "cities": ['Providence', 'Cranston', 'Metunuck', 'Warwick', 'Newport', 'Woonsocket']},
	"South Carolina": {"code": "SC",
					   "reg": "https://info.scvotes.sc.gov/eng/voterinquiry/VoterInformationRequest.aspx"
							  "?PagMode=VoterInfo",
					   "polls": "https://info.scvotes.sc.gov/eng/voterinquiry/VoterInformationRequest.aspx"
								"?PageMode=VoterInfo",
					   "cities": ['Charleston', 'Columbia', 'Greenville', 'Augusta', 'Springfield', 'Orangeburg']},
	"South Dakota": {"code": "SD",
					 "reg": "https://vip.sdsos.gov/viplogin.aspx",
					 "polls": "https://vip.sdsos.gov/viplogin.aspx",
					 "cities": ['Sioux Falls', 'Rapid City', 'Mitchell', 'Pierre', 'Springfield', 'Mobridge']},
	"Tennessee": {"code": "TN",
				  "reg": "https://tnmap.tn.gov/voterlookup/",
				  "polls": "https://web.go-vote-tn.elections.tn.gov/",
				  "cities": ['Memphis', 'Nashville', 'Chattanooga', 'Knoxville', 'Springfield',
							 'Oak Ridge', 'Murfreesboro']},
	"Texas": {"code": "TX",
			  "reg": "https://teamrv-mvp.sos.texas.gov/MVP/mvp.do",
			  "polls": "https://teamrv-mvp.sos.texas.gov/MVP/mvp.do",
			  "cities": ['Dallas', 'Fort Worth', 'Austin', 'Houston', 'Amarillo', 'Lubbock',
						 'El Paso', 'San Antonio', 'Big Spring']},
	"Utah": {"code": "UT",
			 "reg": "https://votesearch.utah.gov/voter-search/search/search-by-voter/voter-info",
			 "polls": "https://votesearch.utah.gov/voter-search/search/search-by-address/how-and-where-can-i-vote",
			 "cities": ['Provo', 'Salt Lake City', 'Ogden', 'Cedar City', 'Vernal', 'Logan']},
	"Vermont": {"code": "VT",
				"reg": "https://mvp.sec.state.vt.us/",
				"polls": "https://mvp.sec.state.vt.us/",
				"cities": ['Brattleboro', 'Rutland', 'Burlington', 'Barre', 'Montpelier', 'St. Albans']},
	"Virginia": {"code": "VA",
				 "reg": "https://vote.elections.virginia.gov/VoterInformation",
				 "polls": "https://www.elections.virginia.gov/citizen-portal/index.html",
				 "cities": ['Richmond', 'Vienna', 'Arlington', 'Norfolk', 'Portsmouth', 'Virginia Beach', 'Roanoke']},
	"Washington": {"code": "WA",
				   "reg": "https://www.sos.wa.gov/elections/myvote/",
				   "polls": "https://www.sos.wa.gov/elections/auditors/",
				   "cities": ['Seattle', 'Tacoma', 'Bellingham', 'Spokane', 'Walla Walla', 'Olympia', 'Richland']},
	"West Virginia": {"code": "WV",
					  "reg": "https://apps.sos.wv.gov/elections/voter/",
					  "polls": "https://services.sos.wv.gov/Elections/Voter/FindMyPollingPlace",
					  "cities": ['Huntington', 'Charleston', 'Parkersburg', 'Wheeling', 'Clarksburg', 'Beckley']},
	"Wisconsin": {"code": "WI",
				  "reg": "https://myvote.wi.gov/en-US/RegisterToVote",
				  "polls": "https://myvote.wi.gov/en-US/FindMyPollingPlace",
				  "cities": ['Milwaukee', 'Kenosha', 'Green Bay', 'Eau Claire', 'Madison', 'Wausau', 'Duluth']},
	"Wyoming": {"code": "WY",
				"reg": "https://sos.wyo.gov/Elections/Docs/WYCountyClerks.pdf",
				"polls": "https://soswy.state.wy.us/Elections/PollPlace/Default.aspx",
				"cities": ['Cheyenne', 'Sheridan', 'Cody', 'Rock Springs', 'Casper', 'Laramie']},
}


# Now do some dynamic setup in the table
for k, v in URLS_BY_STATE.items():
	if 'abs' not in v:
		v['abs'] = absentee_ballot(k)
	if 'regdl' not in v:
		v['regdl'] = reg_deadline(k)
	if 'abroad' not in v:
		v['abroad'] = abroad(k)
