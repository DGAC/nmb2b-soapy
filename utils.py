#!/usr/bin/env python
#-*- coding: utf-8 -*-

import datetime
import os

from shared_vars import DATA_PATH


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

def format_datetime_for_nm(datetime_to_format):
	# TODO : affiner les warnings, messages d'erreurs etc
	
	if type(datetime_to_format) == str:
		# TODO : vérifier que le format correspond bien à ce qui est attendu par NM
		return datetime_to_format
	
	elif isinstance(datetime_to_format, datetime.datetime):
		if datetime_to_format.tzinfo != datetime.timezone.utc:
			print("Attention : l'objet datetime.datetime que vous avez passé en argument n'est pas formaté UTC.")
		return datetime_to_format.strftime("%Y-%m-%d %H:%M")
	
	else:
		print("La date+heure que vous avez passé en argument n'est pas un format \
			accepté par soapy (str ou objet datetime.datetime).")
		# TODO rapidement : lever une exception plutôt 
		exit(1)