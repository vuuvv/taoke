'''
Created by auto_sdk on 2013-04-08 16:46:27
'''
from top.api.base import RestApi
class UmpRangeDeleteRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.act_id = None
		self.ids = None
		self.type = None

	def getapiname(self):
		return 'taobao.ump.range.delete'
