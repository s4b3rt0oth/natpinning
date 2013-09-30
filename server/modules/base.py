#!/usr/bin/env python
#filename=base.py

from __future__ import with_statement
from threading import Thread
import random
import socket
import time
import contextlib
import exceptions
import subprocess
import asyncore

class Base(asyncore.dispatcher):
	def __init__(self,sType, serverPort,sCallbackType):
		asyncore.dispatcher.__init__(self)
		self.sPort = int(serverPort)
		self.CB_TYPE=sCallbackType #socket, ssh, telnet TODO
		if sType =="TCP" or sType == "UDP": self.pType = sType
        	try:
	        	self.create_socket(socket.AF_INET6, socket.SOCK_STREAM)
			self.set_reuse_addr()
	        except AttributeError:
            		# AttributeError catches Python built without IPv6
            		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error:
			# socket.error catches OS with IPv6 disabled
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.bind(('', self.sPort))
		self.listen(5)
	#end def
	
	def handle_accept(self):
		self.log("Received connection from " + addr[0])
		self.protocolhandler(conn, addr)
	#end def
	def protocolhandler(self,conn, addr):
		pass
		#OVERRIDE THIS FUNCTION
	#end def
	def callback(self,sProto,sType,sIP,iPort):
		if sType == "socket":
			try:
				if ":" in sIP:
					cbsock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
				else:
					cbsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				cbsock.connect((sIP,iPort))
				self.log(sProto + ": Callback success on: " + sIP + " port " +str(iPort))
				cbsock.close()
			except socket.error:
				self.log(sProto + ": Callback failed on: " + sIP + " port " +str(iPort))
		elif sType=="ssh":
			try:
				launchcmd=["ssh", "root@"+sIP, "-p", str(iPort)]
				p = subprocess.Popen(launchcmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				print p.stdout.readline
				p.close()
				self.log(sProto + ": Callback success on: " + sIP + " port " +str(iPort))
			except:
				self.log(sProto + ": Callback failed on: " + sIP + " port " +str(iPort))
	#end def
	def log(self, str):
        	print str
	#end def
#end class
