'''
Created by auto_sdk on 2013-04-08 16:46:27
'''
from top.api.base import RestApi
class AlipayEbppBillPayRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.alipay_order_no = None
		self.auth_token = None
		self.merchant_order_no = None
		self.order_type = None

	def getapiname(self):
		return 'alipay.ebpp.bill.pay'
