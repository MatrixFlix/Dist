# -*- coding: utf-8 -*-

import re
import base64
import xbmcgui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, siteManager, addon
from resources.lib import random_ua

UA = random_ua.get_pc_ua()

SITE_IDENTIFIER = 'arabflix'
SITE_NAME = 'Arab-Flix'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

sHost = base64.b64decode(URL_MAIN)
dHost = sHost.decode("utf-8")

URL_MAIN = dHost[::-1]
MOVIE_EN = (f'{URL_MAIN}api/content/categories/', 'showMovies')
SERIE_EN = (f'{URL_MAIN}api/content/categories/', 'showSeries')

URL_SEARCH_MOVIES = (f'{URL_MAIN}api/content/search/', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}api/content/search/', 'showSeries')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()
    addons = addon()

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

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText :
        sUrl = f'{URL_MAIN}api/content/search/{sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showSeriesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText :
        sUrl = f'{URL_MAIN}api/content/search/{sSearchText}'
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    oOutputParameterHandler = cOutputParameterHandler()
    if sSearch:
        sUrl = sSearch

        oRequestHandler = cRequestHandler(f"{sUrl.split('/search/')[0]}/search/")
        oRequestHandler.addHeaderEntry('Accept', 'application/json, text/plain, */*')
        oRequestHandler.addHeaderEntry('accept-language', 'en-US,en;q=0.9,ar;q=0.8')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', f'{URL_MAIN}movies')
        oRequestHandler.addHeaderEntry('Origin', URL_MAIN[:-1])
        oRequestHandler.addJSONEntry('search', sUrl.split('/search/')[1])
        oRequestHandler.addJSONEntry('offset', 0)
        oRequestHandler.setRequestType(1)
        sHtmlContent = oRequestHandler.request(jsonDecode=True)
        
        for aEntry in sHtmlContent["search"]:
            if aEntry["type"] != "movie":
                continue

            movie_id = aEntry["id"]
            siteUrl = f'{URL_MAIN}api/watch/'
            sTitle = aEntry["title"]
            sThumb = aEntry["poster"]
            sDesc = aEntry["description"]

            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sType', 'movie')
            oOutputParameterHandler.addParameter('watch_id', movie_id)
                            
            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('Accept', 'application/json, text/plain, */*')
        oRequestHandler.addHeaderEntry('accept-language', 'en-US,en;q=0.9,ar;q=0.8')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', f'{URL_MAIN}movies')
        oRequestHandler.addHeaderEntry('Origin', URL_MAIN[:-1])
        oRequestHandler.addJSONEntry('type', "movie")
        oRequestHandler.addJSONEntry('cw', [])
        oRequestHandler.setRequestType(1)
        sHtmlContent = oRequestHandler.request(jsonDecode=True)
        
        category_names = list(sHtmlContent.keys())
        index = xbmcgui.Dialog().select("Select Category", category_names)

        if index != -1:
            selected_category = category_names[index]
            selected_items = sHtmlContent[selected_category]
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in selected_items:

                movie_id = aEntry["id"]
                siteUrl = f'{URL_MAIN}api/watch/'
                sTitle = aEntry["title"]
                sThumb = aEntry["poster"]
                sDesc = aEntry["description"]

                m = re.search('([0-9]{4})', sTitle)
                if m:
                    sYear = str(m.group(0))
                    sTitle = sTitle.replace(sYear,'')

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sType', 'movie')
                oOutputParameterHandler.addParameter('watch_id', movie_id)
                                
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    
    if not sSearch:
        oGui.setEndOfDirectory()  
 
def showSeries(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    oOutputParameterHandler = cOutputParameterHandler()
    if sSearch:
        sUrl = sSearch

        oRequestHandler = cRequestHandler(f"{sUrl.split('/search/')[0]}/search/")
        oRequestHandler.addHeaderEntry('Accept', 'application/json, text/plain, */*')
        oRequestHandler.addHeaderEntry('accept-language', 'en-US,en;q=0.9,ar;q=0.8')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', f'{URL_MAIN}movies')
        oRequestHandler.addHeaderEntry('Origin', URL_MAIN[:-1])
        oRequestHandler.addJSONEntry('search', sUrl.split('/search/')[1])
        oRequestHandler.addJSONEntry('offset', 0)
        oRequestHandler.setRequestType(1)
        sHtmlContent = oRequestHandler.request(jsonDecode=True)
        
        for aEntry in sHtmlContent["search"]:
            if aEntry["type"] != "series":
                continue

            serie_id = aEntry["id"]
            siteUrl = f'{URL_MAIN}api/content/seasons/'
            sTitle = aEntry["title"]
            sThumb = aEntry["poster"]
            sDesc = aEntry["description"]

            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('serie_id', serie_id)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)  

            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('Accept', 'application/json, text/plain, */*')
        oRequestHandler.addHeaderEntry('accept-language', 'en-US,en;q=0.9,ar;q=0.8')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', f'{URL_MAIN}shows')
        oRequestHandler.addHeaderEntry('Origin', URL_MAIN[:-1])
        oRequestHandler.addJSONEntry('type', "series")
        oRequestHandler.addJSONEntry('cw', [])
        oRequestHandler.setRequestType(1)
        sHtmlContent = oRequestHandler.request(jsonDecode=True)
        
        category_names = list(sHtmlContent.keys())
        index = xbmcgui.Dialog().select("Select Category", category_names)

        if index != -1:
            selected_category = category_names[index]
            selected_items = sHtmlContent[selected_category]
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in selected_items:

                serie_id = aEntry["id"]
                siteUrl = f'{URL_MAIN}api/content/seasons/'
                sTitle = aEntry["title"]
                sThumb = aEntry["poster"]
                sDesc = aEntry["description"]

                m = re.search('([0-9]{4})', sTitle)
                if m:
                    sYear = str(m.group(0))
                    sTitle = sTitle.replace(sYear,'')

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('serie_id', serie_id)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)  

                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()  
			
def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    serie_id = oInputParameterHandler.getValue('serie_id')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', f'{URL_MAIN}shows')
    oRequestHandler.addHeaderEntry('Origin', URL_MAIN[:-1])
    oRequestHandler.addJSONEntry('id', int(serie_id))
    oRequestHandler.setRequestType(1)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    oOutputParameterHandler = cOutputParameterHandler()
    for aEntry in sHtmlContent:

        season_id = aEntry["id"]
        siteUrl = f'{URL_MAIN}api/content/episodes/'
        sTitle = f'{sMovieTitle} {aEntry["title"]}'
        sSeason = re.search(r'\d+', aEntry["title"]).group() if re.search(r'\d+', aEntry["title"]) else 1

        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('season_id', season_id)
        oOutputParameterHandler.addParameter('series_id', serie_id)
        oOutputParameterHandler.addParameter('season_no', sSeason)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)  
        
        oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    series_id = oInputParameterHandler.getValue('series_id')
    season_id = oInputParameterHandler.getValue('season_id')
    season_no = oInputParameterHandler.getValue('season_no')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Accept', 'application/json, text/plain, */*')
    oRequestHandler.addHeaderEntry('accept-language', 'en-US,en;q=0.9,ar;q=0.8')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', f'{URL_MAIN}shows')
    oRequestHandler.addHeaderEntry('Origin', URL_MAIN[:-1])
    oRequestHandler.addJSONEntry('id', int(season_id))
    oRequestHandler.setRequestType(1)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    oOutputParameterHandler = cOutputParameterHandler()
    episode_number = 0
    for aEntry in sHtmlContent:
        episode_number += 1
        episode_id = aEntry["id"]
        siteUrl = f'{URL_MAIN}api/watch/'
        sTitle = f'{sMovieTitle} E{episode_number}'

        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('watch_id', series_id)
        oOutputParameterHandler.addParameter('season_no', season_no)
        oOutputParameterHandler.addParameter('episode_no', episode_number)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb) 
        oOutputParameterHandler.addParameter('sType', 'series')  
			    
        oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
      
    oGui.setEndOfDirectory()
	
def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sType = oInputParameterHandler.getValue('sType')
    watch_id = oInputParameterHandler.getValue('watch_id')
    episode_no = oInputParameterHandler.getValue('episode_no')
    season_no = oInputParameterHandler.getValue('season_no')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Accept', 'application/json, text/plain, */*')
    oRequestHandler.addHeaderEntry('accept-language', 'en-US,en;q=0.9,ar;q=0.8')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', f'{URL_MAIN}shows')
    oRequestHandler.addHeaderEntry('Origin', URL_MAIN[:-1])
    oRequestHandler.addJSONEntry('id', int(watch_id))
    if sType == 'series':
        oRequestHandler.addJSONEntry('s', int(season_no))
        oRequestHandler.addJSONEntry('e', int(episode_no))
    oRequestHandler.addJSONEntry('type', sType)
    oRequestHandler.setRequestType(1)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    try:
        imdbId = sHtmlContent["imdbId"].replace('tt','')
        subUrl = f'https://rest.opensubtitles.org/search/imdbid-{imdbId}/sublanguageid-ara'
        if sType == 'series':
            subUrl = f"https://rest.opensubtitles.org/search/episode-{episode_no}/imdbid-{imdbId}/season-{season_no}/sublanguageid-ara"

    except:
        VSlog('Failed to get subs')

    for aEntry in sHtmlContent["servers"]:
        sThumb = sHtmlContent["thumb"]
        sHosterUrl = aEntry["url"]
        if 'flixhq' in sHosterUrl:
            sHosterUrl = sHosterUrl.split('&url=')[1].split('&headers')[0]
        sHosterUrl = sHosterUrl + f'?sub.info={subUrl}'
        oHoster = cHosterGui().getHoster('aflix') 
        if oHoster:
            sDisplayTitle = sMovieTitle
            oHoster.setDisplayName(sDisplayTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
