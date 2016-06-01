import kodi
import json
import logging

class Kodi(kodi.Kodi):
	def __init__(self, xbmc):
		proxy = _Proxy(xbmc)
		kodi.Kodi.__init__(self, proxy)

class _Proxy:
	def __init__(self, xbmc):
		self._xbmc = xbmc
		self._id = 0
	def _send_request(self, methodName, params):
		request = self.serialize(methodName, params)
		logging.debug("Sending: {0}".format(request))
		response = self._xbmc.executeJSONRPC(request)
		logging.debug("Receiving: {0}".format(response))
		return self.deserialize(response)
	def serialize(self, methodName, params):
		data = {'jsonrpc': '2.0', 'method': methodName}
		if params:
			data['params'] = params
		self._id += 1
		data['id'] = self._id
		return json.dumps(data)
	def deserialize(self, response):
		responseJson = json.loads(response)
		if responseJson.get('error'):
			code = responseJson['error'].get('code', '')
			message = responseJson['error'].get('message', '')
			raise Exception(code, message, responseJson)
		else:
			return responseJson['result']
	def __getattr__(self, methodName):
		return _Method(self._request, methodName)
	def _request(self, methodName, args=None, kwargs=None):
		return self._send_request(methodName, args or kwargs)

class _Method:
	def __init__(self, requestMethod, methodName):
		if methodName.startswith("_"):
			raise AttributeError("Internal attribute '{}'".format(methodName))
		self._requestMethod = requestMethod
		self._methodName = methodName
	def __getattr__(self, methodName):
		if methodName.startswith("_"):
			raise AttributeError("Internal attribute '{}'".format(methodName))
		return _Method(self._requestMethod, "{0}.{1}".format(self._methodName, methodName))
	def __call__(self, *args, **kwargs):
		return self._requestMethod(self._methodName, args, kwargs)

