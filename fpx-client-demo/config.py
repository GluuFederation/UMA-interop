import cgi



DEMOS = {
	"https://gluu.local.org:8553": {
		"as_uri": "https://gluu.local.org:8553",
		"pat_endpoint":"get-client-token",
		"rpt_endpoint":"uma-rp-get-rpt",

		# client reg
		"client_id": "@!FBA4.9EDD.24E7.909F!0001!64E0.493A!0008!BE4C.B4F6.E5CC.DB74",
		"client_secret": "1b3e24c2-5472-4c26-a33f-b0b1c0c2b1c3",
		"claims_redirect_url": "https://gluu.local.org/cgi-bin/index.py",

		"client_oxd_id": "91b14554-17ac-4cf4-917d-f1b27e95902a",
		"ce_url": "https://gluu.local.org",

		# rs config
		"rs_url": "http://gluu.local.org:8000" ,
		"api_path": "posts/1",
		# Kong route register with below host
		"host_with_claims" 	: "gathering.example.com",
		"host_without_claims" : "non-gathering.example.com"

	},
	"https://idnserver.fpe.dev.identos.ca": {
		"as_uri": "https://idnserver.fpe.dev.identos.ca",
		"pat_endpoint":"transaction/token",
		"rpt_endpoint":"transaction/token",

		# client reg
		"client_id": "canimmunize-client-id",
		"client_secret": "canimmunize-client-secret",
		"claims_redirect_url": "http://localhost:8000/cgi-bin/index.py",

		# rs config
		"rs_url": "https://rs-moh.fpe.dev.identos.ca",
		"api_path": "api/immunization",

		"host_with_claims" 	: "rs-moh.fpe.dev.identos.ca",
		"host_without_claims" : "rs-moh.fpe.dev.identos.ca"		
	}

}

SELECTED_CONFIG="https://idnserver.fpe.dev.identos.ca"

client_settings=DEMOS[SELECTED_CONFIG]

# RS CONFIG
def rs_url():
	return client_settings["rs_url"]

def api_path():
	return client_settings["api_path"]

def host_with_claims():
	try:
		return client_settings["host_with_claims"]
	except KeyError:
		return rs_url()

def host_without_claims():
	try:
		return client_settings["host_without_claims"]
	except KeyError:
		return rs_url()	



# AS CONFIG

def as_uri():
	return client_settings["as_uri"]
def pat_endpoint():
	return client_settings["pat_endpoint"]
def rpt_endpoint():
	return client_settings["rpt_endpoint"]

# CLIENT CONFIG
def client_id():
	return client_settings["client_id"]
def client_secret():
	return client_settings["client_secret"]
def claims_redirect_url():
	return client_settings["claims_redirect_url"]


def ce_url ():
	return client_settings["ce_url "]
def ce_token_path():
	return client_settings["ce_token_path"] 
def client_oxd_id ():
	try:
		return client_settings["client_oxd_id"]
	except KeyError:
		return client_id()		



def is_ticket_in_url():
    arguments = cgi.FieldStorage()
    return 'ticket' in arguments


def is_claim_in_url():
    arguments = cgi.FieldStorage()
    if 'claim' in arguments or 'ticket' in arguments:
        return host_with_claims()
    else:
        return host_without_claims()

