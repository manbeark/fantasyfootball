from groupy.client import Client
from groupy.session import Session
import groupy


# my token cUtuFhTnf3wrg9wBW98K1Sxh19HWcnX5qLuzWs6p
# rox cox 88458162
# dynasty 59938845
# dynasty league bot = 5c1e656845f95d936520adc0d2
# rox cox bot = 603569ee2b02abbf8a4cb6a660

def dyn_post(botid='5c1e656845f95d936520adc0d2',text='',token='cUtuFhTnf3wrg9wBW98K1Sxh19HWcnX5qLuzWs6p'):
	if text == '':
		return
	else:
		session = Session(token)
		manager = groupy.api.bots.Bots(session)
		manager.post(bot_id=botid, text=text)

def rox_post(botid='603569ee2b02abbf8a4cb6a660',text='',token='cUtuFhTnf3wrg9wBW98K1Sxh19HWcnX5qLuzWs6p'):
	if text == '':
		return
	else:
		session = Session(token)
		manager = groupy.api.bots.Bots(session)
		manager.post(bot_id=botid, text=text)