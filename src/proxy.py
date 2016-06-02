'''
The original version of this file is taken from
https://www.github.com/gciotta/jsonrpc-requests
and modified in order to reuse the JSON RPC proxy to send the
commands to Kodi API directly.

Copyright (c) 2014 Giuseppe Ciotta <gciotta@gmail.com>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. The name of the author may not be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import random
import sys
import json
import functools
import requests

class JSONRPCError(Exception):
    """Root exception for all errors related to this library"""

class TransportError(JSONRPCError):
    """An error occurred while performing a connection to the server"""

class ProtocolError(JSONRPCError):
    """An error occurred while dealing with the JSON-RPC protocol"""

class Proxy(object):

    def send_request(self, method_name, is_notification, params):
        ''''Will be overiden by subclasses'''''
        pass

    def deserialize(self, result):
        """Parse the data returned by the server according to the JSON-RPC spec. Try to be liberal in what we accept."""
        if not isinstance(result, dict):
            raise ProtocolError('Response is not a dictionary')
        if result.get('error'):
            code = result['error'].get('code', '')
            message = result['error'].get('message', '')
            raise ProtocolError(code, message, result)
        elif 'result' not in result:
            raise ProtocolError('Response without a result field')
        else:
            return result['result']

    @staticmethod
    def dumps(data):
        """Override this method to customize the serialization process (eg. datetime handling)"""
        return json.dumps(data)

    def serialize(self, method_name, params, is_notification):
        """Generate the raw JSON message to be sent to the server"""
        data = {'jsonrpc': '2.0', 'method': method_name}
        if params:
            data['params'] = params
        if not is_notification:
            # some JSON-RPC servers complain when receiving str(uuid.uuid4()). Let's pick something simpler.
            data['id'] = random.randint(1, sys.maxsize)
        return self.dumps(data)

    def __getattr__(self, method_name):
        return Method(self.__request, method_name)

    def __request(self, method_name, args=None, kwargs=None):
        """Perform the actual RPC call. If _notification=True, send a notification and don't wait for a response"""
        is_notification = kwargs.pop('_notification', False)
        if args and kwargs:
            raise ProtocolError('JSON-RPC spec forbids mixing arguments and keyword arguments')
        return self.send_request(method_name, is_notification, args or kwargs)

class Server(Proxy):
    """A connection to a HTTP JSON-RPC server, backed by requests"""

    def __init__(self, url, session=None, **requests_kwargs):
        self.session = session or requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json-rpc',
        })
        self.request = functools.partial(self.session.post, url, **requests_kwargs)

    def send_request(self, method_name, is_notification, params):
        """Issue the HTTP request to the server and return the method result (if not a notification)"""
        request_body = self.serialize(method_name, params, is_notification)
        try:
            response = self.request(data=request_body)
        except requests.RequestException as requests_exception:
            raise TransportError('Error calling method %r' % method_name, requests_exception)

        if response.status_code != requests.codes.ok:
            raise TransportError(response.status_code)

        if not is_notification:
            try:
                parsed = response.json()
            except ValueError as value_error:
                raise TransportError('Cannot deserialize response body', value_error)

            return self.deserialize(parsed)

class Local(Proxy):

    def __init__(self, xbmc):
        self._xbmc = xbmc

    def send_request(self, method_name, is_notification, params):
        if is_notification:
            raise ProtocolError('Kodi does not support notifications for local JSON-RPC calls')

        request_body = self.serialize(method_name, params, is_notification)
        try:
            response = self._xbmc.executeJSONRPC(request)
        except Exception as requests_exception:
            raise TransportError('Error calling method %r' % method_name, requests_exception)

        parsed = json.loads(response)
        return self.deserialize(parsed)

class Method(object):
    def __init__(self, request_method, method_name):
        if method_name.startswith("_"):  # prevent rpc-calls for private methods
            raise AttributeError("invalid attribute '%s'" % method_name)
        self.__request_method = request_method
        self.__method_name = method_name

    def __getattr__(self, method_name):
        if method_name.startswith("_"):  # prevent rpc-calls for private methods
            raise AttributeError("invalid attribute '%s'" % method_name)
        return Method(self.__request_method, "%s.%s" % (self.__method_name, method_name))

    def __call__(self, *args, **kwargs):
        return self.__request_method(self.__method_name, args, kwargs)

