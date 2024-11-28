#-*- coding: utf-8 -*-
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from six.moves import urllib_parse

UA = "VLSub 0.10.2"

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'aflix', 'ArabFlix', 'gold')

    def _getMediaLinkForGuest(self, autoPlay = False):
        api_call = self._url
        SubTitle = ''
        if ('sub.info' in self._url):
            subUrl = self._url.split('sub.info=')[1]
            oRequestHandler = cRequestHandler(subUrl)
            oRequestHandler.addHeaderEntry('Host', 'rest.opensubtitles.org')
            oRequestHandler.addHeaderEntry('X-User-Agent', 'trailers.to-UA')
            oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            subHtmlContent = oRequestHandler.request(jsonDecode=True)

            SubTitle = [item['SubDownloadLink'].replace(".gz", "").replace("download/", "download/subencoding-utf8/") for item in subHtmlContent]
            api_call = self._url.split('?sub.info=')[0] 

        if api_call:
            return True, urllib_parse.quote(api_call, '/:?=&'), SubTitle

        return False, False
