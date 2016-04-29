# -*- coding: utf-8 -*-
from __future__ import (division, print_function, unicode_literals)
#############################################################################
# Author  : Jerome ODIER, Jerome FULACHIER, Fabian LAMBERT, Solveig ALBRAND
#
# Email   : jerome.odier@lpsc.in2p3.fr
#           jerome.fulachier@lpsc.in2p3.fr
#           fabian.lambert@lpsc.in2p3.fr
#           solveig.albrand@lpsc.in2p3.fr
#
# Version : 5.X.X (2014)
#
#############################################################################

import ssl, sys, pyAMI.config, pyAMI.exception

if sys.version_info[0] == 3:
	import http.client as http_client
else:
	import   httplib   as http_client

#############################################################################

headers = {
	'Accept': 'text/plain',
	'User-Agent': 'pyAMI/%s' % pyAMI.config.version,
	'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
}

#############################################################################

class HttpClient(object):
	#####################################################################

	def __init__(self, config):
		self.config = config

		self.endpoint = None
		self.connection = None

	#####################################################################

	def _connect(self):
		#############################################################
		# HTTP CONNECTION                                           #
		#############################################################

		if   self.endpoint['prot'] == 'http':

			self.connection = http_client.HTTPConnection(
				str(self.endpoint['host']),
				int(self.endpoint['port'])
			)

		#############################################################
		# HTTPS CONNECTION                                          #
		#############################################################

		elif self.endpoint['prot'] == 'https':

			if self.config.conn_mode == self.config.CONN_MODE_LOGIN:
				#############################################
				# WITHOUT CERTIFICATE                       #
				#############################################

				try:
					context = ssl._create_unverified_context(protocol = ssl.PROTOCOL_TLSv1)

					self.connection = http_client.HTTPSConnection(
						str(self.endpoint['host']),
						int(self.endpoint['port']),
						key_file = None,
						cert_file = None,
						context = context
					)

				except AttributeError as e:

					self.connection = http_client.HTTPSConnection(
						str(self.endpoint['host']),
						int(self.endpoint['port']),
						key_file = None,
						cert_file = None
					)

			else:
				#############################################
				# WITH CERTIFICATE                          #
				#############################################

				try:
					context = ssl._create_unverified_context(protocol = ssl.PROTOCOL_TLSv1)

					self.connection = http_client.HTTPSConnection(
						str(self.endpoint['host']),
						int(self.endpoint['port']),
						key_file = self.config.key_file,
						cert_file = self.config.cert_file,
						context = context
					)

				except AttributeError as e:

					self.connection = http_client.HTTPSConnection(
						str(self.endpoint['host']),
						int(self.endpoint['port']),
						key_file = self.config.key_file,
						cert_file = self.config.cert_file
					)

		#############################################################

		else:
			raise pyAMI.exception.Error('invalid endpoint protocol `%s`, not in [http, https]' % self.endpoint['prot'])


	#####################################################################

	def connect(self):
		i = 0x000000000000000000000000
		l = len(self.config.endpoints)

		while i < l:
			#####################################################
			# GET ENDPOINT                                      #
			#####################################################

			self.endpoint = pyAMI.config.endpoint_descrs[
				self.config.endpoints[i]
			]

			i += 1

			#####################################################
			# CONNECT                                           #
			#####################################################

			try:
				self._connect()

				return

			except Exception as e:

				if i == l:
					raise e

	#####################################################################

	def close(self):
		self.connection.close()

	#####################################################################

	def request(self, data):
		#############################################################
		# DO REQUEST                                                #
		#############################################################

		headers['Cookie'] = self.config.jsid

		try:
			self.connection.request('POST', self.endpoint['path'], data, headers)

		except Exception as e:
			raise pyAMI.exception.Error('could not connect to `%s://%s:%s%s`: %s' % (
				self.endpoint['prot'],
				self.endpoint['host'],
				self.endpoint['port'],
				self.endpoint['path'],
				e
			))

		#############################################################
		# GET RESPONSE AND COOKIE                                   #
		#############################################################

		result = self.connection.getresponse()

		self.config.jsid = result.getheader('set-cookie')

		#############################################################

		return result

#############################################################################
