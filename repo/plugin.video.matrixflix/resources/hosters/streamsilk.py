#-*- coding: utf-8 -*-

import re
import base64
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.hunter import hunter
from resources.lib.comaddon import VSlog, isMatrix

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'streamsilk', 'StreamSilk')

    def _getMediaLinkForGuest(self, autoPlay = False):
        api_call = False
        VSlog(self._url)

        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequest.request()

        sPattern = 'return decodeURIComponent\(escape\(r\)\)}\("([^,]+)",([^,]+),"([^,]+)",([^,]+),([^,]+),([^,\))]+)\)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            l = aResult[1]
            for j in l:
                unpacked = hunter(j[0],int(j[1]),j[2],int(j[3]),int(j[4]),int(j[5]))

                hls_url = re.search(r'var urlPlay =\s*"(.*?m3u8.*?)"', unpacked).group(1)       

        if hls_url:
            return True, f'{hls_url.strip()}|User-Agent={UA}&Referer={self._url}'

        if api_call:
            return True, api_call

        return False, False
