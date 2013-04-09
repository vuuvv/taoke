'''
Created by auto_sdk on 2013-04-08 16:46:27
'''
from top.api.base import RestApi
class LogisticsTraceSearchRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.seller_nick = None
		self.tid = None

	def getapiname(self):
		return 'taobao.logistics.trace.search'
