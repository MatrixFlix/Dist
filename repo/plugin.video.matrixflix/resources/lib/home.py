# -*- coding: utf-8 -*-

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.search import cSearch
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import addon
from resources.sites.themoviedb_org import SITE_IDENTIFIER as SITE_TMDB
from resources.sites.anilist_co import SITE_IDENTIFIER as SITE_ANILIST
from resources.lib.trakt import SITE_IDENTIFIER as SITE_TRAKT

SITE_IDENTIFIER = 'cHome'
SITE_NAME = 'Home'

class cHome:

    addons = addon()

    def load(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showMenuSearch', self.addons.VSlang(30076), 'search.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('globalSources', 'globalSources', self.addons.VSlang(30138), 'host.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', self.addons.VSlang(30120), 'film.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', self.addons.VSlang(30121), 'mslsl.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showDocs', self.addons.VSlang(30112), 'doc.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showIslam', self.addons.VSlang(70009), 'islm.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showAnimes', self.addons.VSlang(30122), 'anime.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showSport', self.addons.VSlang(30113), 'sport.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showMenuTV', self.addons.VSlang(30132), 'live.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showReplay', self.addons.VSlang(30117), 'brmg.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showMyVideos', self.addons.VSlang(30130), 'mylist.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'ShowTools', self.addons.VSlang(30033), 'tools.png', oOutputParameterHandler)

        view = False
        if self.addons.getSetting('active-view') == 'true':
            view = self.addons.getSetting('accueil-view')

        oGui.setEndOfDirectory(view)

    def showMyVideos(self):
        oGui = cGui()

        oGui = cGui()
        oGui.addDir('cFav', 'getBookmarks', self.addons.VSlang(30207), 'mark.png')
        oGui.addDir('cViewing', 'showMenu', self.addons.VSlang(30125), 'continue.png')
        oGui.addDir('cWatched', 'showMenu', self.addons.VSlang(30321), 'history.png')
        oGui.addDir(SITE_IDENTIFIER, 'showUsers', self.addons.VSlang(30455), 'user.png')
        oGui.addDir('cDownload', 'getDownloadList', self.addons.VSlang(30229), 'download.png')

        oGui.setEndOfDirectory()

    def showSearchText(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()
        sSearchText = oGui.showKeyBoard(heading=self.addons.VSlang(30076))
        if not sSearchText:
            return False

        oSearch = cSearch()
        sCat = oInputParameterHandler.getValue('sCat')
        oSearch.searchGlobal(sSearchText, sCat)
        oGui.setEndOfDirectory()

    def showMenuSearch(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('themoviedb_org', 'load', self.addons.VSlang(30088), 'searchtmdb.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30078), 'film.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sCat', '2')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30079), 'mslsl.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sCat', '3')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30118), 'anime.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sCat', '5')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30080), 'search.png', oOutputParameterHandler)

        if self.addons.getSetting('history-view') == 'true':
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir('cHome', 'showHistory', self.addons.VSlang(30308), 'history.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showDocs(self):
        oGui = cGui()
        
        oOutputParameterHandler = cOutputParameterHandler()
        if self.addons.getSetting('history-view') == 'true':
            oOutputParameterHandler.addParameter('siteUrl', 'search/tv')
            oGui.addDir(SITE_IDENTIFIER, 'showDocsSearch', self.addons.VSlang(30076), 'search.png', oOutputParameterHandler)
        else:
            oOutputParameterHandler.addParameter('sCat', '5')
            oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30076), 'search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'DOC_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30112), self.addons.VSlang(30120)), 'film.png', oOutputParameterHandler)
		
        oOutputParameterHandler.addParameter('siteUrl', 'DOC_SERIES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30112), self.addons.VSlang(30121)), 'mslsl.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'DOC_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30112), self.addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)


        oGui.setEndOfDirectory()

    def showSport(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'TV')
        oGui.addDir('freebox', 'showWeb', self.addons.VSlang(30332), 'tv.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_FOOT')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30113), self.addons.VSlang(30134)), 'foot.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_LIVE')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30113), self.addons.VSlang(70011)), 'live.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_WWE')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30113), self.addons.VSlang(30135)), 'wwe.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30113), self.addons.VSlang(30105)), 'sport.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showMenuTV(self):
        oGui = cGui()
    
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'TV_GROUPS')
        oGui.addDir('freebox', 'showGroups', self.addons.VSlang(70016), 'genres.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'TV_CHANNELS')
        oGui.addDir('freebox', 'showAllChannels', self.addons.VSlang(70017), 'tv.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'TV')
        oGui.addDir('iptv', 'showWeb', self.addons.VSlang(70014), 'tv.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'TV')
        oGui.addDir('daily', 'showDailyList', '%s (%s)' % (self.addons.VSlang(30138), self.addons.VSlang(30230)),'tv.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'TV_TV')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30138), self.addons.VSlang(30200)), 'host.png', oOutputParameterHandler)
 
        oGui.setEndOfDirectory()

    def showIslam(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ISLAM_QURAN')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging',self.addons.VSlang(70003), 'quran.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'ISLAM_SHOWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(70009), self.addons.VSlang(30117)), 'brmg.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'ISLAM_NASHEED')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(70009), self.addons.VSlang(70004)), 'nsheed.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'ISLAM_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(70009), self.addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()


    def showMovies(self):
        oGui = cGui()
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30078), 'search.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'movies/Recommendations')
        oGui.addDir('cRecommendations', 'showMoviesRecommendations', self.addons.VSlang(70030), 'recommend.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showMoviesGlobal', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(70031)), 'tmdb.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_FAM')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(33107)), 'fam.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'KID_MOVIES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(70012)), 'anim.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_AR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30107)), 'arab.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_DUBBED')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(70002)), 'mdblg.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_EN')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30108)), 'agnab.png', oOutputParameterHandler)
		
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_4K')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(33108)), '4k.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_IR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(301048)), 'iran.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_TURK')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30109)), 'turk.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showMoviesAsia', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30104)), 'asia.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_HI')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30103)), 'hend.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_CLASSIC')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30501)), 'class.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_PACK')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(70013)), 'pack.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_POP')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30315)), 'pop.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_TOP')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(70001)), 'top.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_ANNEES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30106)), 'annees.png', oOutputParameterHandler)
		
        oGui.setEndOfDirectory()

    def showMoviesAsia(self):
        oGui = cGui()
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_ASIAN')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30104)), 'asia.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_KR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(301041)), 'kr.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_KR_AR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(301042)), 'kr.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_CN')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(301043)), 'cn.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_JP')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(301044)), 'jp.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_THAI')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(301045)), 'thai.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_VIET')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(301046)), 'viet.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_TA')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(301047)), 'ta.png', oOutputParameterHandler)
		
        oGui.setEndOfDirectory()

    def showMoviesGlobal(self):
        oGui = cGui()
        addons = self.addons

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'discover/movie')
        oGui.addDir(SITE_TMDB, 'showMoviesNews', addons.VSlang(30101), 'tmdb.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'discover/movie')
        oGui.addDir(SITE_TMDB, 'showMovies', addons.VSlang(30315), 'pop.png', oOutputParameterHandler)
        
        oOutputParameterHandler.addParameter('siteUrl', 'movies/boxoffice')
        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_TRAKT, 'getTrakt', addons.VSlang(30314), 'trakt.png', oOutputParameterHandler)
        
        oOutputParameterHandler.addParameter('siteUrl', 'genre/movie/list')
        oGui.addDir(SITE_TMDB, 'showGenreMovie', addons.VSlang(30105), 'genres.png', oOutputParameterHandler)
        
        oOutputParameterHandler.addParameter('siteUrl', 'discover/movie')
        oGui.addDir(SITE_TMDB, 'showMoviesYears', self.addons.VSlang(30106), 'annees.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'movies/popular')
        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_TRAKT, 'getTrakt', self.addons.VSlang(30427), 'trakt.png', oOutputParameterHandler)
		
        oGui.setEndOfDirectory()

    def showSeries(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '2')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30079), 'search.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'shows/Recommendations')
        oGui.addDir('cRecommendations', 'showShowsRecommendations', self.addons.VSlang(70030), 'recommend.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showSeriesGlobal', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(70031)), 'tmdb.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'RAMADAN_SERIES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(70006)), 'rmdn.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'KID_CARTOON')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(70012)), 'crtoon.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_DUBBED')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(70002)), 'mdblg.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_AR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30107)), 'arab.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_EN')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30108)), 'agnab.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_IR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(301048)), 'iran.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_TR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30109)), 'turk.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_TR_AR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(31110)), 'turk.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showSeriesAsia', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30104)), 'asia.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_PAK')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(301111)), 'paki.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_HEND')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30103)), 'hend.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_HEND_AR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30136)), 'hend.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_LATIN')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30137)), 'latin.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_ANNEES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30106)), 'annees.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showSeriesGlobal(self):
        oGui = cGui()
        addons = self.addons

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'discover/tv')
        oGui.addDir(SITE_TMDB, 'showSeriesNews', addons.VSlang(30101), 'tmdb.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'shows/trending')
        oOutputParameterHandler.addParameter('sCat', '2')
        oGui.addDir(SITE_TRAKT, 'getTrakt', addons.VSlang(30315), 'trakt.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'genre/tv/list')
        oGui.addDir(SITE_TMDB, 'showSeriesNetworks', addons.VSlang(70032), 'netflix.png', oOutputParameterHandler)
    
        oOutputParameterHandler.addParameter('siteUrl', 'genre/tv/list')
        oGui.addDir(SITE_TMDB, 'showGenreTV', addons.VSlang(30105), 'genres.png', oOutputParameterHandler)
    
        oOutputParameterHandler.addParameter('siteUrl', 'discover/tv')
        oGui.addDir(SITE_TMDB, 'showSeriesTop', addons.VSlang(30431), 'top.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'discover/tv')
        oGui.addDir(SITE_TMDB, 'showSeriesYears', self.addons.VSlang(30106), 'annees.png', oOutputParameterHandler)
		
        oGui.setEndOfDirectory()

    def showSeriesAsia(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_ASIA')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30104)), 'asia.png', oOutputParameterHandler)   

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_KR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(301041)), 'kr.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_KR_AR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(301042)), 'kr.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_CN')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(301043)), 'cn.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_JP')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(301044)), 'jp.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_THAI')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(301045)), 'thai.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_VIET')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(301046)), 'viet.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_TA')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(301047)), 'ta.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showAnimes(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()

        if self.addons.getSetting('history-view') == 'true':
            oOutputParameterHandler.addParameter('siteUrl', 'search/tv')
            oGui.addDir(SITE_IDENTIFIER, 'showAnimesSearch', self.addons.VSlang(30076), 'search.png', oOutputParameterHandler)
        else:
            oOutputParameterHandler.addParameter('sCat', '3')
            oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30076), 'search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30121)), 'mslsl.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_MOVIES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30120)), 'film.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'discover/tv')
        oGui.addDir(SITE_ANILIST, 'showAnimesNews', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30101)), 'anime.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'discover/tv')
        oGui.addDir(SITE_ANILIST, 'showAnimesTrending', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(70008)), 'pop.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'discover/tv')
        oGui.addDir(SITE_ANILIST, 'showAnimesTop', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(70001)), 'top.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showAnimesSearch(self):
        oGui = cGui()
        oOutputParameterHandler = cOutputParameterHandler()

        oOutputParameterHandler.addParameter('sCat', '3')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30118), 'search.png', oOutputParameterHandler)
    
        if self.addons.getSetting('history-view') == 'true':
            oOutputParameterHandler.addParameter('sCat', '3')
            oGui.addDir(SITE_IDENTIFIER, 'showHistory', self.addons.VSlang(30308), 'history.png', oOutputParameterHandler)
    
    
        oGui.setEndOfDirectory()

    def showReplay(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'REPLAYTV_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30117), self.addons.VSlang(30101)), 'brmg.png', oOutputParameterHandler)


        oOutputParameterHandler.addParameter('siteUrl', 'REPLAYTV_PLAY')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30117), self.addons.VSlang(70010)), 'msrh.png', oOutputParameterHandler)

        #oOutputParameterHandler.addParameter('siteUrl', 'REPLAYTV_GENRES')
        #oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30117), self.addons.VSlang(30105)), 'replay_genres.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showUsers(self):
        oGui = cGui()

        oGui.addDir('themoviedb_org', 'showMyTmdb', 'TMDB', 'tmdb.png')
        oGui.addDir('cTrakt', 'getLoad', self.addons.VSlang(30214), 'trakt.png')

        oGui.setEndOfDirectory()

    def ShowTools(self):
        oGui = cGui()

        oGui = cGui()
        oGui.addDir(SITE_IDENTIFIER, 'opensetting', self.addons.VSlang(30227), 'notes.png')
        oGui.addDir('cDownload', 'getDownload', self.addons.VSlang(30224), 'download.png')
        oGui.addDir('cLibrary', 'getLibrary', self.addons.VSlang(30303), 'library.png')
        oGui.addDir(SITE_IDENTIFIER, 'showHostDirect', self.addons.VSlang(30469), 'host.png')

        oGui.setEndOfDirectory()

    def opensetting(self):
        addon().openSettings()
			
    def showHistory(self):
        oGui = cGui()

        oInputParameterHandler = cInputParameterHandler()
        sCat = oInputParameterHandler.getValue('sCat')

        from resources.lib.db import cDb
        with cDb() as db:
            row = db.get_history(sCat)

        if row:
            oGui.addText(SITE_IDENTIFIER, self.addons.VSlang(30416), '')
        else:
            oGui.addText(SITE_IDENTIFIER)
        oOutputParameterHandler = cOutputParameterHandler()
        for match in row:
            sTitle = match['title']
            sCat = match['disp']

            # we only offer history for movies, series, anime, doc, drama
            if int(sCat) not in (1, 2, 3, 5, 9):
                continue 

            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oOutputParameterHandler.addParameter('searchtext', sTitle)

            oGuiElement = cGuiElement()
            oGuiElement.setSiteName('globalSearch')
            oGuiElement.setFunction('globalSearch')

            try:
                oGuiElement.setTitle('- ' + sTitle)
            except:
                oGuiElement.setTitle('- ' + str(sTitle, 'utf-8'))

            oGuiElement.setFileName(sTitle)
            oGuiElement.setCat(sCat)
            oGuiElement.setIcon('search.png')
            oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, 'cHome', 'delSearch', self.addons.VSlang(30412))
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        if row:
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'delSearch', self.addons.VSlang(30413), 'trash.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def delSearch(self):
        from resources.lib.db import cDb
        with cDb() as db:
            db.del_history()
        return True

    def callpluging(self):
        oGui = cGui()

        oInputParameterHandler = cInputParameterHandler()
        sSiteUrl = oInputParameterHandler.getValue('siteUrl')

        oPluginHandler = cPluginHandler()
        aPlugins = oPluginHandler.getAvailablePlugins(sSiteUrl)
        oOutputParameterHandler = cOutputParameterHandler()
        for aPlugin in aPlugins:
            try:
                icon = 'sites/%s.png' % (aPlugin[2])
                oOutputParameterHandler.addParameter('siteUrl', aPlugin[0])
                oGui.addDir(aPlugin[2], aPlugin[3], aPlugin[1], icon, oOutputParameterHandler)
            except:
                pass

        oGui.setEndOfDirectory()

    def showHostDirect(self):  # fonction de recherche
        oGui = cGui()
        sUrl = oGui.showKeyBoard(heading=self.addons.VSlang(30045))
        if (sUrl != False):

            oHoster = cHosterGui().checkHoster(sUrl)
            if (oHoster != False):
                oHoster.setDisplayName(self.addons.VSlang(30046))
                oHoster.setFileName(self.addons.VSlang(30046))
                cHosterGui().showHoster(oGui, oHoster, sUrl, '')

        oGui.setEndOfDirectory()
