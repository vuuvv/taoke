'''
Created by auto_sdk on 2013-04-08 16:46:27
'''
from top.api.base import RestApi
class WlbOrderitemPageGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.order_code = None
		self.page_no = None
		self.page_size = None

	def getapiname(self):
		return 'taobao.wlb.orderitem.page.get'
