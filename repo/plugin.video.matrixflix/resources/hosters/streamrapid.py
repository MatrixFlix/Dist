#-*- coding: utf-8 -*-

from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'streamrapid', 'Rabbitstream/Dokicloud')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)

        api_call = self._url
        SubTitle = ''
        if ('sub.info' in self._url):
            SubTitle = self._url.split('sub.info=')[1]
            self._url = self._url.replace('+', '%2B').split('?sub.info=')[0]

        if api_call:
            if ('http' in SubTitle):
                return True, api_call, SubTitle
            else:
                return True, api_call

        return False, False
