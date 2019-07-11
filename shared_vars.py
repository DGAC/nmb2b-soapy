#-*- coding: utf-8 -*-
import os

# -------------------------------------------------------------------
B2B_PROXY = None
NM_B2B_API_KEY_ID = os.environ.get('NM_B2B_API_KEY_ID')  # default is None
NM_B2B_API_SECRET = os.environ.get('NM_B2B_API_SECRET')  # default is None
if NM_B2B_API_KEY_ID and NM_B2B_API_SECRET:
	B2B_PROXY = {
		'key': 		NM_B2B_API_KEY_ID,
		'secret': 	NM_B2B_API_SECRET
	}
	

DEFAULT_B2B_VERSION = '23.0.0'

WSDL_PROXY = "https://wsdl.b2b-proxy.4me.im/23.0.0/"



# -------------------------------------------------------------------
ALLOWED_DATASET = ["OPERATIONAL"]
DEFAULT_DATASET = "OPERATIONAL"
def get_dataset(wanted_dataset):
	if wanted_dataset in ALLOWED_DATASET: return wanted_dataset
	return "OPERATIONAL"