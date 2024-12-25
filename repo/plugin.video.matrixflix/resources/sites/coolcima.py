# -*- coding: utf-8 -*-

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.multihost import cMegamax
from resources.lib import random_ua

UA = random_ua.get_ua()

SITE_IDENTIFIER = 'coolcima'
SITE_NAME = 'CoolCima'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (f'{URL_MAIN}category/افلام-اجنبي/', 'showMovies')
MOVIE_DUBBED = (f'{URL_MAIN}category/افلام-اجنبي-مدبلجة/', 'showMovies')
MOVIE_AR = (f'{URL_MAIN}category/افلام-عربي/', 'showMovies')
MOVIE_HI = (f'{URL_MAIN}category/افلام-هندي/', 'showMovies')
MOVIE_ASIAN = (f'{URL_MAIN}category/افلام-اسيوية/', 'showMovies')
MOVIE_TURK = (f'{URL_MAIN}category/افلام-تركي/', 'showMovies')
KID_MOVIES = (f'{URL_MAIN}category/افلام-كرتون/', 'showMovies')

SERIE_TR = (f'{URL_MAIN}category/مسلسلات-تركي-مترجمة/', 'showSeries')
SERIE_TR_AR = (f'{URL_MAIN}category/مسلسلات-تركي-مدبلجة/', 'showSeries')
SERIE_DUBBED = (f'{URL_MAIN}category/مسلسلات-اجنبية-مدبلجة/', 'showSeries')
SERIE_ASIA = (f'{URL_MAIN}category/مسلسلات-اسيوي-مترجمة/', 'showSeries')
SERIE_HEND = (f'{URL_MAIN}category/مسلسلات-هندي-مترجمة/', 'showSeries')
SERIE_HEND_AR = (f'{URL_MAIN}category/مسلسلات-هندي-مدبلجة/', 'showSeries')
SERIE_LATIN = (f'{URL_MAIN}category/مسلسلات-لاتينية/', 'showSeries')
SERIE_EN = (f'{URL_MAIN}category/مسلسلات-اجنبي/', 'showSeries')
SERIE_AR = (f'{URL_MAIN}category/مسلسلات-عربي/', 'showSeries')
RAMADAN_SERIES = (f'{URL_MAIN}category/مسلسلات-رمضان-2024/', 'showSeries')
KID_CARTOON = (f'{URL_MAIN}category/مسلسلات-كرتون-مترجمة/', 'showSeries')

DOC_SERIES = (f'{URL_MAIN}genre/وثائقي', 'showSeries')
SPORT_WWE = (f'{URL_MAIN}category/عروض-مصارعة-مترجمة/', 'showMovies')
ANIM_NEWS = (f'{URL_MAIN}category/مسلسلات-انمي-مترجمة/', 'showSeries')
ANIM_MOVIES = (f'{URL_MAIN}category/افلام-انمي/', 'showMovies')
# REPLAYTV_PLAY = (f'{URL_MAIN}category/مسرحيات/', 'showMovies')
REPLAYTV_NEWS = (f'{URL_MAIN}category/برامج-تلفزيونية/', 'showSeries')

URL_SEARCH_MOVIES = (f'{URL_MAIN}/?s=', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}/?s=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', RAMADAN_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'رمضان', 'rmdn.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية مدبلجة', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', 'arab.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', 'asia.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', 'turk.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', 'hend.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'crtoon.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انمي', 'anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', 'arab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', 'mdblg.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', 'hend.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND_AR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HEND_AR[1], 'مسلسلات هندية مدبلج', 'hend.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_LATIN [0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات لاتنية', 'latin.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', 'mdblg.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', KID_CARTOON[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات كرتون', 'anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', 'anime.png', oOutputParameterHandler)  

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}category/مسلسلات-انمي-مدبلجة/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي مدبلجة', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}category/مسلسلات-انمي-مدبلجة/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات كرتون مدبلجة', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات وثائقية', 'doc.png', oOutputParameterHandler) 

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيونية','brmg.png', oOutputParameterHandler)
	
    # oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_PLAY[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مسرحيات', 'msrh.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_WWE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مصارعة', 'wwe.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText :
        sUrl = f'{URL_MAIN}/?s={sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showSeriesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText :
        sUrl = f'{URL_MAIN}/?s={sSearchText}'
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<div class="block-post">\s*<a href="([^"]+)" title="([^"]+)".+?data-img="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)		
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if '/episode' in aEntry[0] or '/serie' in aEntry[0]:
                continue

            sTitle = (cUtil().CleanMovieName(aEntry[1])).replace("كول سيما","")
            siteUrl = f'{aEntry[0]}watch/'
            sThumb = aEntry[2].replace("(","").replace(")","")
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            			
            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    
        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        oOutputParameterHandler = cOutputParameterHandler()
        if sNextPage:
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
     
        oGui.setEndOfDirectory()
 
def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
        
    sPattern = '<div class="block-post">\s*<a href="([^"]+)" title="([^"]+)".+?data-img="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    itemList =[]
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if '/movie' in aEntry[0]:
                continue

            sTitle = (cUtil().CleanSeriesName(aEntry[1])).replace("كول سيما","")
            sTitle = re.sub(r"S\d{1,2}", "", sTitle)
            siteUrl = aEntry[0]          
            sThumb = aEntry[2]
            sDesc=''
            if sTitle not in itemList:
                itemList.append(sTitle)
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    
        progress_.VSclose(progress_)
    
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
			
def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()     
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div class="tabCon" id="seasons">'
    sEnd = '<div class="tabCon"'
    sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)
    
    sPattern = '<div class="block-post">\s*<a href="([^"]+)".+?data-img="([^"]+)".+?</li>\s*<li>(.+?)</li>'
    aResult = oParser.parse(sHtmlContent1, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:

            sSeason = aEntry[2].replace("الموسم ","S")
            sTitle = f'{sMovieTitle} {sSeason}'
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    else:

        sStart = '<div class="tabCon episodes" id="episodes">'
        sEnd = '</ul>'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = 'href="([^"]+)".+?<span>الحلقة</span>(.+?)</div>'
        aResult = oParser.parse(sHtmlContent, sPattern)   
        if aResult[0] is True:
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in aResult[1]:
                sEp = aEntry[1]
                sTitle = f'{sMovieTitle} E{sEp}'
                siteUrl = f'{aEntry[0]}watch/'
                sThumb = sThumb
                sDesc = ''
                sHost = ''

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sHost', sHost)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
             
                oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div class="tabCon" id="episodes">'
    sEnd = '</ul>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)".+?<span>الحلقة</span>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)   
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            sEp = aEntry[1]
            sTitle = f'{sMovieTitle} E{sEp}'
            siteUrl = f'{aEntry[0]}watch/'
            sThumb = sThumb
            sDesc = ''
            sHost = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sHost', sHost)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			    
            oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
      
    oGui.setEndOfDirectory()
	
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li><a class="next page-numbers" href="([^<]+)">'	 
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    
    return False

def showLinks(oInputParameterHandler = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    Referer = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern =  'vo_postID = "([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        sID = aResult[1][0] 

    sPattern = 'id="s_.+?onClick="([^"]+)".+?class="server">(.+?)</i>'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            ServerIDs = aEntry[0].replace('getServer2(this.id,','').replace(');','') 
            sHosterID = ServerIDs.split(',')[0]
            serverId = ServerIDs.split(',')[1]
      
            url = f'{URL_MAIN}wp-content/themes/coolcima/temp/ajax/iframe2.php?id={sID}&video={sHosterID}&serverId={serverId}'
            sHost = aEntry[1]
            sTitle = f'{sMovieTitle} [COLOR coral]{sHost}[/COLOR]'

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sHosterUrl', url)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sHost', sHost)
            oOutputParameterHandler.addParameter('Referer', Referer)

            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sTitle, oOutputParameterHandler)
                       
    sUrl = sUrl.replace('/watch/','/downloads/')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div class="DownList">'
    sEnd = '</div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)".+?</span><span>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            if 'megamax' in aEntry[0]:
                continue
            
            url = aEntry[0]
            sQual = aEntry[1]
            if url.startswith('//'):
               url = f'http:{url}'

            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               sDisplayTitle = f'{sMovieTitle} [COLOR coral] [{sQual}] [/COLOR]'
               oHoster.setDisplayName(sDisplayTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sHosterUrl = oInputParameterHandler.getValue('sHosterUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    Referer = oInputParameterHandler.getValue('Referer')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sHosterUrl)
    cook = oRequestHandler.GetCookies()
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', Referer.encode('utf-8'))
    oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-fetch-dest', 'empty'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-fetch-mode', 'cors'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('x-requested-with', 'XMLHttpRequest')
    sHtmlContent2 = oRequestHandler.request()
    
    sPattern = 'iframe.+?src="([^"]+)'
    aResult = oParser.parse(sHtmlContent2, sPattern)
    if aResult[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                sHosterUrl = aResult[1][0]
                if bool(re.search(r'mega.*max', sHosterUrl)) or 'lodcima' in sHosterUrl:
                    data = cMegamax().GetUrls(sHosterUrl)
                    if data is not False:
                        for item in data:
                            sHosterUrl = item.split(',')[0].split('=')[1]
                            sQual = item.split(',')[1].split('=')[1]
                            sLabel = item.split(',')[2].split('=')[1]

                            sDisplayTitle = f'{sMovieTitle} ({sQual}) [COLOR coral]{sLabel}[/COLOR]'    
                            oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                            oOutputParameterHandler.addParameter('siteUrl', sUrl)
                            oOutputParameterHandler.addParameter('sQual', sQual)
                            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                            oOutputParameterHandler.addParameter('sThumb', sThumb)
                            oGui.addLink(SITE_IDENTIFIER, 'showMegaLinks', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)	
  
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def showMegaLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sHosterUrl = oInputParameterHandler.getValue('sHosterUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()