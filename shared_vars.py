#-*- coding: utf-8 -*-
import os

# -------------------------------------------------------------------
DEFAULT_B2B_VERSION = '23.0.0'
def get_available_b2b_version_for_soapy():
	return ['23.0.0']

# -------------------------------------------------------------------
WSDL_PROXY = "https://wsdl.b2b-proxy.4me.im/23.0.0/"
#WSLD_PREOPS_MAIN = "https://www.b2b.preops.nm.eurocontrol.int/"
WSDL_PREOPS_MAIN="https://www.b2b.preops.nm.eurocontrol.int/FILE_PREOPS/gateway/spec/b2b_publications/23.0.0/B2B_WSDL_XSD.23.0.0.5.81.tar.gz"
#WSLD_PREOPS_MAIN = "https://www.b2b.nm.eurocontrol.int/"

# -------------------------------------------------------------------
ALLOWED_DATASET = ["OPERATIONAL"]
DEFAULT_DATASET = "OPERATIONAL"
def get_dataset(wanted_dataset):
	if wanted_dataset in ALLOWED_DATASET: return wanted_dataset
	return "OPERATIONAL"

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(ROOT_PATH, "data")