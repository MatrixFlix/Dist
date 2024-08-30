#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog

UA = 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vimeo', 'Vimeo')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = False
        sReferer = ""
        url = self._url.split('|Referer=')[0]
        sReferer = self._url.split('|Referer=')[1]

        oParser = cParser()
        oRequest = cRequestHandler(url)
        oRequest.addHeaderEntry('Host', 'vimeo.com')
        oRequest.addHeaderEntry('Referer', sReferer)
        oRequest.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequest.request()

        sPattern = '"config":"(.+?)",'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            web_url = aResult[1][0]

        oRequest = cRequestHandler(web_url)
        oRequest.addHeaderEntry('Referer', 'https://vimeo.com/')
        oRequest.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequest.request(jsonDecode=True)
        for cdn in sHtmlContent['request']['files']['hls']['cdns'].values():
            url=[]
            qua=[]
            url.append(str(cdn["url"]))
            qua.append(str(cdn["origin"]))

        api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
