# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import json

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'clickopen', 'ClickOpen')

    def _getMediaLinkForGuest(self, autoPlay = False):
        url = 'https://clickopen.win/api/source/' + self._url.rsplit('/', 1)[1]

        postdata = 'r=&d=clickopen.win'

        oRequest = cRequestHandler(url)
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', self._url)
        oRequest.enableCache(False)
        oRequest.addParametersLine(postdata)
        sHtmlContent = oRequest.request()

        page = json.loads(sHtmlContent)
        if page:
            url = []
            qua = []
            for x in page['data']:
                url.append(x['file'])
                qua.append(x['label'])

            if url:
                api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
