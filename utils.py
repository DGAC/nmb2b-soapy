#!/usr/bin/env python
#-*- coding: utf-8 -*-

import argparse
import datetime
import logging
import os
import re
import sys
import xml.etree.ElementTree as ET

import requests
#from elasticsearch import Elasticsearch

#from decolog import *
#from dsnaproxies import dsnaproxies
from shared_vars import DATA_PATH


# -------------------------------------------------------------------
# -------------------------------------------------------------------
# Nouveaux utilitaires par Maxence
def write_content_to_file(filename, content, rep=DATA_PATH):
	os.makedirs(os.path.dirname(rep+filename), exist_ok=True)
	full_path = os.path.join(rep, filename)
	with open(full_path, 'w') as file_to_be_written:
		file_to_be_written.write(content)
 
def get_datetime(nbr_days=0):
	'''
	Retourne une datetime avec + ou - le nombre de jours indiqué en arg.
	'''
	datetime_to_return = datetime.datetime.utcnow()
	if nbr_days < 0:
		datetime_to_return -= datetime.timedelta(days=abs(nbr_days))
	elif nbr_days > 0:
		datetime_to_return += datetime.timedelta(days=abs(nbr_days))
	return datetime_to_return.strftime("%Y-%m-%d")

def sendTime():
	sendTime = f"{datetime.datetime.utcnow().replace(microsecond=0)}"
	return sendTime[:19]