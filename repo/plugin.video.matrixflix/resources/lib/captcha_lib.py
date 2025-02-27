"""
    resolveurl XBMC Addon
    Copyright (C) 2014 tknorris

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    reusable captcha methods
"""

import re
import xbmcgui
import os
import requests
import base64
import time
import six
from kodi_six import xbmc, xbmcgui, xbmcaddon, xbmcvfs
from resources.lib import recaptcha_v2
from resources.lib import helpers
from resources.lib.comaddon import VSlog

addon = xbmcaddon.Addon('plugin.video.matrixflix')
net = Sgn=requests.Session()
IMG_FILE = 'captcha_img.gif'

def get_keyboard_new(heading, default='', hide_input=False):

    """
    This function has been in support since XBMC Gotham v13
    """

    if hide_input is False:
        hide_input = 0
    elif hide_input is True:
        hide_input = xbmcgui.ALPHANUM_HIDE_INPUT

    dialog = xbmcgui.Dialog()

    keyboard = dialog.input(heading, defaultt=default, type=0, option=hide_input)

    if keyboard:

        return keyboard

    return None

def get_response(img, x=450, y=0, w=400, h=130):
    try:
        img = xbmcgui.ControlImage(x, y, w, h, img)
        wdlg = xbmcgui.WindowDialog()
        wdlg.addControl(img)
        wdlg.show()
        time.sleep(3)
        solution = get_keyboard_new('letters_image')
        if not solution:
            raise Exception('captcha_error')
    finally:
        wdlg.close()
        return solution

def translate_path(path):
    return xbmcvfs.translatePath(path) if six.PY3 else xbmc.translatePath(path)

def write_img(url=None, bin=None):
    img = os.path.join(translate_path, IMG_FILE)
    if url:
        bin = Sgn.get(url).nodecode(True).content
    with open(img, 'wb') as file:
        _ = file.write(bin)
    return img


def do_captcha(html, base_url=None):
    solvemedia = re.search('<iframe[^>]+src="((?:https?:)?//api.solvemedia.com[^"]+)', html)
    recaptcha = re.search(r'<script\s+type="text/javascript"\s+src="(http://www.google.com[^"]+)', html)
    recaptcha_v2 = re.search('data-sitekey="([^"]+)', html)
    xfilecaptcha = re.search(r'<img\s+src="([^"]+/captchas/[^"]+)', html)
    ccapimg = re.search('key=([^"]+)"', html)

    if solvemedia:
        return do_solvemedia_captcha(solvemedia.group(1))
    elif recaptcha:
        return do_recaptcha(recaptcha.group(1))
    elif recaptcha_v2:
        return do_recaptcha_v2(recaptcha_v2.group(1), base_url)
    elif xfilecaptcha:
        return do_xfilecaptcha(xfilecaptcha.group(1))
    elif ccapimg and base_url:
        return {'secimgkey': ccapimg.group(1), 'secimginp': do_ccapimg_captcha(base_url + 'ccapimg?key=' + ccapimg.group(1))}
    else:
        captcha = re.compile(r'''left:(\d+)px;padding-top:\d+px;['"]>&#(.+?);<''').findall(html)
        result = sorted(captcha, key=lambda ltr: int(ltr[0]))
        solution = ''.join(str(int(num[1]) - 48) for num in result)
        if solution:
            return {'code': solution}
        else:
            return {}


def do_solvemedia_captcha(captcha_url):
    VSlog('SolveMedia Captcha: %s' % captcha_url)
    if captcha_url.startswith('//'):
        captcha_url = 'http:' + captcha_url
    html = Sgn.get(captcha_url).content
    data = {
        'adcopy_challenge': ''  # set to blank just in case not found; avoids exception on return
    }
    data.update(helpers.get_hidden(html), include_submit=False)

    # Check for alternate puzzle type - stored in a div
    alt_frame = re.search('<div><iframe src="(/papi/media[^"]+)', html)
    if alt_frame:
        html = Sgn.get("http://api.solvemedia.com%s" % alt_frame.group(1)).content
        alt_puzzle = re.search(r'<div\s+id="typein">\s*<img\s+src="data:image/png;base64,([^"]+)', html, re.DOTALL)
        if alt_puzzle:
            captcha_img = write_img(bin=base64.b64decode(alt_puzzle.group(1)))
        else:
            raise Exception('captcha_error')
    else:
        captcha_img = write_img("http://api.solvemedia.com%s" % re.search('<img src="(/papi/media[^"]+)"', html).group(1))

    solution = get_response(captcha_img)
    data['adcopy_response'] = solution
    html = Sgn.post('http://api.solvemedia.com/papi/verify.noscript', data)
    return {'adcopy_challenge': data['adcopy_challenge'], 'adcopy_response': 'manual_challenge'}


def do_recaptcha(captcha_url):
    VSlog('Google ReCaptcha: %s' % captcha_url)
    if captcha_url.startswith('//'):
        captcha_url = 'http:' + captcha_url
    personal_nid = addon.getSetting('personal_nid')
    if personal_nid:
        headers = {'Cookie': 'NID=' + personal_nid}
    else:
        headers = {}
    html = Sgn.get(captcha_url, headers=headers).content
    part = re.search(r"challenge \: \\'(.+?)\\'", html)
    captcha_img = 'http://www.google.com/recaptcha/api/image?c=' + part.group(1)
    solution = get_response(captcha_img)
    return {'recaptcha_challenge_field': part.group(1), 'recaptcha_response_field': solution}


def do_recaptcha_v2(sitekey, sRefer):
    token = recaptcha_v2.UnCaptchaReCaptcha().processCaptcha(sitekey, lang='en', Referer=sRefer)
    if token:
        return {'g-recaptcha-response': token}

    return {}


def do_xfilecaptcha(captcha_url):
    VSlog('XFileLoad ReCaptcha: %s' % captcha_url)
    if captcha_url.startswith('//'):
        captcha_url = 'http:' + captcha_url
    solution = get_response(captcha_url)
    return {'code': solution}


def do_ccapimg_captcha(captcha_url):
    VSlog('CCapImg Captcha: %s' % captcha_url)
    captcha_img = write_img(captcha_url)
    return get_response(captcha_img)
