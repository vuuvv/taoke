'''
Created by auto_sdk on 2013-04-08 16:46:27
'''
from top.api.base import RestApi
class SimbaCampaignAreaGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.campaign_id = None
		self.nick = None

	def getapiname(self):
		return 'taobao.simba.campaign.area.get'
