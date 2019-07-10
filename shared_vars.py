#-*- coding: utf-8 -*-
import os

# -------------------------------------------------------------------
# PROXIES
def define_proxy(org_spef):
	return { 
		'http'	: f"http://{org_spef}.aviation:8080", 
		'https'	: f"http://{org_spef}.aviation:8080",
		'ftp'	: f"http://{org_spef}.aviation:8080"
	}
LOCAL_PROXIES = { 
	"doec"		: define_proxy("proxy.crna-n"),
	"crna-n"	: define_proxy("jules.lfpo"),
	"crna-e"	: define_proxy("proxy.crna-e"),
}
def get_local_proxy(org):
	return LOCAL_PROXIES[org]
DEFAULT_ORG="doec"

B2B_PROXY = None
NM_B2B_API_KEY_ID = os.environ.get('NM_B2B_API_KEY_ID')  # default is None
NM_B2B_API_SECRET = os.environ.get('NM_B2B_API_SECRET')  # default is None
if NM_B2B_API_KEY_ID and NM_B2B_API_SECRET:
	B2B_PROXY = {
		'key': 		NM_B2B_API_KEY_ID,
		'secret': 	NM_B2B_API_SECRET
	}
	

# -------------------------------------------------------------------
B2B_VERSIONS = ['20.5.0', '22.0.0', '23.0.0']
DEFAULT_B2B_VERSION = '23.0.0'
def get_entry_point(b2b_version):
		
	base = "https://www.b2b.preops.nm.eurocontrol.int"
	if B2B_PROXY: base = "https://b2b-proxy.4me.im"
	
	version = '23.0.0'
	if b2b_version in B2B_VERSIONS:
		version = b2b_version

	return base + "/B2B_PREOPS/gateway/spec/" + version
WSDL_PROXY = "https://wsdl.b2b-proxy.4me.im/23.0.0/"

# -------------------------------------------------------------------
# définition de quelques chemins utiles
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CERTS_PATH = (
	os.path.join(ROOT_PATH, 'cert', 'preops', 'cert-preops.pem'), 
	os.path.join(ROOT_PATH, 'cert', 'preops', 'plaincle.pem'))
DATA_PATH = os.path.join(ROOT_PATH, "data")
# REQUESTS_PATH = os.path.join(ROOT_PATH, "data", "requests")
# RESPONSES_PATH = os.path.join(ROOT_PATH, "data", "responses")


# -------------------------------------------------------------------
ALLOWED_DATASET = ["OPERATIONAL"]
DEFAULT_DATASET = "OPERATIONAL"
def get_dataset(wanted_dataset):
	if wanted_dataset in ALLOWED_DATASET: return wanted_dataset
	return "OPERATIONAL"


# -------------------------------------------------------------------
GENERIC_WRAPPER = '''
<soapenv:Envelope 
xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
xmlns:as="eurocontrol/cfmu/b2b/AirspaceServices" 
xmlns:cm="eurocontrol/cfmu/b2b/CommonServices" 
xmlns:fl="eurocontrol/cfmu/b2b/FlightServices" 
xmlns:flow="eurocontrol/cfmu/b2b/FlowServices"  
xmlns:fw="eurocontrol/cfmu/b2b/FlowServices" 
xmlns:gi="eurocontrol/cfmu/b2b/GeneralinformationServices"
xmlns:ns9="http://www.fixm.aero/flight/4.0" 
xmlns:ns10="http://www.fixm.aero/base/4.0" 
xmlns:ns11="http://www.fixm.aero/eurextension/4.0" 
xmlns:ps="eurocontrol/cfmu/b2b/PublishsubscribeServices" 
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns:flig="eurocontrol/cfmu/b2b/FlightServices">
	<soapenv:Header/>
	<soapenv:Body>{request_to_wrap}</soapenv:Body>
</soapenv:Envelope>
'''
