#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons

import re
import requests

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.aadecode import AADecoder
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'userload', 'Userload')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = False

        keymorocco = ''
        keymycountry= ''
        morocco = ''
        mycountry = ''

        urlapi = "https://userload.co/api/assets/userload/js/videojs.js"

        sHtmlContent1 = requests.get(urlapi).content.decode('utf-8')

        oParser = cParser()
        sPattern = '(ﾟωﾟ.+?\(\'_\'\);)'
        aResult = oParser.parse(sHtmlContent1 , sPattern)

        if aResult[0]:
            sdecode = AADecoder(aResult[1][0]).decode()

            sPattern =  'morocco=".([^\W]+).+?"&mycountry=".([^\W]+)'
            aResult_2 = oParser.parse(sdecode, sPattern)

            if aResult_2[0] :
                keymorocco = aResult_2[1][0][0]
                keymycountry = aResult_2[1][0][1]

        referer = self._url.split('|Referer=')[1]
        url = self._url.split('|Referer=')[:-1][0]

        oRequestHandler = cRequestHandler(url)
        oRequestHandler.addHeaderEntry('Referer', referer)
        oRequestHandler.enableCache(False)
        sHtmlContent1 = oRequestHandler.request()

        sPattern2 = '<script type="text/javascript">(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
        aResult = re.findall(sPattern2, sHtmlContent1)

        if aResult:
            str2 = aResult[0]
            if not str2.endswith(';'):
                str2 = str2 + ';'

            strs = cPacker().unpack(str2)

            oParser = cParser()
            sPattern = 'var\s(.+?)="([^"]*)'
            aResult = oParser.parse(strs, sPattern)

            if aResult[0]:
                for r in aResult[1]:
                    if r[0] == keymorocco:
                        morocco = r[1]
                    if r[0] == keymycountry:
                        mycountry = r[1]

        if morocco and mycountry:
            url2 = 'https://userload.co/api/request/'
            pdata = 'morocco=' + morocco + '&mycountry=' + mycountry
            oRequest = cRequestHandler(url2)
            oRequest.setRequestType(1)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
            oRequest.addHeaderEntry('Content-Length', len(str(pdata)))
            oRequest.addHeaderEntry('Referer', url)
            oRequest.addParametersLine(pdata)
            api_call = oRequest.request()

            if 'mp4' in api_call and 'uloadcdn.com' in api_call :
                return True, api_call.strip()

        return False, False
