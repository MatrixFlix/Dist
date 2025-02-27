#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, VSlog
from resources.lib.util import QuotePlus

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'rutube', 'RuTube')

    def setUrl(self, url):
        self._url = url
        self._url = self._url.replace('http://', '')
        self._url = self._url.replace('https://', '')
        self._url = self._url.replace('rutube.ru/video/embed/', '')
        self._url = self._url.replace('video.rutube.ru/', '')
        self._url = self._url.replace('rutube.ru/video/', '')
        self._url = self._url.replace('rutube.ru/play/embed/', '')
        self._url = 'http://rutube.ru/play/embed/' + str(self._url)

    def __getIdFromUrl(self, url):
        sPattern = "\/play\/embed\/(\w+)"
        oParser = cParser()
        aResult = oParser.parse(url, sPattern)
        if aResult[0]:
            return aResult[1][0]

        return ''

    def __getRestFromUrl(self, url):
        sPattern = "\?([^ ]+)"
        oParser = cParser()
        aResult = oParser.parse(url, sPattern)
        if aResult[0]:
            return aResult[1][0]

        return ''

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        stream_url = False

        oParser = cParser()

        sID = self.__getIdFromUrl(self._url)
        sRestUrl = self.__getRestFromUrl(self._url)

        api = 'http://rutube.ru/api/play/options/' + sID + '/?format=json&no_404=true&referer=' + QuotePlus(self._url)
        api = api + '&' + sRestUrl

        oRequest = cRequestHandler(api)
        sHtmlContent = oRequest.request()

        sPattern = '"m3u8": *"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if not (aResult):
            sPattern = '"default": *"([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            url2 = aResult[1][0]
        else:
            return False,False

        oRequest = cRequestHandler(url2)
        sHtmlContent = oRequest.request()

        sPattern = '(http.+?\?i=)([0-9x_]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            url=[]
            qua=[]

            for aEntry in aResult[1]:
                url.append(aEntry[0] + aEntry[1])
                qua.append(aEntry[1])

            #tableau
            stream_url = dialog().VSselectqual(qua, url)

        if (stream_url):
            return True, stream_url
        else:
            return False, False

        return False, False
