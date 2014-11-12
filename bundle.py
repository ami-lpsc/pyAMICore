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

import os, glob, subprocess, ctypes.util

#############################################################################

os.system('rm -fr pyAMI.app')

#############################################################################

os.system('mkdir pyAMI.app')
os.system('mkdir pyAMI.app/Contents')
os.system('mkdir pyAMI.app/Contents/MacOS')
os.system('mkdir pyAMI.app/Contents/Resources')
os.system('mkdir pyAMI.app/Contents/Resources/pyAMI')
os.system('mkdir pyAMI.app/Contents/Resources/PySide')
os.system('mkdir pyAMI.app/Contents/Frameworks')

#############################################################################

Info_plist = '''<?xml version="1.0" encoding="UTF-8"?>

<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">

<plist version="1.0">
  <dict>
    <key>CFBundleExecutable</key>
    <string>pyAMI</string>
    <key>CFBundleIconFile</key>
    <string>ami.icns</string>
    <key>CFBundleIdentifier</key>
    <string>pyAMI</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>pyAMI</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
  </dict>
</plist>
'''

PkgInfo = '''APPL????
'''

f = open('pyAMI.app/Contents/Info.plist', 'wt')
f.write(Info_plist)
f.close()

f = open('pyAMI.app/Contents/PkgInfo', 'wt')
f.write(PkgInfo)
f.close()

#############################################################################

pyami = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (division, print_function, unicode_literals)
#############################################################################

import os

#############################################################################

os.system('defaults write com.apple.versioner.python Prefer-32-Bit -bool no')

#############################################################################

BUNDLE_Contents = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/..')

BUNDLE_Frameworks = BUNDLE_Contents + '/Frameworks'
BUNDLE_Resources = BUNDLE_Contents + '/Resources'

#############################################################################

os.execve('%s/ami-internal' % BUNDLE_Resources, ['%s/ami-internal' % BUNDLE_Resources], {'DYLD_LIBRARY_PATH': '%s:%s' % (BUNDLE_Frameworks, BUNDLE_Resources)})

#############################################################################
'''

f = open('pyAMI.app/Contents/MacOS/pyAMI', 'wt')
f.write(pyami)
f.close()

os.system('chmod a+x pyAMI.app/Contents/MacOS/pyAMI')

#############################################################################

xslt = '''<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
'''

f = open('pyAMI.app/Contents/Resources/custom.xslt', 'wt')
f.write(xslt)
f.close()

#############################################################################

os.system('cp ami pyAMI.app/Contents/Resources')
os.system('cp ami.icns pyAMI.app/Contents/Resources')
os.system('cp ami-internal pyAMI.app/Contents/Resources')

#############################################################################

if True:
	import PySide
	pyside_dir = os.path.dirname(PySide.__file__)
	os.system('cp -R ' + pyside_dir + ' pyAMI.app/Contents/Resources')

if True:
	import IPython
	ipython_dir = os.path.dirname(IPython.__file__)
	os.system('cp -R ' + ipython_dir + ' pyAMI.app/Contents/Resources')

if True:
	import argparseplus
	argparseplus_dir = os.path.dirname(argparseplus.__file__)
	os.system('cp -R ' + argparseplus_dir + ' pyAMI.app/Contents/Resources')

if True:
	import tiny_xslt
	tiny_xslt_dir = os.path.dirname(tiny_xslt.__file__)
	os.system('cp -R ' + tiny_xslt_dir + ' pyAMI.app/Contents/Resources')

if True:
	import pyAMI
	pyami_dir = os.path.dirname(pyAMI.__file__)
	os.system('cp -R ' + pyami_dir + ' pyAMI.app/Contents/Resources')

#############################################################################

for dir_name, dir_names, file_names in os.walk('pyAMI.app/Contents/Resources'):

	for file_name in file_names:

		if file_name.endswith('.pyc'):

			os.remove(dir_name + '/' + file_name)

#############################################################################

def popen(command, STDIN = None, STDOUT = None, STDERR = None):

	p = subprocess.Popen(
		command,
		shell = False,
		stdin = STDIN,
		stdout = STDOUT,
		stderr = STDERR,
		universal_newlines = True
	)

	return p

#############################################################################

deps = set({})

for src in glob.glob(pyside_dir + '/*.so'):
	#####################################################################

	lib = os.path.basename(src)

	dst = 'pyAMI.app/Contents/Resources/PySide/%s' % lib

	os.system('install_name_tool -id @executable_path/../Resources/PySide/%s %s' % (lib, dst))

	#####################################################################

	lines = popen(['otool', '-L', src], STDOUT = subprocess.PIPE).communicate()[0].split('\n')

	for line in lines:

		data = line.split()

		if len(data) > 0 and (
		       data[0].find('pyside') >= 0
			or
		       data[0].find('shiboken') >= 0
		):
			deps.add(data[0])

#############################################################################

for lib in deps:
	src = ctypes.util.find_library(lib)

	dst = 'pyAMI.app/Contents/Frameworks/%s' % lib

	if not src is None:
		os.system('cp %s %s && install_name_tool -id @executable_path/../Frameworks/%s %s' % (src, dst, lib, dst))

#############################################################################
