# -*- coding: utf-8 -*-

import re, requests, base64
import xbmcgui
import six
import time
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog, siteManager, addon

UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1"
addons = addon()

SITE_IDENTIFIER = 'newmirror'
SITE_NAME = 'NewMirror'
SITE_DESC = 'multi audio vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

URL_MAIN = base64.b64decode(URL_MAIN).decode("utf-8")[::-1]
IMG_MAIN = base64.b64decode('cG90Lm5kY3JvcnJpbWZuLmdtaQ==').decode("utf-8")[::-1]
VRF_MAIN = base64.b64decode('cHBhLnJvcnJpbXRlbi55ZmlyZXZyZXN1').decode("utf-8")[::-1]

MOVIE_EN = (URL_MAIN + 'movies', 'showMovies')
SERIE_EN = (URL_MAIN + 'series', 'showSeries')

URL_SEARCH_MOVIES = (URL_MAIN + 'search.php?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'search.php?s=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
	
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def set_setting(id, value):
    if not isinstance(value, six.string_types):
        value = str(value)
    addons.setSetting(id, value)

def fetch_html_content(url):
    def bypass(main_url):
        response = requests.get(f"{main_url}/home")
        
        match = re.search(r'data-addhash="([^"]+)"', response.text)
        if match:
            addhash = match.group(1)
        else:
            VSlog("addhash not found")
        
        unix_time = int(time.time())
        verify_url = f"https://{VRF_MAIN}/verify?hash={addhash}&t={unix_time}"
        requests.get(verify_url)
        
        request_body = {
            "verify": addhash
        }
        
        response = requests.post(f"{main_url}/verify2.php", data=request_body)
        
        t_hash_t = response.cookies.get("t_hash_t")
        set_setting('t_hash_t', t_hash_t)
        set_setting('t_hash_t_create', str(int(time.time())))
        
        return t_hash_t

    try:
        last_gen = int(addons.getSetting('t_hash_t_create'))
    except Exception:
        last_gen = 0

    if not addons.getSetting('t_hash_t') or last_gen < (time.time() - (1 * 24 * 60 * 60)):
        t_hash_t = bypass(URL_MAIN)
    else:
        t_hash_t = addons.getSetting('t_hash_t')
    
    headers = {
        "user-agent": UA,
        "cookie": f"t_hash_t={t_hash_t}; hd=on",
    }

    sHtmlContent = requests.get(url, headers=headers)
    return sHtmlContent

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search.php?s={sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
    
def showSeriesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search.php?s={sSearchText}'
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return  

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    if sSearch:
        sUrl = sSearch

        oOutputParameterHandler = cOutputParameterHandler()
        data = fetch_html_content(sUrl).json()
        for key in data['searchResult']:
            siteUrl = f'{URL_MAIN}playlist.php?id={key["id"]}'
            sThumb = f"https://{IMG_MAIN}/poster/v/{key['id']}.jpg"
            sTitle = key['t']
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

        sHtmlContent = fetch_html_content(sUrl).text

        sPattern =  'data-time="([^"]+)' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            sTime = aResult[1][0] 

        Yes = xbmcgui.Dialog().yesno(
            'احصل على اسم الفلم؟',
            'هل تريد تجربة الحصول على اسم الفلم قد يكون الأمر بطيئًا.. لا يُنصح بذلك..',
            'إلغاء'
            )

        listitems =[]
        sPattern =  'class="tray-link">(.+?)</a>' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sCat = aEntry
                listitems.append(sCat)
      
        index = xbmcgui.Dialog().contextmenu(listitems)
        if index>=0:
            entry = listitems[index] 

        oParser = cParser()
        sStart = f'>{entry}</a>'
        sEnd = '<div class="tray-container">'
        sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = 'data-post="([^"]+)".+?data-src="([^"]+)'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent1, sPattern)	
        if aResult[0] :
            oOutputParameterHandler = cOutputParameterHandler()  
            for aEntry in aResult[1]:
                siteUrl = f'{URL_MAIN}playlist.php?id={aEntry[0]}&tm={sTime}'
                sThumb = aEntry[1]
                sTitle = aEntry[0]
                if Yes:
                    sMovie = f'{URL_MAIN}post.php?id={aEntry[0]}'
                    data = fetch_html_content(sMovie).json()
                    sTitle = data['title']
                    siteUrl = f'{URL_MAIN}playlist.php?id={aEntry[0]}&t={sTitle}&tm={sTime}'
                sDesc = ''
                sCode = aEntry[0]

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sCode', sCode)
                oOutputParameterHandler.addParameter('sType', 'Movie')

                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()  

def showSeries(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    if sSearch:
        sUrl = sSearch
        oOutputParameterHandler = cOutputParameterHandler()
        data = fetch_html_content(sUrl).json()
        for key in data['searchResult']:
            siteUrl = f"{URL_MAIN}post.php?id={key['id']}"
            sThumb = f"https://{IMG_MAIN}/poster/v/{key['id']}.jpg"
            sTitle = key['t']
            sDesc = ''
            sCode = key['id']

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sCode', sCode)
            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
      
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

        response = fetch_html_content(sUrl)
        sHtmlContent = response.text

        sPattern =  'data-time="([^"]+)' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            sTime = aResult[1][0] 

        Yes = xbmcgui.Dialog().yesno(
            'احصل على اسم المسلسل',
            'هل تريد تجربة الحصول على اسم المسلسل قد يكون الأمر بطيئًا.. لا يُنصح بذلك..',
            'إلغاء'
            )

        listitems =[]
        sPattern =  'class="tray-link">(.+?)</a>' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sCat = aEntry
                listitems.append(sCat)
      
        index = xbmcgui.Dialog().contextmenu(listitems)
        if index>=0:
            entry = listitems[index] 

        oParser = cParser()
        sStart = f'>{entry}</a>'
        sEnd = '<div class="tray-container">'
        sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = 'data-post="([^"]+)".+?data-src="([^"]+)'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent1, sPattern)	
        if aResult[0] :
            oOutputParameterHandler = cOutputParameterHandler()  
            for aEntry in aResult[1]:
                siteUrl = f'{URL_MAIN}post.php?id={aEntry[0]}'
                sThumb = aEntry[1]
                sTitle = aEntry[0]
                if Yes:
                    data = fetch_html_content(siteUrl).json()
                    sTitle = data['title']
                sDesc = ''
                sCode = aEntry[0]

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sCode', sCode)
                oOutputParameterHandler.addParameter('sTime', sTime)
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()  

def showSeasons():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sCode = oInputParameterHandler.getValue('sCode')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sTime = oInputParameterHandler.getValue('sTime')
    
    data = fetch_html_content(sUrl).json()
    for key in data['season']:
        sSeason = ' S'+ key['s']
        siteUrl = f"{URL_MAIN}episodes.php?s={key['id']}&series={sCode}"
        sThumb = f"https://{IMG_MAIN}/poster/v/{key['id']}.jpg"
        sTitle = data['title']
        sTitle = sTitle + sSeason
        sDesc = data['desc']
			
        oOutputParameterHandler.addParameter('siteUrl',siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sDesc', sDesc)
        oOutputParameterHandler.addParameter('sCode', sCode)
        oOutputParameterHandler.addParameter('sTime', sTime)

        oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory() 
        
def showEpisodes():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sCode = oInputParameterHandler.getValue('sCode')
    sTime = oInputParameterHandler.getValue('sTime')

    data = fetch_html_content(sUrl).json()
    for key in data['episodes']:
        sEpisode = key['ep']
        siteUrl = f'{URL_MAIN}playlist.php?id={key["id"]}&tm={sTime}'
        sThumb = f"https://{IMG_MAIN}/poster/v/{key['id']}.jpg"
        sTitle = sMovieTitle + sEpisode
        sDesc = sDesc

        oOutputParameterHandler.addParameter('siteUrl',siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sType', 'Serie')

        oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sThumb, sDesc, oOutputParameterHandler)

    sPage = int(data['nextPageShow'])
    if sPage > 0: 
            siteUrl = f'{URL_MAIN}episodes.php?s={data["nextPageSeason"]}&series={sCode}&page={data["nextPage"]}'
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory() 
 
def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sCode = oInputParameterHandler.getValue('sCode')
    sType = oInputParameterHandler.getValue('sType')

    sSub = False
    data = fetch_html_content(sUrl).json()
    for key in data:
        if sType == 'Movie':
            sMovie = f'{URL_MAIN}post.php?id={sCode}'
            data = fetch_html_content(sMovie).json()
            sMovieTitle = data['title']
        try:
            for data in key['tracks']:
                if data['kind'] == 'thumbnails':
                    continue

                if data["label"] == "ar":
                    sSub = 'https:' + data["file"]
                elif data["label"] == "en":
                    sSub = 'https:' + data["file"]
        except:
            VSlog('no subs')

        for data in key['sources']:
            sQual = data['label']
            if 'Full' in sQual:
                sQual = '1080p'
            if 'Mid' in sQual:
                sQual = '720p Default'
            if 'Low' in sQual:
                sQual = '480p'

            sUrl = f'{URL_MAIN[:-1]}{data["file"]}'
            sThumb = ''
            sTitle = ('%s  [COLOR coral](%s)[/COLOR]') % (sMovieTitle, sQual)  

            sHosterUrl = f'{sUrl}|Referer={URL_MAIN}&cookie=t_hash_t={addons.getSetting("t_hash_t")};hd=on'
            if sSub:
                sHosterUrl += f'?sub.info={sSub}'
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                sDisplayTitle = sTitle
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
