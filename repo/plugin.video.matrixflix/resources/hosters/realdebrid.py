# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import requests

from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog

class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'realdebrid', 'RealDebrid', 'violet')
        self.__sRealHost = ''

    def setRealHost(self, host):
        self.__sRealHost = "/" + host

    def setDisplayName(self, displayName):
        self._displayName = displayName + ' [COLOR violet]'+ self._defaultDisplayName + self.__sRealHost + '[/COLOR]'
        
    def _getMediaLinkForGuest(self, autoPlay = False):
        token = cPremiumHandler(self.getPluginIdentifier()).getToken()
        if not token:
            return False, False

        headers = {'Authorization': 'Bearer %s' %token}
        data = {'link': self._url, 'password':''}
        r = requests.post('https://api.real-debrid.com/rest/1.0/unrestrict/link', data=data, headers=headers)
        dictData = r.json()
        if 'error' in dictData.keys():
            dialog().VSinfo(dictData['error'].upper().replace('_', ' '), self.getPluginIdentifier())

            return False, self._url
        else:
            api_call= dictData['download'] 

        if api_call:
            try:
                mediaDisplay = api_call.split('/')
                VSlog('Hoster RealDebrid - play : %s/ ... /%s' % ('/'.join(mediaDisplay[0:3]), mediaDisplay[-1]))
            except:
                VSlog('Hoster RealDebrid - play failed')

        return True, api_call

