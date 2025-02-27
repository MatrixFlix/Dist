# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog
from resources.lib.comaddon import VSlog

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'estream', 'Estream')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = False

        oRequest = cRequestHandler(self._url)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern = '<source *src="([^"]+)" *type=\'video/.+?\''
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]

        sPattern = '<script type=\'text/javascript\'>(.+?)</script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            stri = cPacker().unpack(aResult[1][0])
            sPattern = 'file:"([^"]+)",label:"([0-9]+)"}'
            aResult = oParser.parse(stri, sPattern)
            if aResult[0]:
                url = []
                qua = []

                for aEntry in aResult[1]:
                    url.append(aEntry[0])
                    qua.append(aEntry[1][:3] + '*' + aEntry[1][3:])

                api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
