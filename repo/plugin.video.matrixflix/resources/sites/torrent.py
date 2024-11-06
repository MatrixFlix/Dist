# -*- coding: utf-8 -*-

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import progress, addon, isMatrix, VSlog
from resources.lib.util import cUtil
from resources.lib.tmdb import cTMDb
import re

SITE_IDENTIFIER = 'torrent'
SITE_NAME = '[COLOR orange]Torrent[/COLOR]'
SITE_DESC = 'Torrent Hosters'

URL_MAIN = 'https://www.themoviedb.org/'

API_VERS = '3'
API_URL = URL_MAIN + API_VERS

view = '500'
tmdb_session = ''
tmdb_account = ''

MOVIE_EN = ('movie/now_playing', 'showMovies')
MOVIE_TOP = ('movie/top_rated', 'showMovies')
MOVIE_POP = ('movie/popular', 'showMovies')
MOVIE_4k = ('movie/popular', 'showMovies')
MOVIE_GENRES = ('genre/movie/list', 'showGenreMovie')

SERIE_EN = ('tv/popular', 'showSeries')

URL_SEARCH_MOVIES = ('https://api.themoviedb.org/3/search/movie?include_adult=false&query=', 'showMoviesSearch')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', '%s (TMDB)' % addons.VSlang(30330), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'movie/popular')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', addons.VSlang(30425), 'comments.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'movie/now_playing')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', addons.VSlang(30426), 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'movie/top_rated')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', addons.VSlang(30427), 'notes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'tv/popular')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', addons.VSlang(30429), 'comments.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'tv/on_the_air')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', addons.VSlang(30430), 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'tv/top_rated')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', addons.VSlang(30431), 'notes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'search/movie')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovie', addons.VSlang(30423), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'search/tv')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSerie', addons.VSlang(30424), 'search.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearchMovie():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        showMovies(sSearchText.replace(' ', '+'))
        return

def showSearchSerie():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        showSeries(sSearchText.replace(' ', '+'))
        return

def showMovies(sSearch=''):
    oGui = cGui()
    grab = cTMDb()

    oInputParameterHandler = cInputParameterHandler()

    iPage = 1
    term = ''
    if oInputParameterHandler.exist('page'):
        iPage = oInputParameterHandler.getValue('page')

    if oInputParameterHandler.exist('sSearch'):
        sSearch = oInputParameterHandler.getValue('sSearch')

    if sSearch:
        result = grab.getUrl('search/movie', iPage, 'query=' + sSearch)
        sUrl = ''

    else:
        if oInputParameterHandler.exist('session_id'):
            term += 'session_id=' + oInputParameterHandler.getValue('session_id')

        sUrl = oInputParameterHandler.getValue('siteUrl')
        result = grab.getUrl(sUrl, iPage, term)

    try:
        total = len(result)
        if total > 0:
            total = len(result['results'])
            progress_ = progress().VScreate(SITE_NAME)

            for i in result['results']:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break

                i = grab._format(i, '', "movie")

                sId, sTitle, simdb_id, sThumb, sDesc, sYear = i['tmdb_id'], i['title'], i['imdb_id'], i['poster_path'], i['plot'], i['year']

                if not isMatrix():
                    sTitle = sTitle.encode("utf-8")
                siteUrl = f'tmdbId={sId}&imdbId={simdb_id}'
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('simdb_id', simdb_id)
                oOutputParameterHandler.addParameter('sTmdbId', sId)
                oOutputParameterHandler.addParameter('sType', 'movie')
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

            progress_.VSclose(progress_)

            if int(iPage) > 0:
                iNextPage = int(iPage) + 1
                oOutputParameterHandler = cOutputParameterHandler()
                if sSearch:
                    oOutputParameterHandler.addParameter('sSearch', sSearch)

                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('page', iNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + str(iNextPage), oOutputParameterHandler)

    except:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]لم يتم العثور على نتائج.[/COLOR]')

    oGui.setEndOfDirectory()


def showSeries(sSearch=''):
    grab = cTMDb()

    oInputParameterHandler = cInputParameterHandler()

    iPage = 1
    term = ''
    if oInputParameterHandler.exist('page'):
        iPage = oInputParameterHandler.getValue('page')

    if oInputParameterHandler.exist('sSearch'):
        sSearch = oInputParameterHandler.getValue('sSearch')

    if sSearch:
        result = grab.getUrl('search/tv', iPage, 'query=' + sSearch)
        sUrl = ''

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

        if oInputParameterHandler.exist('genre'):
            term = 'with_genres=' + oInputParameterHandler.getValue('genre')

        if oInputParameterHandler.exist('session_id'):
            term += 'session_id=' + oInputParameterHandler.getValue('session_id')

        result = grab.getUrl(sUrl, iPage, term)

    oGui = cGui()

    try:
        total = len(result)

        if total > 0:
            total = len(result['results'])
            progress_ = progress().VScreate(SITE_NAME)

            for i in result['results']:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break

                i = grab._format(i, '', "tvshow")
                sId, simdb_id, sTitle, sGenre, sThumb, sFanart, sDesc, sYear = i['tmdb_id'], i['imdb_id'], i['title'], i['genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']

                if not isMatrix():
                    sTitle = sTitle.encode("utf-8")

                sSiteUrl = 'tv/' + str(sId)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sSiteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sId', sId)
                oOutputParameterHandler.addParameter('sFanart', sFanart)
                oOutputParameterHandler.addParameter('sTmdbId', sId)
                oOutputParameterHandler.addParameter('simdb_id', simdb_id)

                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

            progress_.VSclose(progress_)

            if int(iPage) > 0:
                iNextPage = int(iPage) + 1
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('page', iNextPage)
                if sSearch:
                    oOutputParameterHandler.addParameter('sSearch', sSearch)
                if oInputParameterHandler.exist('genre'):
                    oOutputParameterHandler.addParameter('genre', oInputParameterHandler.getValue('genre'))
                oGui.addNext(SITE_IDENTIFIER, 'showSeries', 'Page ' + str(iNextPage), oOutputParameterHandler)

    except TypeError:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]لم يتم العثور على نتائج.[/COLOR]')

    oGui.setEndOfDirectory()


def showSeasons():
    oGui = cGui()
    grab = cTMDb()
    addons = addon()

    oInputParameterHandler = cInputParameterHandler()

    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sFanart = oInputParameterHandler.getValue('sFanart')
    sTmdbId = oInputParameterHandler.getValue('sTmdbId')
    sId = oInputParameterHandler.getValue('sId')
    simdb_id = oInputParameterHandler.getValue('simdb_id')

    if not sId:
        sId = sUrl.split('/')[-1]

    if not sFanart:
        sFanart = ''

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sMovieTitle)

    if not isMatrix():
        oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(sMovieTitle))
    else:
        oOutputParameterHandler.addParameter('searchtext', sMovieTitle)

    result = grab.getUrl(sUrl)
    total = len(result)
    if total > 0:
        total = len(result['seasons'])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()

        for i in result['seasons']:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sNbreEp, SSeasonNum = i['episode_count'], i['season_number']

            i = grab._format(i, '', "season")
            sTitle, sGenre, sThumb, sFanart, sDesc, sYear = i['title'], i['genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']

            sTitle = 'Saison ' + str(SSeasonNum) + ' (' + str(sNbreEp) + ')'

            sUrl = 'tv/' + str(sId) + '/season/' + str(SSeasonNum)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sId', sId)
            oOutputParameterHandler.addParameter('sSeason', SSeasonNum)
            oOutputParameterHandler.addParameter('sFanart', sFanart)
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
            oOutputParameterHandler.addParameter('simdb_id', simdb_id)

            oGui.addSeason(SITE_IDENTIFIER, 'showSeriesEpisode', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showSeriesEpisode():
    grab = cTMDb()
    addons = addon()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sFanart = oInputParameterHandler.getValue('sFanart')
    sTmdbId = oInputParameterHandler.getValue('sTmdbId')
    simdb_id = oInputParameterHandler.getValue('simdb_id')

    sSeason = oInputParameterHandler.getValue('sSeason')
    if not sSeason:
        sSeason = sUrl.split('/')[-1]

    if not sFanart:
        sFanart = ''

    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sMovieTitle)
    search = '%s S%02d' % (sMovieTitle, int(sSeason))

    if not isMatrix():
        oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(search))
    else:
        oOutputParameterHandler.addParameter('searchtext', search)

    result = grab.getUrl(sUrl)

    total = len(result)
    if total > 0 and 'episodes' in result:
        total = len(result['episodes'])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()

        for i in result['episodes']:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sEpNumber = i['episode_number']

            i = grab._format(i, '')
            sTitle, sGenre, sThumb, sFanart, sDesc, sYear = i['title'], i['genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']

            if not isMatrix():
                sTitle = sTitle.encode("utf-8")

            sTitle = 'S%s E%s %s' % (sSeason, str(sEpNumber), sTitle)

            sExtraTitle = ' S' + "%02d" % int(sSeason) + 'E' + "%02d" % int(sEpNumber)

            oOutputParameterHandler.addParameter('siteUrl', sMovieTitle + '|' + sExtraTitle)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
            oOutputParameterHandler.addParameter('simdb_id', simdb_id)
            oOutputParameterHandler.addParameter('sSeason', sSeason)
            oOutputParameterHandler.addParameter('sEpisode', sEpNumber)
            oOutputParameterHandler.addParameter('sType', 'tv')
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    simdb_id = oInputParameterHandler.getValue('simdb_id')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sSeason = oInputParameterHandler.getValue('sSeason')
    sEpisode = oInputParameterHandler.getValue('sEpisode')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sType = oInputParameterHandler.getValue('sType')
    sTmdbId = oInputParameterHandler.getValue('sTmdbId')
    
    if simdb_id == '' or simdb_id is False:
        addons = addon()
        API_Key = addons.getSetting('api_tmdb')

        if sType == 'movie':
            sApi = f'https://api.themoviedb.org/3/movie/{sTmdbId}?api_key={API_Key}'
        else:
            sApi = f'https://api.themoviedb.org/3/tv/{sTmdbId}/external_ids?api_key={API_Key}'
        oRequestHandler = cRequestHandler(sApi)
        data = oRequestHandler.request(jsonDecode=True)

        simdb_id = data["imdb_id"]

    oOutputParameterHandler = cOutputParameterHandler()
    for sServer in ['apiBay', 'Torrentio', 'YTX', 'PopcornTime', 'EZTV']:
        sDisplayTitle = f'{sMovieTitle} [COLOR coral]- {sServer}[/COLOR]'      
        oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
        oOutputParameterHandler.addParameter('simdb_id', simdb_id)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sSeason', sSeason)
        oOutputParameterHandler.addParameter('sEpisode', sEpisode)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sServer', sServer)
        oOutputParameterHandler.addParameter('sType', sType)

        oGui.addLink(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sHosterUrl = oInputParameterHandler.getValue('sHosterUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sEpisode = oInputParameterHandler.getValue('sEpisode')
    sSeason = oInputParameterHandler.getValue('sSeason')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sServer = oInputParameterHandler.getValue('sServer')
    simdb_id = oInputParameterHandler.getValue('simdb_id')
    sType = oInputParameterHandler.getValue('sType')


    if sServer == 'EZTV':
        try:
            from resources.lib.scrapers.eztv import get_links

            sLinks = get_links(sType, simdb_id, sMovieTitle, sSeason, sEpisode)
            for item in sLinks:
                sTitle = item[0].replace("."," ").replace("\n", "")
                sTitle = ' '.join(re.findall(r'S\d{2}E\d{2}', sTitle)) + ' ' + re.sub(r'S\d{2}E\d{2}', '', sTitle).strip()
                sDisplayTitle = f'File: {sTitle.lower()}\nQuality: [COLOR orange]{item[3]}[/COLOR] Size: [COLOR gold]{item[2]}[/COLOR]'
                sHosterUrl = item[1]
    
                oHoster = cHosterGui().getHoster('torrent')
                if oHoster:  
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        except:
            VSlog('Error')

    if sServer == 'PopcornTime':
        try:
            from resources.lib.scrapers.yrkde import get_links

            sLinks = get_links(sType, simdb_id, sMovieTitle, sSeason, sEpisode)
            for item in sLinks:
                sTitle = item[0].replace("."," ").replace("\n", "")
                sTitle = ' '.join(re.findall(r'S\d{2}E\d{2}', sTitle)) + ' ' + re.sub(r'S\d{2}E\d{2}', '', sTitle).strip()
                sDisplayTitle = f'File: {sTitle.lower()}\nQuality: [COLOR orange]{item[3]}[/COLOR] Size: [COLOR gold]{item[2]}[/COLOR]'
                sHosterUrl = item[1]
    
                oHoster = cHosterGui().getHoster('torrent')
                if oHoster:  
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        except:
            VSlog('Error')

    elif sServer == 'Torrentio':
        try:
            from resources.lib.scrapers.torrentio import get_links

            sLinks = get_links(sType, simdb_id, sMovieTitle, sSeason, sEpisode)
            for item in sLinks:
                sTitle = item[0].replace("."," ").replace("\n", "")
                sTitle = ' '.join(re.findall(r'S\d{2}E\d{2}', sTitle)) + ' ' + re.sub(r'S\d{2}E\d{2}', '', sTitle).strip()
                sDisplayTitle = f'File: {sTitle.lower()}\nQuality: [COLOR orange]{item[3]}[/COLOR] Size: [COLOR gold]{item[2]}[/COLOR]'          
                sHosterUrl = item[1]
    
                oHoster = cHosterGui().getHoster('torrent')
                if oHoster:  
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        except:
            VSlog('Error')

    elif sServer == 'apiBay':
        try:
            from resources.lib.scrapers import apibay
            
            sLinks = apibay.get_links(sType, simdb_id, sMovieTitle, sSeason, sEpisode)
            for item in sLinks:
                sTitle = item[0].replace("."," ").replace("\n", "")
                sTitle = ' '.join(re.findall(r'S\d{2}E\d{2}', sTitle)) + ' ' + re.sub(r'S\d{2}E\d{2}', '', sTitle).strip()
                sDisplayTitle = f'File: {sTitle.lower()}\nQuality: [COLOR orange]{item[3]}[/COLOR] Size: [COLOR gold]{item[2]}[/COLOR]'              
                sHosterUrl = item[1]
    
                oHoster = cHosterGui().getHoster('torrent')
                if oHoster:  
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        except:
            VSlog('Error')

    elif sServer == 'YTX':
        try:
            from resources.lib.scrapers import yts
            
            sLinks = yts.get_links(sType, simdb_id, sMovieTitle, '', '')
            for item in sLinks:
                sTitle = item[0].replace("."," ").replace("\n", "")
                sDisplayTitle = f'File: {sTitle}\nQuality: [COLOR orange]{item[3]}[/COLOR] Size: [COLOR gold]{item[2]}[/COLOR]'                
                sHosterUrl = item[1]
    
                oHoster = cHosterGui().getHoster('torrent')
                if oHoster:  
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        except:
            VSlog('Error')

    oGui.setEndOfDirectory()
