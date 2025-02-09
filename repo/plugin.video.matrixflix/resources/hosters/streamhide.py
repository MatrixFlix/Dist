# coding: utf-8

from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.packer import cPacker
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog
from resources.lib.util import urlHostName
from resources.lib import random_ua

UA = random_ua.get_ua()

class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'streamhide', 'StreamHide')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)

        if ('/d/' in self._url):
            self._url = self._url.replace('/d/','/e/').split('_')[0]

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', f'https://{urlHostName(self._url)}/')
        oRequest.addHeaderEntry('Origin', f'https://{urlHostName(self._url)}')
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern = r'(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sHtmlContent = cPacker().unpack(aResult[1][0])

        sPattern = r'sources:\s*\[{file:\s*["\']([^"\']+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]
            return True, api_call

        return False, False
