'''
Created by auto_sdk on 2013-04-08 16:46:27
'''
from top.api.base import RestApi
class FenxiaoOrderRemarkUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.purchase_order_id = None
		self.supplier_memo = None
		self.supplier_memo_flag = None

	def getapiname(self):
		return 'taobao.fenxiao.order.remark.update'
