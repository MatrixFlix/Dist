# -*- coding: utf-8 -*-

from resources.lib.parser import cParser
from resources.lib.util import urlEncode
from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, isMatrix
from resources.lib.aadecode import AADecoder
from resources.lib.util import urlHostName
from resources.lib.hunter import hunter

import re
import base64

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'

def decode(chars, b):
    state = {}
    j = 0
    optsData = ""
    i = 0
  
    while i < 256:
        state[i] = i
        i = i + 1
  
    i = 0
  
    while i < 256:
        j = (j + state[i] + ord(chars[i % len(chars)])) % 256
        v = state[i]
        state[i] = state[j]
        state[j] = v
        i = i + 1
    
    bMatrix = isMatrix()

    i = 0
    j = 0
    bi = 0
    while bi < len(b) :
        nn = (i + 1) % 256
        i = nn
        j = (j + state[nn]) % 256
        v = state[i]
        state[i] = state[j]
        state[j] = v
        if bMatrix:
            optsData += chr(b[bi] ^ state[(state[i] + state[j]) % 256])
        else:
            optsData += chr(ord(b[bi]) ^ state[(state[i] + state[j]) % 256])
        bi = bi + 1

    return optsData

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'turbovid', 'Turbovid')

    def setUrl(self, url):
        self._url = url

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = False

        headers4 = {'user-agent': UA,
                    'Referer': self._url
                    }

        sPattern = 'iframe id="iframe" src="([^"]+)"'
        oParser = cParser()
        
        t = 3
        url2 = self._url
        url = ''
        
        while t > 0:
            t = t - 1
            
            oRequest = cRequestHandler(url2)
            oRequest.addHeaderEntry('User-Agent', UA)
            if url:
                oRequest.addHeaderEntry('Referer', url)
            oRequest.enableCache(False)
            sHtmlContent = oRequest.request()
            
            aResult = oParser.parse(sHtmlContent, sPattern)
            url = url2
            
            if aResult[0] == False:
                break

            url2 = aResult[1][0]

        sPattern = "urlPlay = '([^']+)'"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]
            return True, api_call + '|' + urlEncode(headers4)

        sPattern = "data-hash\s*=\s*'([^']+)'"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]
            return True, api_call + '|' + urlEncode(headers4)

        sPattern = 'return decodeURIComponent\(escape\(r\)\)}\("([^,]+)",([^,]+),"([^,]+)",([^,]+),([^,]+),([^,\))]+)\)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            l = aResult[1]
            for j in l:
                unpacked = hunter(j[0],int(j[1]),j[2],int(j[3]),int(j[4]),int(j[5]))

                sPattern = "var urlPlay =\s*'([^']+)'"
                aResult = oParser.parse(unpacked, sPattern)
                if aResult[0]:  
                    hls_url = aResult[1][0]  

                    sRefer = urlHostName(self._url)
                    return True, f'{hls_url.strip()}|User-Agent={UA}&Referer=https://{sRefer}/&Origin=https://{sRefer}'

        sPattern = '<input type="hidden" value="([^"]+)" id="js" \/><input type="hidden" value="([^"]+)" id="code" \/><input type="hidden" value="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if not aResult[0]:
            return False, False
            
        js = aResult[1][0][0]
        code = aResult[1][0][1]
        func = aResult[1][0][2]
            
        aResult = re.search('(ﾟωﾟ.+?\(\'_\'\);)', sHtmlContent, re.DOTALL | re.UNICODE)
        if aResult:
            sHtmlContent = AADecoder(aResult.group(1)).decode()
            if sHtmlContent:
                aResult = re.search("\('([^']+)', window\.atob\(document\.getElementById\('func'\).v", sHtmlContent, re.DOTALL)
                if aResult:
                    key = aResult.group(1)
                    
        t = decode(key, base64.b64decode(func))
        
        sPattern = "\('src',\s*'([^']+)'"
        aResult = oParser.parse(t, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]

        if api_call:
            return True, api_call + '|' + urlEncode(headers4)

        return False, False
