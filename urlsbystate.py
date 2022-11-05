VO = "https://www.vote.org"
VA = "https://www.voteamerica.com"
CODE = 'code'
REG = 'reg'
POLLS = 'polls'
CITIES = 'cities'  # XXX This should move to campaign.Campaign but it's disruptive
ABS = 'abs'
REGDL = 'regdl'
ABROAD = 'abroad'
VOTE_STATE = 'vote_state'


class States:
	ALABAMA = 'Alabama'
	ALASKA = 'Alaska'
	ARIZONA = 'Arizona'
	ARKANSAS = 'Arkansas'
	CALIFORNIA = 'California'
	COLORADO = 'Colorado'
	CONNECTICUT = 'Connecticut'
	DELAWARE = 'Delaware'
	DISTRICT_OF_COLUMBIA = 'District of Columbia'
	FLORIDA = 'Florida'
	GEORGIA = 'Georgia'
	GUAM = 'Guam'
	HAWAII = 'Hawaii'
	IDAHO = 'Idaho'
	ILLINOIS = 'Illinois'
	INDIANA = 'Indiana'
	IOWA = 'Iowa'
	KANSAS = 'Kansas'
	KENTUCKY = 'Kentucky'
	LOUISIANA = 'Louisiana'
	MAINE = 'Maine'
	MARYLAND = 'Maryland'
	MASSACHUSETTS = 'Massachusetts'
	MICHIGAN = 'Michigan'
	MINNESOTA = 'Minnesota'
	MISSISSIPPI = 'Mississippi'
	MISSOURI = 'Missouri'
	MONTANA = 'Montana'
	NEBRASKA = 'Nebraska'
	NEVADA = 'Nevada'
	NEW_HAMPSHIRE = 'New Hampshire'
	NEW_JERSEY = 'New Jersey'
	NEW_MEXICO = 'New Mexico'
	NEW_YORK = 'New York'
	NORTH_CAROLINA = 'North Carolina'
	NORTH_DAKOTA = 'North Dakota'
	OHIO = 'Ohio'
	OKLAHOMA = 'Oklahoma'
	OREGON = 'Oregon'
	PENNSYLVANIA = 'Pennsylvania'
	PUERTO_RICO = 'Puerto Rico'
	RHODE_ISLAND = 'Rhode Island'
	SOUTH_CAROLINA = 'South Carolina'
	SOUTH_DAKOTA = 'South Dakota'
	TENNESSEE = 'Tennessee'
	TEXAS = 'Texas'
	UTAH = 'Utah'
	VERMONT = 'Vermont'
	VIRGINIA = 'Virginia'
	WASHINGTON = 'Washington'
	WEST_VIRGINIA = 'West Virginia'
	WISCONSIN = 'Wisconsin'
	WYOMING = 'Wyoming'


def url_encode_state(state):
	return '-'.join(state.split(' ')).lower()


def absentee_ballot(state):
	return VA + f"/absentee-mail-ballot/{url_encode_state(state)}/#guide"


def reg_deadline(state):
	return VA + f"/voter-registration/{url_encode_state(state)}/#guide"


def abroad(state):
	return f"https://www.votefromabroad.org/states/{URLS_BY_STATE[state][CODE]}"


def vote_state(state):
	return VA + "/how-to-vote/" + state.lower().replace(' ', '-')


# Static info, extended with initializers below.
# Static schema:
# 	code: Postal state/territory code
# 	reg: URL for state voter registration
# 	polls: URL for state polling places
#	cities: Places people and things in state
#	vote: Optional call to action for hashtag
# Dynamic schema:
#	abs: Absentee ballot info (3rd party)
#	regdl: Registration deadlines (3rd party)
#	abroad: Voters abroad info
# XXX More of this should go in configuration.
URLS_BY_STATE = {
	"Alabama": {CODE: "AL",
				REG: "https://myinfo.alabamavotes.gov/VoterView/RegistrantSearch.do",
				POLLS: "https://myinfo.alabamavotes.gov/VoterView/PollingPlaceSearch.do"},
	"Alaska": {CODE: "AK",
			   REG: "https://myvoterinformation.alaska.gov/",
			   POLLS: "https://myvoterinformation.alaska.gov/"},
	"Arizona": {CODE: "AZ",
				REG: "https://voter.azsos.gov/VoterView/RegistrantSearch.do",
				POLLS: "https://my.arizona.vote/PortalList.aspx"},
	"Arkansas": {CODE: "AR",
				 REG: "https://www.voterview.ar-nova.org/voterview",
				 POLLS: "https://www.voterview.ar-nova.org/voterview"},
	"California": {CODE: "CA",
				   REG: "https://www.sos.ca.gov/elections/registration-status/",
				   POLLS: "https://www.sos.ca.gov/elections/polling-place/"},
	"Colorado": {CODE: "CO",
				 REG: "https://www.sos.state.co.us/voter/pages/pub/olvr/findVoterReg.xhtml",
				 POLLS: "https://www.coloradosos.gov/pubs/elections/VIP.html"},
	"Connecticut": {CODE: "CT",
					REG: "https://www.dir.ct.gov/sots/LookUp.aspx",
					POLLS: "https://portaldir.ct.gov/sots/LookUp.aspx"},
	"Delaware": {CODE: "DE",
				 REG: "https://ivote.de.gov/voterview",
				 POLLS: "https://ivote.de.gov/VoterView"},
	"District of Columbia": {CODE: "DC",
						REG: "https://www.dcboe.org/Voters/Register-To-Vote/Check-Voter-Registration-Status",
						POLLS: "https://www.dcboe.org/Voters/Where-to-Vote/Find-Out-Where-to-Vote"},
	"Florida": {CODE: "FL",
				REG: "http://registration.elections.myflorida.com/CheckVoterStatus",
				POLLS: "https://dos.myflorida.com/elections/for-voters/check-your-voter-status-and-polling-place/voter-precinct-lookup/"},
	"Georgia": {CODE: "GA",
				# A bit better than voteamerica.org's for the Jan. 2021 runoff,
				# but does not display in a Twitter card
				# ABS: "https://www.vote411.org/georgia#absentee-ballot-process",
				# REGDL: "https://sos.ga.gov/admin/files/2020%20Revised%20Short%20Calendar.pdf",
				REG: "https://www.mvp.sos.ga.gov/",
				POLLS: "https://www.mvp.sos.ga.gov/MVP/mvp.do"},
	"Guam": {CODE: "GU",
				ABS: "https://gec.guam.gov/index.php/in-office/in-office-absentee-voting",
				REG: "https://gec.guam.gov/validate",
				REGDL: "https://gec.guam.gov/index.php/gec-2018-election-important-dates",
				POLLS: "https://drive.google.com/file/d/1w6pdGRrjwqVMa8cRbx_-9zObMCVQQ3aR/view"},
	"Hawaii": {CODE: "HI",
			   REG: "https://olvr.hawaii.gov/register.aspx",
			   POLLS: "https://olvr.hawaii.gov/altpollingplacesearch.aspx"},
	"Idaho": {CODE: "ID",
			  REG: "https://elections.sos.idaho.gov/ElectionLink/ElectionLink/VoterSearch.aspx",
			  POLLS: "https://elections.sos.idaho.gov/ElectionLink/ElectionLink/ViewPollingLocation.aspx"},
	"Illinois": {CODE: "IL",
				 REG: "https://ova.elections.il.gov/RegistrationLookup.aspx",
				 POLLS: "https://ova.elections.il.gov/PollingPlaceLookup.aspx"},
	"Indiana": {CODE: "IN",
				REG: "https://indianavoters.in.gov/",
				POLLS: "https://indianavoters.in.gov/"},
	"Iowa": {CODE: "IA",
			 REG: "https://sos.iowa.gov/elections/VoterReg/RegToVote/search.aspx",
			 POLLS: "https://sos.iowa.gov/elections/voterreg/pollingplace/search.aspx"},
	"Kansas": {CODE: "KS",
			   REG: "https://myvoteinfo.voteks.org/VoterView",
			   POLLS: "https://myvoteinfo.voteks.org/VoterView"},
	"Kentucky": {CODE: "KY",
				 REG: "https://vrsws.sos.ky.gov/VIC/",
				 POLLS: "https://www.sos.ky.gov/elections/Pages/Polling-Locations.aspx"},
	"Louisiana": {CODE: "LA",
				  REG: "https://voterportal.sos.la.gov/",
				  POLLS: "https://voterportal.sos.la.gov/"},
	"Maine": {CODE: "ME",
			  REG: "http://www.maine.gov/portal/government/edemocracy/voter_lookup.php",
			  POLLS: "https://www1.maine.gov/portal/government/edemocracy/voter_lookup.php"},
	"Maryland": {CODE: "MD",
				 REG: "https://voterservices.elections.maryland.gov/votersearch",
				 POLLS: "https://elections.maryland.gov/voting/where.html"},
	"Massachusetts": {CODE: "MA",
					  REG: "https://www.sec.state.ma.us/VoterRegistrationSearch/MyVoterRegStatus.aspx",
					  POLLS: "https://www.sec.state.ma.us/wheredoivotema/bal/MyElectionInfo.aspx"},
	"Michigan": {CODE: "MI",
				 REG: "https://mvic.sos.state.mi.us/",
				 POLLS: "https://mvic.sos.state.mi.us/"},
	"Minnesota": {CODE: "MN",
				  REG: "https://mnvotes.sos.state.mn.us/VoterStatus.aspx",
				  POLLS: "https://pollfinder.sos.state.mn.us/"},
	"Mississippi": {CODE: "MS",
					REG: "https://www.msegov.com/sos/voter_registration/AmIRegistered",
					POLLS: "https://www.sos.ms.gov/PollingPlace/Pages/default.aspx"},
	"Missouri": {CODE: "MO",
				 REG: "https://s1.sos.mo.gov/elections/voterlookup/",
				 POLLS: "https://voteroutreach.sos.mo.gov/PRD/VoterOutreach/VOSearch.aspx"},
	"Montana": {CODE: "MT",
				REG: "https://app.mt.gov/voterinfo/",
				POLLS: "https://app.mt.gov/voterinfo/"},
	"Nebraska": {CODE: "NE",
				 REG: "https://www.votercheck.necvr.ne.gov/VoterView/RegistrantSearch.do",
				 POLLS: "https://www.votercheck.necvr.ne.gov/VoterView/PollingPlaceSearch.do"},
	"Nevada": {CODE: "NV",
			   REG: "https://nvsos.gov/votersearch/",
			   POLLS: "https://www.nvsos.gov/votersearch/"},
	"New Hampshire": {CODE: "NH",
					  REG: "https://app.sos.nh.gov/voterinformation",
					  POLLS: "https://app.sos.nh.gov/pollingplacesampleballot"},
	"New Jersey": {CODE: "NJ",
				   REG: "https://voter.njsvrs.com/PublicAccess/jsp/UserLogin/Login.jsp",
				   POLLS: "https://voter.svrs.nj.gov/polling-place-search"},
	"New Mexico": {CODE: "NM",
				   REG: "https://voterportal.servis.sos.state.nm.us/WhereToVote.aspx",
				   POLLS: "https://voterportal.servis.sos.state.nm.us/WhereToVoteAddress.aspx"},
	"New York": {CODE: "NY",
				 REG: "https://voterlookup.elections.ny.gov/",
				 POLLS: "https://voterlookup.elections.ny.gov/"},
	"North Carolina": {CODE: "NC",
					   REG: "https://vt.ncsbe.gov/RegLkup/",
					   POLLS: "https://vt.ncsbe.gov/PPLkup/"},
	"North Dakota": {CODE: "ND",
					 REG: "https://vip.sos.nd.gov/PortalListDetails.aspx?ptlhPKID=79&ptlPKID=7",
					 POLLS: "https://vip.sos.nd.gov/wheretovote.aspx"},
	"Ohio": {CODE: "OH",
			 REG: "https://voterlookup.ohiosos.gov/voterlookup.aspx",
			 POLLS: "https://voterlookup.ohiosos.gov/VoterLookup.aspx"},
	"Oklahoma": {CODE: "OK",
				 REG: "https://services.okelections.us/voterSearch.aspx",
				 POLLS: "https://okvoterportal.okelections.us/"},
	"Oregon": {CODE: "OR",
			   REG: "https://secure.sos.state.or.us/orestar/vr/showVoterSearch.do?source=SOS",
			   POLLS: "https://sos.oregon.gov/voting/Pages/drop-box-locator.aspx"},
	"Pennsylvania": {CODE: "PA",
					 REG: "https://www.pavoterservices.state.pa.us/Pages/VoterRegistrationStatus.aspx",
					 POLLS: "https://www.pavoterservices.pa.gov/Pages/PollingPlaceInfo.aspx"},
	"Puerto Rico": {CODE: "PR",
					REG: "http://consulta.ceepur.org/",
					REGDL: "http://ww2.ceepur.org/Home/EducacionElectoral",
					ABS: "http://ww2.ceepur.org/Home/SolicituddeVoto#VotoAusente",
					POLLS: "http://www.ceepur.org/directorio.htm"},
	"Rhode Island": {CODE: "RI",
					 REG: "https://vote.sos.ri.gov/Home/UpdateVoterRecord?ActiveFlag=0",
					 POLLS: "https://vote.sos.ri.gov/Home/PollingPlaces?ActiveFlag=2"},
	"South Carolina": {CODE: "SC",
					   REG: "https://info.scvotes.sc.gov/eng/voterinquiry/VoterInformationRequest.aspx"
							  "?PagMode=VoterInfo",
					   POLLS: "https://info.scvotes.sc.gov/eng/voterinquiry/VoterInformationRequest.aspx"
								"?PageMode=VoterInfo"},
	"South Dakota": {CODE: "SD",
					 REG: "https://vip.sdsos.gov/viplogin.aspx",
					 POLLS: "https://vip.sdsos.gov/viplogin.aspx"},
	"Tennessee": {CODE: "TN",
				  REG: "https://tnmap.tn.gov/voterlookup/",
				  POLLS: "https://web.go-vote-tn.elections.tn.gov/"},
	"Texas": {CODE: "TX",
			  REG: "https://teamrv-mvp.sos.texas.gov/MVP/mvp.do",
			  POLLS: "https://teamrv-mvp.sos.texas.gov/MVP/mvp.do"},
	"Utah": {CODE: "UT",
			 REG: "https://votesearch.utah.gov/voter-search/search/search-by-voter/voter-info",
			 POLLS: "https://votesearch.utah.gov/voter-search/search/search-by-address/how-and-where-can-i-vote"},
	"Vermont": {CODE: "VT",
				REG: "https://mvp.sec.state.vt.us/",
				POLLS: "https://mvp.sec.state.vt.us/"},
	"Virginia": {CODE: "VA",
				 REG: "https://vote.elections.virginia.gov/VoterInformation",
				 POLLS: "https://www.elections.virginia.gov/casting-a-ballot/"},
	"Washington": {CODE: "WA",
				   REG: "https://www.sos.wa.gov/elections/myvote/",
				   POLLS: "https://www.sos.wa.gov/elections/auditors/"},
	"West Virginia": {CODE: "WV",
					  REG: "https://apps.sos.wv.gov/elections/voter/",
					  POLLS: "https://services.sos.wv.gov/Elections/Voter/FindMyPollingPlace"},
	"Wisconsin": {CODE: "WI",
				  REG: "https://myvote.wi.gov/en-US/RegisterToVote",
				  POLLS: "https://myvote.wi.gov/en-US/FindMyPollingPlace"},
	"Wyoming": {CODE: "WY",
				REG: "https://sos.wyo.gov/Elections/Docs/WYCountyClerks.pdf",
				POLLS: "https://soswy.state.wy.us/Elections/PollPlace/Default.aspx"}
}


# Now do some dynamic setup in the table
for k, v in URLS_BY_STATE.items():
	if ABS not in v:
		v[ABS] = absentee_ballot(k)
	if REGDL not in v:
		v[REGDL] = reg_deadline(k)
	if ABROAD not in v:
		v[ABROAD] = abroad(k)
	if VOTE_STATE not in v:
		v[VOTE_STATE] = vote_state(k)
