import os, sys
sys.path.insert(0, os.path.abspath('../src'))

import kodi
import jsonrpc_requests as rpc

class Kodi(kodi.Kodi):
	def __init__(self, host, user, pwd):
		proxy = rpc.Server(host, auth=(user, pwd))
		super().__init__(proxy)
