from xml.etree import ElementTree

API_KEY = ""

API_SECRET = ""

BEARER_TOKEN = ""

ACCESS_TOKEN = ""

ACCESS_SECRET = ""

def loadKeys(keysPath):
	global API_KEY, API_SECRET, BEARER_TOKEN, ACCESS_TOKEN, ACCESS_SECRET

	tree = ElementTree.parse(keysPath)
	root = tree.getroot()
	if root.tag != "credentials":
		raise NameError(f"Keys document starts with {root.tag}")

	twitterCreds = list(root)[0]
	for cred in list(twitterCreds):
		if cred.tag == "apiKey":
			API_KEY = cred.text
		elif cred.tag == "apiSecret":
			API_SECRET = cred.text
		elif cred.tag == "bearerToken":
			BEARER_TOKEN = cred.text
		elif cred.tag == "accessToken":
			ACCESS_TOKEN = cred.text
		elif cred.tag == "accessSecret":
			ACCESS_SECRET = cred.text
		else:
			raise NameError(f"Keys document contains bad element {cred.tag}")
