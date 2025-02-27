# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import addon, dialog, VSlog
from resources.lib.config import GestionCookie
from resources.lib.parser import cParser

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'


class cPremiumHandler:
    ADDON = addon()
    DIALOG = dialog()

    def __init__(self, sHosterIdentifier):
        self.__sHosterIdentifier = sHosterIdentifier.lower()
        self.__sDisplayName = 'Premium mode'
        self.isLogin = False
        self.__LoginTry = False
        self.__ssl = False

        if self.__sHosterIdentifier == '1fichier':
            self.__sHosterIdentifier = 'onefichier'

        self.__Ispremium = False
        bIsPremium = self.ADDON.getSetting('hoster_' + str(self.__sHosterIdentifier) + '_premium')
        if (bIsPremium == 'true'):
            VSlog("Use premium account to host " + str(self.__sHosterIdentifier))
            self.__Ispremium = True
        else:
            VSlog("Use free account to host " + str(self.__sHosterIdentifier))

    def isPremiumModeAvailable(self):
        return self.__Ispremium

    def getUsername(self):
        sUsername = self.ADDON.getSetting('hoster_' + str(self.__sHosterIdentifier) + '_username')
        return sUsername

    def getPassword(self):
        sPassword = self.ADDON.getSetting('hoster_' + str(self.__sHosterIdentifier) + '_password')
        return sPassword

    def AddCookies(self):
        cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)
        return 'Cookie=' + cookies

    def Checklogged(self, code):
        if 'uptobox' in self.__sHosterIdentifier:
            if '//uptobox.com/logout?' in code or 'Success' in code:
                return True

        if 'onefichier' in self.__sHosterIdentifier:
            if 'premium' in code or 'jqueryFileTree' in code or '1fichier.com/logout' in code:
                return True

        return False

    def CheckCookie(self):
        cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)
        if cookies != '':
            return True
        return False

    def Authentificate(self):
        if self.__LoginTry:
            return False
        self.__LoginTry = True

        if not self.__Ispremium:
            return False

        post_data = {}

        if 'uptobox' in self.__sHosterIdentifier:
            url = 'https://uptobox.com/login'
            post_data['login'] = self.getUsername()
            post_data['password'] = self.getPassword()

        elif 'onefichier' in self.__sHosterIdentifier:
            url = 'https://1fichier.com/login.pl'
            post_data['mail'] = self.getUsername()
            post_data['pass'] = self.getPassword()
            post_data['lt'] = 'on'
            post_data['purge'] = 'on'
            post_data['valider'] = 'Send'

        elif 'uploaded' in self.__sHosterIdentifier:
            url = 'http://uploaded.net/io/login'
            post_data['id'] = self.getUsername()
            post_data['pw'] = self.getPassword()

        else:
            return False

        oRequestHandler = cRequestHandler(url)
        oRequestHandler.setRequestType(1)

        if 'uptobox' in self.__sHosterIdentifier:
            oRequestHandler.disableRedirect()

            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Content-Type', "application/x-www-form-urlencoded")
            oRequestHandler.addHeaderEntry('Content-Length', str(len(post_data)))

        for data in post_data:
            oRequestHandler.addParameters(data, post_data[data])

        sHtmlContent = oRequestHandler.request()
        head = oRequestHandler.getResponseHeader()

        if 'uptobox' in self.__sHosterIdentifier:
            if 'Set-Cookie' in head and 'xfss' in head['Set-Cookie']:
                self.isLogin = True
            else:
                self.DIALOG.VSinfo('Authentification rate', self.__sDisplayName)
                return False
        elif 'onefichier' in self.__sHosterIdentifier:
            if 'You are logged in. This page will redirect you.' in sHtmlContent:
                self.isLogin = True
            else:
                self.DIALOG.VSinfo('Authentification rate', self.__sDisplayName)
                return False
        elif 'uploaded' in self.__sHosterIdentifier:
            if sHtmlContent == '':
                self.isLogin = True
            else:
                self.DIALOG.VSinfo('Authentification rate', self.__sDisplayName)
                return False
        else:
            return False

        cookies = ''
        if 'Set-Cookie' in head:
            oParser = cParser()
            sPattern = '(?:^|,) *([^;,]+?)=([^;,\/]+?);'
            aResult = oParser.parse(str(head['Set-Cookie']), sPattern)
            if (aResult[0] == True):
                for cook in aResult[1]:
                    if 'deleted' in cook[1]:
                        continue
                    cookies = cookies + cook[0] + '=' + cook[1] + ';'

        GestionCookie().SaveCookie(self.__sHosterIdentifier, cookies)

        self.DIALOG.VSinfo('Authentication successful', self.__sDisplayName)
        VSlog('Authentication successful')

        return True

    def GetHtmlwithcookies(self, url, data, cookies):
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        if not (data == None):
            oRequestHandler.addParametersLine(data)
            oRequestHandler.addHeaderEntry('Referer', url)

        oRequestHandler.addHeaderEntry('Cookie', cookies)

        sHtmlContent = oRequestHandler.request()
        return sHtmlContent

    def GetHtml(self, url, data=None):
        cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)
        if (cookies == '') and not self.__LoginTry and self.__Ispremium:
            self.Authentificate()
            if not self.isLogin:
                return ''
            cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)

        sHtmlContent = self.GetHtmlwithcookies(url, data, cookies)

        if not self.Checklogged(sHtmlContent) and not self.__LoginTry and self.__Ispremium:
            VSlog('Cookies non valables')
            self.Authentificate()
            if self.isLogin:
                cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)
                sHtmlContent = self.GetHtmlwithcookies(url, data, cookies)
            else:
                return ''

        return sHtmlContent

    def setToken(self, sToken):
        self.ADDON.setSetting('hoster_' + str(self.__sHosterIdentifier) + '_token', sToken)

    def getToken(self):

        if not self.__Ispremium:
            return None

        sToken = self.ADDON.getSetting('hoster_' + str(self.__sHosterIdentifier) + '_token')
        if sToken:
            return sToken

        if 'alldebrid' in self.__sHosterIdentifier:
            sToken = self.ADDON.getSetting('token_alldebrid')
            if sToken:
                self.ADDON.setSetting('hoster_' + str(self.__sHosterIdentifier) + '_token', sToken)
            return sToken

        if 'uptobox' in self.__sHosterIdentifier:

            if not self.isLogin:
                self.Authentificate()

            if self.isLogin:
                sHtmlContent = self.GetHtml('https://uptobox.com/my_account')
                sPattern = 'data-clipboard-text="(.+?)" data-tippy-content="Token'
                aResult = cParser().parse(sHtmlContent, sPattern, 1)
                if aResult[0]:
                    sToken = aResult[1][0]
                    self.ADDON.setSetting('hoster_' + str(self.__sHosterIdentifier) + '_token', sToken)
                    return sToken

        return None
