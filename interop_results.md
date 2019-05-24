# UMA Interop Results

## Keycloak

### Overview of Results
What was tested was:

* Dynamic Client Registration
* Protection API
* Permission API
* UMA Grant Type
* Introspection Endpoint

Gluu Gateway was was able to:

* Dynamically register clients in Keycloak
* Manage protected resources through the Protection API
* Issue permission tickets through the Permission API
* Obtain an RPT using the UMA Grant Type
* Introspect the RPT, using our introspection endpoint, and check the granted permissions

### Custom adjustments

#### Keycloak
1. Dynamic client registration creates clients with "Authorization Enabled" set to true
2. Ignore unused json fields in requests (by default keycloak is throwing exception)
3. Change name of token-introspection url in OPIC and UMA discovery point
4. Create realm (in example name of realm is "oxd")

#### Gluu Gateway
1. OXD - Send "token_type_hint" = "requesting_party_token" parameter in order to be able to introspect RPT in Keycloak.
2. Gluu Gateway - Token type recognition

## Identos

### Overview of Results 

Overall very minor client differences required between the GLUU and IDENTOS implementations.

Client->RS: no differences
Client->AS: few differences (client authentication, rpt request and needs_info,redirect_user response)

### UMA Implementation Differences

#### Client authentication to AS

GLUU: Client must get an OAuth access token (using Client Credential Grant) before calling the RPT endpoint. This is because Gluu encourages clients to use private key authentication at the token endpoint, which cannot be accomplished via basic authentication.
IDENTOS: Client uses basic client credentials directly with RPT endpoint


#### RPT request

(UMA Grant 3.3.1 Client Request to Authorization Server for RPT)

GLUU: body includes ticket & "oxd_id"
IDENTOS: body includes ticket & "grant_type"


#### RPT response: needs_info, redirect_user

(UMA Grant 3.3.6 Authorization Server Response to Client on Authorization Failure)

GLUU: client can use the redirect_user uri directly without other processing (guessing this is just for demo?)
IDENTOS: returns the base url (same as the value in the well-known right now) without any params


*** Q: should this be a complete uri (eg ticket as query param) or just the endpoint and require the client to build the url?
	- the client must append additional data
		- state
		- redirect_uri (if only 1 registered, the AS *could*  append/assume)


#### Client->RS resource request

GLUU: client requests against the gluu-gateway and must include downstream Host param (I think?)
IDENTOS: no Host required, no knowledge of RS internals


### Other 'code' changes

- moved hardcoded AS endpoints (eg rpt endpoint) into the config.py (from helper.py)

- index.py, use as_uri from RPT-less resource request
	- even if the as_uri is used, on the callback the server hardcodes the AS location (no state atm)

- index.py, move redirect link creating & presentation into helper.py 
	- consistency with other methods

- helper.py display_response, handle exception when response json is not set

- helper.py get_ticket 
	- renamed to get_as_and_ticket
	- parse and return as_uri and ticket
	- improve www-authenticate header parsing

- helper.py add display_redirect_link function

