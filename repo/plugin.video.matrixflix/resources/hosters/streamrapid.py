#-*- coding: utf-8 -*-

import json
import re
import requests
import base64
from six.moves import urllib_parse

from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
from resolveurl.lib.pyaes import openssl_aes

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'streamrapid', 'Rabbitstream/Dokicloud')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        mainurl = self._url

        referer = urllib_parse.urljoin(self._url, '/')
        headers = {'User-Agent': UA,
                   'Referer': referer}
        
        s = requests.Session()  
   
        r = s.get(self._url, headers=headers)
        sHtmlContent = r.content.decode('utf8')
        oParser = cParser()

        sPattern = '<script type="text/javascript" src="(.+?)"></script>'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            surl = aResult[1][0]
            surl = referer + surl

        host = mainurl.split("/e")[0]
        host = host.split("//")[1]
        mid = mainurl.split('?')[0]
        mid = mid.split("embed-4")[1]
        mid = mid.replace('/', '/getSources?id=')
        aurl = 'https://'+host+'/ajax/embed-4'+mid

        headers = {'User-Agent': UA,
                   'Referer': referer, 'X-Requested-With': 'XMLHttpRequest'}
        r = s.get(aurl, headers=headers)
        sHtmlContent = r.content.decode('utf8')
        oParser = cParser()

        sPattern = '"sources":"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sources = aResult[1][0]

            response = requests.get('https://keys4.fun')
            keys = response.json()["rabbitstream"]["keys"]

            key_bytes = bytes(keys)
            key_string = base64.b64encode(key_bytes).decode('utf-8')

            strippedSources = sources

            OpenSSL_AES = openssl_aes.AESCipher()
            sources = json.loads(OpenSSL_AES.decrypt(strippedSources, key_string))

            sPattern = "'file': '(.+?)',"
            aResult = oParser.parse(sources, sPattern)
            if aResult[0]:
                source = aResult[1][0]

        sPattern = '{"file":"([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            source = aResult[1][0]

        url_stream = source

        SubTitle = ''
        sPattern = '"file":"([^"]+)".+?"label":"(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            url = []
            qua = []
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))
            SubTitle = dialog().VSselectsub(qua, url)

        if url_stream:
            if ('http' in SubTitle):
                return True, url_stream, SubTitle
            else:
                return True, url_stream

        return False, False

def extractKey(script):
    startOfSwitch = script.rfind("switch")
    endOfCases = script.find("partKeyStartPosition")
    switchBody = script[startOfSwitch:endOfCases]
    nums = []
    matches = re.findall(r":[a-zA-Z0-9]+=([a-zA-Z0-9]+),[a-zA-Z0-9]+=([a-zA-Z0-9]+);", switchBody)
    for match in matches:
        innerNumbers = []
        for varMatch in match:
            regex = re.compile(f"{varMatch}=0x([a-zA-Z0-9]+)")
            varMatches = re.findall(regex, script)
            lastMatch = varMatches[-1]
            if not lastMatch:
                return None
            number = int(lastMatch, 16)
            innerNumbers.append(number)
        nums.append([innerNumbers[0], innerNumbers[1]])
    return nums