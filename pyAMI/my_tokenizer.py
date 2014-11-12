# -*- coding: utf-8 -*-
from __future__ import (division, print_function, unicode_literals)
#############################################################################
# Author  : Jerome ODIER
#
# Email   : jerome.odier@cern.ch
#
#############################################################################

import pyAMI.exception

#############################################################################

def tokenize(s, spaces = [], symbols = [], strings = [], line = 1):
	result_tokens = []
	result_lines = []

	i = 0x0000
	l = len(s)

	word = ''

	while i < l:
		#############################################################
		# COUNT LINES                                               #
		#############################################################

		if s[i] == '\n':
			line += 1

		#############################################################
		# EAT SAPCES                                                #
		#############################################################

		if s[i] in spaces:

			if word:
				result_tokens.append(word)
				result_lines.append(line)
				word = ''

			i += 1

			continue

		#############################################################
		# EAT SYMBOLS                                               #
		#############################################################

		found = False

		for symbol in symbols:

			if s[i: ].startswith(symbol):

				if word:
					result_tokens.append(word)
					result_lines.append(line)
					word = ''

				j = i + len(symbol)

				result_tokens.append(s[i: j])
				result_lines.append(line)

				i = j

				found = True
				break

		if found:
			continue

		#############################################################
		# EAT STRINGS                                               #
		#############################################################

		found = False

		for string in strings:

			if s[i: ].startswith(string[0]):

				if word:
					result_tokens.append(word)
					result_lines.append(line)
					word = ''

				j = i + _shift(s[i: ], string, line)

				result_tokens.append(s[i: j])
				result_lines.append(line)

				i = j

				found = True
				break

		if found:
			continue

		#############################################################
		# EAT REMAINING CHARACTERES                                 #
		#############################################################

		word += s[i]
		i += 1

	#####################################################################

	if word:
		result_tokens.append(word)
		result_lines.append(line)

	return result_tokens, result_lines

#############################################################################

def _shift(s, group, line):
	result = len(group[0])

	while True:
		idx = s.find(group[1], result)

		if idx < 0:
			raise pyAMI.exception.Error('syntax error, line `%d`, missing token `%s`' % (line, group[1]))

		result = idx + len(group[1])

		if s[idx - 1] != '\\':
			break

	return result

#############################################################################
