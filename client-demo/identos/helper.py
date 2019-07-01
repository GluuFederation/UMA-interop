import requests
import json
import base64
from urllib import urlencode
import urlparse 

from config import *


def display_header():
    print "Content-type:text/html\r\n\r\n"
    print '''
    <html>
    <head>
        <title>Demo UMA Client CGI Program</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>
    </head>
    <body>
        <nav class="navbar navbar-light bg-success"><a class="text-white navbar-brand" href="/cgi-bin/index.py">UMA Client Demo</a></nav>
        <div class="container">
    '''


def display_footer():
    print '''
    </div>
    </body>
    </html>
    '''


def display_action_name(name):
    print '''<br/><div class="card"><div class="card-body"><h3 class="text-success">%s</h3></div></div>''' % name

def display_url(url):
    print '''<div class="card"><div class="card-body">Click on Below URL <br/><a href="%s">%s</a></div></div>''' % (url, url)


def display_response(response, request):
    response_json = ""
    try:
        response_json = json.dumps(response.json(), indent=4)
    except ValueError:
        pass

    print '''
    <table class="table table-striped"  style=\"width: 100%; table-layout: fixed\">
    <tbody>
        <tr>
            <td width="200px">Request url:</td>
            <td>{request_url}</td>
        </tr>
        <tr>
            <td>Request headers:</td>
            <td style="overflow:scroll;">{request_headers}</td>
        </tr>
        <tr>
            <td>Request body:</td>
            <td><pre>{request_body}</pre></td>
        </tr>
        <tr>
            <td>Response status:</td>
            <td>{response_status}</td>
        </tr>
        <tr>
            <td>Response headers:</td>
            <td>{response_headers}</td>
        </tr>
        <tr>
            <td>Response body:</td>
            <td><pre>{response_body}</pre></td>
        </tr>
    </tbody>
    </table>
    '''.format(
        request_url=response.url,
        request_headers=str(response.request.headers),
        request_body=json.dumps(request, indent=4),
        response_status=str(response.status_code),
        response_headers=str(response.headers),
        response_body=response_json
    )

def parse_www_authenticate(www_authenticate):
    # expect WWW-Authenticate to have the form "UMA realm=a, ticket=b, as_uri=c"     
    before, _, after = www_authenticate.lstrip().partition("UMA")
    if len(after) == 0:
        return ("", "")

    parts = [x.lstrip().split("=") for x in after.split(",")]
    output = {x[0]:x[1].replace("\"", "") for x in parts}
    return output


def tokenless_resource_request(host):
    headers = {"Host": host}
    response = requests.get(("%s/%s" % (rs_url(), api_path())), headers)    

    display_action_name("Client calls RS API without RPT token")
    display_response(response, "")

    www_authenticate = response.headers["WWW-Authenticate"].lstrip()
    output = parse_www_authenticate(www_authenticate)

    return output["as_uri"], output["ticket"], output["realm"]


def get_permission_access_token():
    body = {"client_id": client_id(),
            "client_secret": client_secret(),
            "op_host": ce_url(),
            "scope": ["oxd", "openid"]}
    response = requests.post(("%s/%s" % (as_uri(), pat_endpoint())),
                             headers={"Content-Type": "application/json"},
                             json=body,
                             verify=False)
    # display_action_name("2. Authenticating client in oxd-server")
    # display_response(response, body)
    return response.json()['access_token']





def get_rpt(as_uri, authorization, ticket):
    body = {"oxd_id": client_oxd_id(),
            "grant_type": "urn:ietf:params:oauth:grant-type:uma-ticket",    
            "ticket": ticket}
    
    response = requests.post(("%s/%s" % (as_uri, rpt_endpoint())),
                             headers={"Content-Type": "application/json",
                                      "Authorization": authorization},
                             json=body,
                             verify=False)
    display_action_name("Client calls AS UMA /token endpoint with permission ticket and client credentials")
    display_response(response, body)

    if 'error' in response.json() and response.json()['error'] == "need_info":
        return True, "", response.json().get('redirect_user'), response.json().get("ticket")
    else:
        return False, response.json()['access_token'], "", ""



def display_redirect_link(redirect_url, ticket):
    # inspect the query string to ensure required values are set
    url_components = urlparse.urlparse(redirect_url)

    redirect_params = dict(urlparse.parse_qsl(url_components.query))
    redirect_params.setdefault("state", "hardcodedstate")
    redirect_params.setdefault("ticket", ticket)
    redirect_params.setdefault("claims_redirect_uri", claims_redirect_url())
    redirect_params.setdefault("client_id" , client_id())

    url_parts = list(url_components)
    url_parts[4] = urlencode(redirect_params) # 4= query

    # rebuild url with updated query    
    full_claim_redirectUrl = urlparse.urlunparse(url_parts)

    display_action_name("4. Claims gathering url")
    display_url(full_claim_redirectUrl)


def rpt_resource_request(host, rpt):
    response = requests.get(("%s/%s" % (rs_url(), api_path())),
                            headers={"Host": host, "Authorization": "Bearer %s" % rpt})
    display_action_name("Client calls RS API with RPT token.")
    display_response(response, "")
