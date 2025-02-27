﻿from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.util import urlHostName
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
from resources.lib import random_ua
import unicodedata

UA = random_ua.get_phone_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'xvideo', 'xVideoSharing')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = ''
        sReferer = f'https://{urlHostName(self._url)}/'

        oRequest = cRequestHandler(self._url)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()
        oParser = cParser()
       
        api_call = ''
        sPattern = 'file:"(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0] 
            
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            data = aResult[1][0]
            data = unicodedata.normalize('NFD', data).encode('ascii', 'ignore').decode('unicode_escape')
            sHtmlContent = cPacker().unpack(data)

        else:
            self._url = self._url.replace('embed-','')
            oRequest = cRequestHandler(self._url)
            sHtmlContent = oRequest.request()

            sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                data = aResult[1][0]
                data = unicodedata.normalize('NFD', data).encode('ascii', 'ignore').decode('unicode_escape')
                sHtmlContent = cPacker().unpack(data)

        sPattern = 'file:"(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0] 

        sPattern = '<source src="(.+?)" type="video/mp4"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            api_call = aResult[1][0]

        sPattern = 'sources:\["([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0] 

        if api_call:
            return True, f'{api_call}|User-Agent={UA}&Referer={sReferer}&verifypeer=false&Accept-Language=en-US,en;q=0.9'

        return False, False