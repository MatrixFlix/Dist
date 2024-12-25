#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog, dialog
from resources.lib import helpers
from resources.lib import captcha_lib
from six.moves import urllib_parse
import re
import requests
import time

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'frdl', 'FreeDownload')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = ''
        Sgn=requests.Session()

        headers = {
            'referer': self._url,
            'User-Agent': UA
                }

        sHtmlContent = Sgn.get(self._url, headers=headers).text
        data = helpers.get_hidden(sHtmlContent)
        data.update(captcha_lib.do_captcha(sHtmlContent))

        match = re.search(r'seconds\.html\((\d+)\);', sHtmlContent)
        if match:
            waitingseconds = int(match.group(1))+1

        dialog().VSinfo(f'الموقع يطلب الانتظار لمدة {waitingseconds} ثانية')
        time.sleep(waitingseconds)

        _r = Sgn.post(self._url, data, headers=headers)
        sHtmlContent = _r.content.decode('utf8',errors='ignore')

        r = r = re.search(r'''sources:\s*\[{src:\s*["'](?P<url>[^"']+)''', sHtmlContent, re.DOTALL)
        if r:
            api_call = urllib_parse.quote(r.group(1), '/:?=&') + helpers.append_headers(headers)

        else:
            pattern = r'<a href="([^"]+)"[^>]*type="button" class="btn[^"]*">'
            r = re.search(pattern, sHtmlContent)
            if r:
                api_call = urllib_parse.quote(r.group(1), '/:?=&') + helpers.append_headers(headers)

        if api_call:
            return True, api_call

        return False, False