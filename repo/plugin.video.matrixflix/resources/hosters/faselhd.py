#coding: utf-8
import base64
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog, addon, siteManager
from resources.sites.faselhd import decode_page
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'faselhd', 'FaselHD', 'gold')

    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        api_call = self._url
        VSlog(self._url)
        oParser = cParser()   

        if addon().getSetting('Use_alternative') == "true":
            URL_MAIN = base64.b64decode(siteManager().getUrlMain2('faselhd')).decode("utf-8")[::-1]
            self._url = URL_MAIN + "/".join(self._url.split("/")[3:]) if self._url.startswith("https://") else self._url

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('user-agent',UA)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        if 'adilbo' in sHtmlContent:
            sHtmlContent = decode_page(sHtmlContent)
        
        sPattern =  'data-url="([^<]+)">([^<]+)</button>' 
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sLink = []
                sQual = []
                for aEntry in aResult[1]:
                    sLink.append(str(aEntry[0]))
                    sQual.append(str(aEntry[1].upper()))
            api_call = dialog().VSselectqual(sQual, sLink)

        sPattern =  'videoSrc = ["\']([^"\']+)["\']' 
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                api_call = aEntry
        
        if api_call:
            return True, api_call + '|User-Agent=' + UA

        return False, False
