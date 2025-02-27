# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import json
import re
import requests
import xbmc

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog, CountdownDialog, VSPath
from resources.lib.config import GestionCookie
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.librecaptcha.gui import cInputWindowYesNo
from resources.lib.parser import cParser


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'uptostream', 'UpToStream')
        self.oPremiumHandler = None

    def setUrl(self, url):
        self._url = str(url)

    def checkSubtitle(self, sHtmlContent):
        if not sHtmlContent:
            return False

        files = []
        for aEntry in sHtmlContent:
            if aEntry["label"] == "French":
                url = aEntry["src"]
                if not url.startswith('http'):
                    url = 'http:' + url
                files.append(url)
            else:
                continue
        return files

    def _getMediaLinkForGuest(self, autoPlay = False):
        pass

    def getMediaLink(self):
        self.oPremiumHandler = cPremiumHandler('uptobox')
        premium = self.oPremiumHandler.isPremiumModeAvailable()
        if not premium:
            dialog().VSok('Ce hoster necessite un compte, meme gratuit.')
            return False, False

        api_call = False
        SubTitle = False
        filecode = self._url.split('/')[-1].split('?')[0]

        token = self.oPremiumHandler.getToken()
        if token:
            r = requests.get('https://uptobox.eu/api/user/me?token=' + token).json()
        if token and r["data"]["premium"]:
            status = ''
            url1 = "https://uptobox.eu/api/streaming?token=%s&file_code=%s" % (token, filecode)
            try:
                oRequestHandler = cRequestHandler(url1)
                dict_liens = oRequestHandler.request(jsonDecode=True)
                status = dict_liens["statusCode"]
                if status == 0:
                    js_result = dict_liens["data"]
            except Exception as e:
                status = e

            if status:
                VSlog('UPTOBOX - ' + status)
                return False

        else:
            SubTitle = ""
            cookies = GestionCookie().Readcookie("uptobox")

            s = requests.Session()
            s.headers.update({"Cookie": cookies})
            r = s.get('https://uptobox.eu/api/streaming?file_code=' + filecode).json()

            if r["statusCode"] != 0: 
                dialog().VSinfo(r["data"])
                return False, False

            if not xbmc.getCondVisibility('system.platform.android'):
                import webbrowser
                webbrowser.open(r['data']['user_url'])
                with CountdownDialog("Autorisation nécessaire", "Pour voir cette vidéo, veuillez vous connecter",
                                     "Allez sur ce lien : " + r['data']['user_url'],
                                     "Et valider le pin : " + r['data']['pin'], True, r["data"]['expired_in'], 10) as cd:
                    js_result = cd.start(self.__check_auth, [r["data"]["check_url"]])["data"]
            else:
                import pyqrcode
                qr = pyqrcode.create(r['data']['user_url'])
                qr.png(VSPath('special://home/userdata/addon_data/plugin.video.vstream/qrcode.png'), scale=5)
                oSolver = cInputWindowYesNo(captcha='special://home/userdata/addon_data/plugin.video.vstream/qrcode.png', msg="Scanner le QRCode pour acceder au lien d'autorisation", roundnum=1)
                retArg = oSolver.get()
                if retArg == "N":
                    return False

                js_result = s.get(r["data"]["check_url"]).json()["data"]

        if js_result.get("streamLinks").get('src'):
            api_call = js_result['streamLinks']['src']
        else:
            sPattern = "'(.+?)': {(.+?)}"

            oParser = cParser()
            aResult = oParser.parse(js_result["streamLinks"], sPattern)

            url = []
            qua = []

            for aEntry in aResult[1]:
                QUAL = aEntry[0]
                d = re.findall("'u*(.+?)': u*'(.+?)'", aEntry[1])
                for aEntry1 in d:
                    url.append(aEntry1[1])
                    qua.append(QUAL + ' (' + aEntry1[0] + ')')

            api_call = dialog().VSselectqual(qua, url)

        try:
            SubTitle = self.checkSubtitle(js_result["subs"])
        except:
            VSlog("Pas de sous-titre")

        if api_call:
            if SubTitle:
                return True, api_call, SubTitle
            else:
                return True, api_call

        return False, False

    def __check_auth(self, url):
        try:
            js_result = json.loads(requests.get(url).content)
        except ValueError:
            raise Exception('Unusable Authorization Response')

        if js_result.get('statusCode') == 0:
            if js_result.get('data') == "wait-pin-validation":
                return False
            else:
                return js_result

        raise Exception('Error during check authorisation.')
