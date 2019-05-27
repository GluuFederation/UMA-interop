#!/usr/bin/python
from helper import *
from config import *

display_header()

ticket = ''


def handle_claims_gathering_response():
    global ticket
    if is_ticket_in_url():
        arguments = cgi.FieldStorage()
        ticket = arguments['ticket'].value

        # Here is my PCT token!
        # Client attempts to get RPT at UMA /token endpoint, this time presenting the PCT
        # display_action_name("Client attempts to get RPT at UMA /token endpoint, this time presenting the PCT")

host = is_claim_in_url()
handle_claims_gathering_response()

# Client calls API without RPT token
as_uri = as_uri()

if not is_ticket_in_url():
    as_uri, ticket, _ = tokenless_resource_request(host=host)

# Get Client Credential for token endpoint 
def client_basic_header(cid, cs): 
    return "Basic %s" % base64.b64encode("%s:%s" % (cid, cs))

client_authz=client_basic_header(client_id(), client_secret())
if ce_url():
    client_authz = "Bearer " + get_permission_access_token()

# Client calls AS UMA /token endpoint with permission ticket and client credentials
need_info, token, redirect_url, ticket_two = get_rpt(as_uri, client_authz, ticket)

if not need_info:
    # Client calls API Gateway with RPT token
    rpt_resource_request(host=host, rpt=token)
else:
    # No RPT for you!  Go directly to Claims Gathering!
    # AS returns needs_info with claims gathering URI, which the user should
    # put in his browser. Link shorter would be nice if the user has to type it in.    
    display_redirect_link(redirect_url, ticket_two)

display_footer()
