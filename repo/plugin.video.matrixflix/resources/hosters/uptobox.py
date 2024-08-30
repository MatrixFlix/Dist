# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.hosters.hoster import iHoster
from resources.hosters.uptostream import cHoster as uptostreamHoster
from resources.lib.comaddon import dialog, VSlog, addon
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import cRequestHandler

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'uptobox', 'Uptobox', 'violet')
        self.oPremiumHandler = None

    def setUrl(self, url):
        self._url = str(url)
        self._url = self._url.replace('iframe/', '')
        self._url = self._url.replace('http:', 'https:')
        self._url = self._url.split('?aff_id')[0]

    def checkUrl(self, sUrl):
        return True

    def getMediaLink(self):
        self.oPremiumHandler = cPremiumHandler(self.getPluginIdentifier())
        if self.oPremiumHandler.isPremiumModeAvailable():
            ADDON = addon()

            try:
                mDefault = int(ADDON.getSetting("hoster_uptobox_mode_default"))
            except AttributeError:
                mDefault = 0

            if mDefault == 0:
                ret = dialog().VSselect(['Streaming (via Uptostream)', 'Rest and direct (via Uptobox)'],
                                        'Choose your operating mode..')
            else:
                ret = mDefault - 1

            if ret == 0:
                return self._getMediaLinkForGuest()

            if ret == 1:
                return self._getMediaLinkByPremiumUser()

            return False

        else:
            VSlog('UPTOBOX - no premium')
            return self._getMediaLinkForGuest()

    def _getMediaLinkForGuest(self, autoPlay = False):
        self._url = self._url.replace('uptobox.com/', 'uptostream.eu/')
        self._url = self._url.replace('uptobox.eu/', 'uptostream.eu/')

        oHoster = uptostreamHoster()
        oHoster.setUrl(self._url)
        return oHoster.getMediaLink()

    def _getMediaLinkByPremiumUser(self, autoPlay = False):

        token = self.oPremiumHandler.getToken()
        if not token:
            return self._getMediaLinkForGuest()

        fileCode = self._url.split('/')[-1].split('?')[0]
        url1 = "https://uptobox.eu/api/link?token=%s&file_code=%s" % (token, fileCode)
        try:
            oRequestHandler = cRequestHandler(url1)
            dict_liens = oRequestHandler.request(jsonDecode=True)
            statusCode = dict_liens["statusCode"]
            if statusCode == 0:  # success
                return True, dict_liens["data"]["dlLink"]

            if statusCode == 16:  # Waiting needed
                status = "Pas de compte Premium"
            elif statusCode == 7: 
                status = dict_liens["message"] + ' : ' + dict_liens["data"]
            else:
                status = 'Erreur inconnue : %s, message = %s : %s' % (str(statusCode), dict_liens["message"], str(dict_liens["data"]))
        except Exception as e:
            status = e

        VSlog('UPTOBOX - ' + str(status))

        return False
