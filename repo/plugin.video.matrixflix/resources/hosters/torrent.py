# -*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib.handler.requestHandler import cRequestHandler
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

        if 'magnet' in self._url:
            oRequestHandler = cRequestHandler("https://raw.githubusercontent.com/XIU2/TrackersListCollection/refs/heads/master/best.txt")
            tList = oRequestHandler.request()
            trackers = [line.strip() for line in tList.strip().split('\n') if line.strip()]
            #trackers = [
            #            "udp://tracker.coppersurfer.tk:6969/announce",
            #            "udp://9.rarbg.to:2920/announce",
            #            "udp://tracker.opentrackr.org:1337",
            #            "udp://tracker.internetwarriors.net:1337/announce",
            #            "udp://tracker.leechers-paradise.org:6969/announce",
            #            "udp://tracker.coppersurfer.tk:6969/announce",
            #            "udp://tracker.pirateparty.gr:6969/announce",
            #            "udp://tracker.cyberia.is:6969/announce",
            #            "udp://tracker.openbittorrent.com:6969/announce",
            #            "udp://public.popcorn-tracker.org:6969/announce",
            #            "udp://tracker.bittor.pw:1337/announce"
            #            ]
            api_call = f'plugin://plugin.video.torrest/play_magnet?magnet={self._url}'+ "&tr=" + "&tr=".join(trackers)
        else:
            videoID = self.__getIdFromUrl(self._url)
            api_call = f'plugin://plugin.video.torrest/play_url?url={videoID}'

        if api_call:
            return True, api_call
        
        return False, False

    def __getIdFromUrl(self, sUrl):
        id = sUrl.replace('ttmxtt','')
        return id
