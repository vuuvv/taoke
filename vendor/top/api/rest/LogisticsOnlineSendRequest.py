'''
Created by auto_sdk on 2013-04-08 16:46:27
'''
from top.api.base import RestApi
class LogisticsOnlineSendRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.cancel_id = None
		self.company_code = None
		self.feature = None
		self.out_sid = None
		self.seller_ip = None
		self.sender_id = None
		self.tid = None

	def getapiname(self):
		return 'taobao.logistics.online.send'
