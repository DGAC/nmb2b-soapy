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

# -------------------------------------------------------------------
# -------------------------------------------------------------------

# def do_day( when="today"):
# 		''' c'est du generique => le sortir de la classe NMB2B'''
# 		aujourdhui  = datetime.datetime.utcnow()
# 		hier        = aujourdhui-datetime.timedelta(days=1)
# 		demain      = aujourdhui+datetime.timedelta(days=1)
# 		ademain      = aujourdhui+datetime.timedelta(days=2)
# 		day		= None
# 		if when=='yesterday'        : day = hier
# 		elif when=='tomorrow'       : day = demain
# 		elif when=='+1'   		: day = demain
# 		elif when=='+2'     	: day = ademain
# 		else                        : day = aujourdhui
# 		return day.strftime("%Y-%m-%d" )

# def do_creneau( blocname, when="today"):
# 		''' c'est du generique => le sortir de la classe NMB2B'''
# 		start,endi  = None, None
# 		aujourdhui  = datetime.datetime.utcnow()
# 		hier        = aujourdhui-datetime.timedelta(days=1)
# 		demain      = aujourdhui+datetime.timedelta(days=1)
# 		sdemain      = aujourdhui+datetime.timedelta(days=2)
# 		day         = None
# 		starttime   = "00"
# 		endtime     = "00"
# 		deltaj	= datetime.timedelta(days=1)

# 		if when.startswith("H") and len(when)==2 and int(when[1]) in range(10):
# 			starttime = "0"+when[1]
# 			endtime   = "0%d"%(int(when[1])+1)
# 			deltaj	= 0
# 		if when.startswith("H") and len(when)==3 and int(when[1:]) in range(10,23):
# 			starttime = when[1:]
# 			endtime   = "%d"%(int(when[1:])+1)
# 			deltaj	= 0

# 		if when=='yesterday'        : day = hier
# 		elif when=='tomorrow'       : day = demain
# 		else                        : day = aujourdhui

# 		mstart      = "%Y-%m-%d" +" %s:00"%starttime
# 		start       = datetime.datetime.strftime(day, mstart)
# 		end         = datetime.datetime.strftime(day+deltaj, "%Y-%m-%d" +" %s:00"%endtime)
# 		return "<%s><wef>%s</wef><unt>%s</unt></%s>"%(blocname, start, end, blocname)

# def autocreneau( when='today'):
# 		 ''' c'est du generique => le sortir de la classe NMB2B'''
# 		 if when=="today":
# 			 pass
# 		 if when=="yesterday":
# 			 pass
# 		 if when=="tomorrow":
# 			 pass

# def autosendtime():
# 		ladate	= "%s"%datetime.datetime.utcnow()
# 		return	"<sendTime>%s</sendTime>"%(ladate[:19])
		 
# def to_file( filename, data):
# 			fic       = open(filename , "w")
# 			fic       . write(data)
# 			fic       . close()

# def save_metrics_to_es(metrics):
# 	# TODO : QUID de l'adresse IP ?
# 	es	= Elasticsearch(host="100.1.1.10")
# 	res = es.index(index="nmrequest", doc_type="log", body=metrics)

# def checkdate_YYYYMMDD(ladate):
# 	return re.match("\d{4}-\d{2}-\d{2}", ladate) is not None
	
# def gere_main_args():
# 	p = argparse.ArgumentParser()
# 	p.add_argument( '--proxy', dest='proxy',  default=None)
# 	p.add_argument('--elastic-ip', dest='elip',  default=None)
# 	p.add_argument('--elastic-port', dest='elport',  default=None)
# 	p.add_argument('--use-metrics', dest='usemetrics', default="no")
# 	return  p.parse_args()

# def do_dsnaproxy(C):
# 	return { 'http':'http://proxy.%s.aviation:8080'%C, 'https': 'https://proxy.%s.aviation:8080'%C }

# dsnaproxies     = {
# 	"doec"        : do_dsnaproxy("crna-n"),
# 	"crna-n"      : do_dsnaproxy("crna-n"),
# 	"crna-e"      : do_dsnaproxy("crna-e"),
# }

# nmb2bnamespaces={
# 			"fw"	: "eurocontrol/cfmu/b2b/FlowServices" ,
# 			"as"	: "eurocontrol/cfmu/b2b/AirspaceServices"  ,
# 			"fl"	: "eurocontrol/cfmu/b2b/FlightServices",
# 			"gi"	: "eurocontrol/cfmu/b2b/GeneralinformationServices" ,
# 			"cm"	: "eurocontrol/cfmu/b2b/CommonServices",
# 			"ns0"	: "http://www.fixm.aero/base/4.0" ,
# 			"ns2"	: "http://www.fixm.aero/flight/4.0",
# 			"xsi"	: "http://www.w3.org/2001/XMLSchema-instance",
# 			"S"	: "http://schemas.xmlsoap.org/soap/envelope/",
# 			"ps"	: "eurocontrol/cfmu/b2b/PublishsubscribeServices"
# }


# def envelopper(self, req):
# 		''' remplacer la partie namespaces en constante , ca allegera le code '''
# 		return '''<soapenv:Envelope 
# xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
# xmlns:as="eurocontrol/cfmu/b2b/AirspaceServices" 
# xmlns:cm="eurocontrol/cfmu/b2b/CommonServices" 
# xmlns:fl="eurocontrol/cfmu/b2b/FlightServices" 
# xmlns:flow="eurocontrol/cfmu/b2b/FlowServices"  
# xmlns:fw="eurocontrol/cfmu/b2b/FlowServices" 
# xmlns:gi="eurocontrol/cfmu/b2b/GeneralinformationServices"
# xmlns:ns9="http://www.fixm.aero/flight/4.0" 
# xmlns:ns10="http://www.fixm.aero/base/4.0" 
# xmlns:ns11="http://www.fixm.aero/eurextension/4.0" 
# xmlns:ps="eurocontrol/cfmu/b2b/PublishsubscribeServices" 
# xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
# xmlns:flig="eurocontrol/cfmu/b2b/FlightServices"  

# > <soapenv:Header/><soapenv:Body>%s</soapenv:Body></soapenv:Envelope>'''%(req)
		 

# def save_xml(self):
# 		if not self.request is None :
# 			requestfilename	= "requetes/request-%s-%s.xml"%(self.name, self.request["ts-start"])
# 			responsefilename	= "requetes/response-%s-%s.xml"%(self.name, self.request["ts-start"])
# 			self.to_file(requestfilename, self.request["request"])
# 			self.to_file(responsefilename, self.request["data"])
		
# def logguer_metriques(self, requete):
# 		es	= Elasticsearch(host="100.1.1.10")
# 		res = es.index(index="nmrequest", doc_type="log",  body=requete)
