# -*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
import xbmcaddon

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'torrent', 'Torrent')

    def _getMediaLinkForGuest(self, autoPlay = False):

        api_call = ''

        try:
            xbmcaddon.Addon('plugin.video.torrest')
        except:
            VSlog('Plugin Torrest Not Installed')


            return False

        videoID = self.__getIdFromUrl(self._url)
        api_call = 'plugin://plugin.video.torrest/play_url?url=' + videoID


        if api_call:
            return True, api_call
        else:
            return False, False

    def __getIdFromUrl(self, sUrl):
        id = ''
        id = sUrl.replace('ttmxtt','')
 
        return id
