# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re
import xbmc
from resources.lib.comaddon import addon, isMatrix, isNexus, VSlog
from resources.lib.db import cDb
from resources.lib.util import cUtil, QuoteSafe

class cGuiElement:

    DEFAULT_FOLDER_ICON = 'library.png'

    def __init__(self):

        self.addons = addon()
        self.__sFunctionName = ''
        self.__sRootArt = 'special://home/addons/plugin.video.matrixflix/resources/art/'
        self.__sType = 'video'
        self.__sMeta = 0
        self.__sTrailer = ''
        self.__sMetaAddon = self.addons.getSetting('meta-view')
        self.__sMediaUrl = ''
        self.__sSiteUrl = ''
        self.__sTitle = ''
        self.__sCleanTitle = ''
        self.__sTitleWatched = ''
        self.__ResumeTime = 0
        self.__TotalTime = 0
        self.__sFileName = ''
        self.__sDescription = ''
        self.__sGenre = ''
        self.__sThumbnail = ''
        self.__sPoster = ''
        self.__Season = ''
        self.__Episode = ''
        self.__sIcon = self.DEFAULT_FOLDER_ICON
        self.__sFanart = self.__sRootArt + 'fanart.jpg'
        self.poster = 'https://image.tmdb.org/t/p/%s' % self.addons.getSetting('poster_tmdb')
        self.fanart = 'https://image.tmdb.org/t/p/%s' % self.addons.getSetting('backdrop_tmdb')
        self.sDecoColor = self.addons.getSetting('deco_color')
        self.__TmdbId = ''
        self.__ImdbId = ''
        self.__Year = ''
        self.__sRes = ''

        self.__aItemValues = {}
        self.__aProperties = {}
        self.__aContextElements = []
        self.__sSiteName = ''
        self.__sCat = ''

    def setType(self, sType):
        self.__sType = sType

    def getType(self):
        return self.__sType

    def setCat(self, sCat):
        self.__sCat = int(sCat)

    def getCat(self):
        return self.__sCat

    def setMetaAddon(self, sMetaAddon):
        self.__sMetaAddon = sMetaAddon

    def getMetaAddon(self):
        return self.__sMetaAddon

    def setTrailer(self, sTrailer):
        self.__sTrailer = sTrailer

    def getTrailer(self):
        return self.__sTrailer

    def setTmdbId(self, data):
        self.__TmdbId = data if data != '0' else ''

    def getTmdbId(self):
        return self.__TmdbId

    def setImdbId(self, data):
        self.__ImdbId = data

    def getImdbId(self):
        return self.__ImdbId

    def setYear(self, data):
        self.__Year = data

    def getYear(self):
        return self.__Year

    def setRes(self, data):
        if data.upper() in ('1080P', 'FHD', 'FULLHD'):
            data = '1080p'
        elif data.upper() in ('720P', 'DVDRIP', 'DVDSCR', 'HD', 'HDLIGHT', 'HDRIP', 'BDRIP', 'BRRIP'):
            data = '720p'
        elif data.upper() in ('4K', 'UHD', '2160P'):
            data = '2160p'

        self.__sRes = data

    def getRes(self):
        return self.__sRes

    def setGenre(self, genre):
        self.__sGenre = genre

    def getGenre(self):
        return self.__sGenre

    def getSeason(self):
        return self.__Season

    def getEpisode(self):
        return self.__Episode

    def setTotalTime(self, data):
        self.__TotalTime = data

    def getTotalTime(self):
        return self.__TotalTime

    def setResumeTime(self, data):
        self.__ResumeTime = data

    def getResumeTime(self):
        return self.__ResumeTime

    def setMeta(self, sMeta):
        self.__sMeta = int(sMeta)

    def getMeta(self):
        return self.__sMeta

    def setMediaUrl(self, sMediaUrl):
        self.__sMediaUrl = sMediaUrl

    def getMediaUrl(self):
        return self.__sMediaUrl

    def setSiteUrl(self, sSiteUrl):
        self.__sSiteUrl = sSiteUrl

    def getSiteUrl(self):
        return self.__sSiteUrl

    def setSiteName(self, sSiteName):
        self.__sSiteName = sSiteName

    def getSiteName(self):
        return self.__sSiteName

    def setFileName(self, sFileName):
        self.__sFileName = cUtil().titleWatched(sFileName)

    def getFileName(self):
        return self.__sFileName

    def setFunction(self, sFunctionName):
        self.__sFunctionName = sFunctionName

    def getFunction(self):
        return self.__sFunctionName

    def TraiteTitre(self, sTitle):
        bMatrix = isMatrix()

        try:
            sTitle = sTitle.replace('Season', 'season').replace('Saison', 'season')
            sTitle = sTitle.replace(' - season', 'season').replace(' – season', ' season')\
                           .replace(' — season', ' season')
            sTitle = sTitle.replace("مدبلج بالعربية","مدبلج").replace("مدبلج بالعربي","[COLOR yellow]مدبلج[/COLOR]").replace("مدبلج عربي","[COLOR yellow]مدبلج[/COLOR]").replace("مدبلجة","[COLOR yellow]مدبلجة[/COLOR]").replace("مدبلجه","[COLOR yellow]مدبلجة[/COLOR]").replace("مدبلج بالمصري","[COLOR yellow]مدبلج بالمصري[/COLOR]").replace("مدبلج مصري","[COLOR yellow]مدبلج بالمصري[/COLOR]").replace("مدبلج للعربية","مدبلج").replace("مدبلج","[COLOR yellow]مدبلج[/COLOR]")

            if not bMatrix:
                sTitle = sTitle.decode('utf-8')
        except:
            pass

        sTitle = re.sub(' +', ' ', sTitle)
        sTitle = re.sub('\.+', '.', sTitle)

        sTitle = sTitle.replace('()', '').replace('[]', '').replace('- -', '-')

        sTitle = re.sub('[- –_\.\[]+$', '', sTitle)
        sTitle = re.sub('^[- –_\.]+', '', sTitle)

        string = re.search('[^\w ]([0-9]{4})[^\w ]', sTitle)
        if string:
            sTitle = sTitle.replace(string.group(0), '')
            self.__Year = str(string.group(1))
            self.addItemValues('year', self.__Year)

        string = re.search('([\d]{2}[\/|-]\d{2}[\/|-]\d{4})', sTitle)
        if string:
            sTitle = sTitle.replace(string.group(0), '')
            self.__Date = str(string.group(0))
            sTitle = '%s (%s) ' % (sTitle, self.__Date)

        # sTitle = re.sub('([\(|\[](?!\/*COLOR)[^\)\(\]\[]+?[\]|\)])', '[COLOR ' + self.sDecoColor + ']\\1[/COLOR]', sTitle)

        sa = ep = ''
        
        if self.__sCat in (2, 3, 4, 8, 9):
            m = re.search('(|S|season)(\s?|\.)(\d+)(\s?|\.)(E|Ep|x|\wpisode)(\s?|\.)(\d+)', sTitle, re.UNICODE)
            if m:
                sa = m.group(3)
                ep = m.group(7)
                if ep=='264' or ep=='265':
                    sa = ep = ''
                else:
                    sTitle = sTitle.replace(m.group(0), '')
                    
            else:
                m = re.search('(^|\s|\.)(E|Ep|\wpisode)(\s?|\.)(\d+)', sTitle, re.UNICODE)
                if m:
                    sTitle = sTitle.replace(m.group(0), '')
                    ep = m.group(4)
                else:
                    m = re.search('( S|season)(\s?|\.)(\d+)', sTitle, re.UNICODE)
                    if m:
                        sTitle = sTitle.replace(m.group(0), '')
                        sa = m.group(3)
    
            if sa or ep:
                sTitle = sTitle.replace('()', '').replace('[]', '').replace('- -', '-')
                sTitle = re.sub('[- –_\.\[]+$', '', sTitle)
    
            if sa:
                self.__Season = sa
                self.addItemValues('Season', self.__Season)
            if ep:
                self.__Episode = ep
                self.addItemValues('Episode', self.__Episode)
                if not self.__Season:
                    self.__Season = '1'

        if not bMatrix:
            try:
                sTitle = sTitle.encode('utf-8')
            except:
                pass

        sTitle2 = ''
        if self.__Season:
            sTitle2 = sTitle2 + 'S%02d' % int(self.__Season)
        if self.__Episode:
            sTitle2 = sTitle2 + 'E%02d' % int(self.__Episode)

        charMap = {
                    "\u0621": "'", "\u0622": "|", "\u0623": ">", "\u0624": "&",
                    "\u0625": "<", "\u0626": "}", "\u0627": "A", "\u0628": "b",
                    "\u0629": "p", "\u062A": "t", "\u062B": "v", "\u062C": "j",
                    "\u062D": "H", "\u062E": "x", "\u062F": "d", "\u0630": "*",
                    "\u0631": "r", "\u0632": "z", "\u0633": "s", "\u0634": "$",
                    "\u0635": "S", "\u0636": "D", "\u0637": "T", "\u0638": "Z",
                    "\u0639": "E", "\u063A": "g", "\u0640": "_", "\u0641": "f",
                    "\u0642": "q", "\u0643": "k", "\u0644": "l", "\u0645": "m",
                    "\u0646": "n", "\u0647": "h", "\u0648": "w", "\u0649": "Y",
                    "\u064A": "y", "\u064B": "F", "\u064C": "N", "\u064D": "K",
                    "\u064E": "a", "\u064F": "u", "\u0650": "i", "\u0651": "~",
                    "\u0652": "o", "\u0670": "`", "\u0671": "{", "\u067E": "P",
                    "\u0686": "J", "\u06A4": "V", "\u06AF": "G"
                    }
        sTitle4 = ''.join(charMap.get(char, char) for char in sTitle)

        self.__sTitleWatched = cUtil().titleWatched(sTitle4).replace(' ', '')
        if sTitle2:
            self.addItemValues('tvshowtitle', cUtil().getSerieTitre(sTitle))
            self.__sTitleWatched += '_' + sTitle2
        self.addItemValues('originaltitle', self.__sTitleWatched)

        if sTitle2:
            sTitle2 = '[COLOR %s]%s[/COLOR] ' % (self.sDecoColor, sTitle2)

        sTitle2 = sTitle2 + sTitle

        if self.__Year:
            sTitle2 = '%s [COLOR %s](%s)[/COLOR]' % (sTitle2, self.sDecoColor, self.__Year)

        return sTitle2

    def setRawTitle(self, sTitle):
        self.__sTitle = sTitle
        
    def setTitle(self, sTitle):
        self.__sCleanTitle = re.sub('\[.*\]|\(.*\)', '', sTitle)
        if not self.__sCleanTitle:
            self.__sCleanTitle = re.sub('\[.+?\]|\(.+?\)', '', sTitle)
            if not self.__sCleanTitle:
                self.__sCleanTitle = sTitle.replace('[', '').replace(']', '').replace('(', '').replace(')', '')

        if isMatrix():
            try:
                sTitle = str(sTitle.encode('latin-1'), 'utf-8')
            except:
                pass
        else:
            try:
                sTitle = str(sTitle.strip().decode('utf-8'))
            except:
                pass

        if not sTitle.startswith('[COLOR'):
            self.__sTitle = self.TraiteTitre(sTitle)
        else:
            self.__sTitle = sTitle

    def getTitle(self):
        return self.__sTitle

    def getCleanTitle(self):
        return self.__sCleanTitle

    def getTitleWatched(self):
        return self.__sTitleWatched

    def setDescription(self, sDescription):
        if isMatrix():
            try:
                if 'Ã' in sDescription or '\\xc' in sDescription:
                    self.__sDescription = str(sDescription.encode('latin-1'), 'utf-8')
                else:
                    self.__sDescription = sDescription
            except:
                self.__sDescription = sDescription
        else:
            self.__sDescription = sDescription

    def getDescription(self):
        return self.__sDescription

    def setThumbnail(self, sThumbnail):
        self.__sThumbnail = sThumbnail

    def getThumbnail(self):
        return self.__sThumbnail

    def setPoster(self, sPoster):
        self.__sPoster = sPoster

    def getPoster(self):
        return self.__sPoster

    def setFanart(self, sFanart):
        if sFanart != '':
            self.__sFanart = sFanart

    def setMovieFanart(self):
        self.__sFanart = self.__sFanart

    def setTvFanart(self):
        self.__sFanart = self.__sFanart

    def setDirectTvFanart(self):
        self.__sFanart = self.__sFanart

    def setDirFanart(self, sIcon):
        self.__sFanart = self.__sFanart

    def getFanart(self):
        return self.__sFanart

    def setIcon(self, sIcon):
        if not sIcon:
            self.__sIcon = ''
            return
        try:
            self.__sIcon = unicode(sIcon, 'utf-8')
        except:
            self.__sIcon = sIcon
        self.__sIcon = self.__sIcon.encode('utf-8')
        self.__sIcon = QuoteSafe(self.__sIcon)

    def getIcon(self):
        folder = 'special://home/addons/plugin.video.matrixflix/resources/art'
        path = '/'.join([folder, self.__sIcon])
        return path

    def addItemValues(self, sItemKey, mItemValue):
        self.__aItemValues[sItemKey] = mItemValue

    def getItemValue(self, sItemKey):
        if sItemKey not in self.__aItemValues:
            return
        return self.__aItemValues[sItemKey]

    def getWatched(self):
        if not self.getTitleWatched():
            return 0

        meta = {'titleWatched': self.getTitleWatched(),
                'site': self.getSiteUrl(),
                'cat': self.getCat()
                }

        with cDb() as db:
            data = db.get_watched(meta)
        return data

    def getInfoLabel(self):
        meta = {'title': xbmc.getInfoLabel('ListItem.title'),
                'year': xbmc.getInfoLabel('ListItem.year'),
                'genre': xbmc.getInfoLabel('ListItem.genre'),
                'director': xbmc.getInfoLabel('ListItem.director'),
                'country': xbmc.getInfoLabel('ListItem.country'),
                'rating': xbmc.getInfoLabel('ListItem.rating'),
                'votes': xbmc.getInfoLabel('ListItem.votes'),
                'mpaa': xbmc.getInfoLabel('ListItem.mpaa'),
                'duration': xbmc.getInfoLabel('ListItem.duration'),
                'trailer': xbmc.getInfoLabel('ListItem.trailer'),
                'writer': xbmc.getInfoLabel('ListItem.writer'),
                'studio': xbmc.getInfoLabel('ListItem.studio'),
                'tagline': xbmc.getInfoLabel('ListItem.tagline'),
                'plotoutline': xbmc.getInfoLabel('ListItem.plotoutline'),
                'plot': xbmc.getInfoLabel('ListItem.plot'),
                'poster_path': xbmc.getInfoLabel('ListItem.Art(thumb)'),
                'backdrop_path': xbmc.getInfoLabel('ListItem.Art(fanart)'),
                'imdbnumber': xbmc.getInfoLabel('ListItem.IMDBNumber'),
                # 'season': xbmc.getInfoLabel('ListItem.season'),
                # 'episode': xbmc.getInfoLabel('ListItem.episode'),
                'tvshowtitle': xbmc.getInfoLabel('ListItem.tvshowtitle')
                }

        if 'title' in meta and meta['title']:
            meta['title'] = self.getTitle()

        if 'backdrop_path' in meta and meta['backdrop_path']:
            url = meta.pop('backdrop_path')
            self.addItemProperties('fanart_image', url)
            if not self.__sFanart or self.__sRootArt in self.__sFanart:
                self.__sFanart = url

        if 'trailer' in meta and meta['trailer']:
            self.__sTrailer = meta['trailer']

        if 'poster_path' in meta and meta['poster_path']:
            url = meta.pop('poster_path')
            if not self.__sThumbnail:
                self.__sThumbnail = url
            if not self.__sPoster:
                self.__sPoster = url

        for key, value in meta.items():
            if value:
                self.addItemValues(key, value)

        return

    def getMetadonne(self):
        metaType = self.getMeta()
        if metaType == 0:
            self.addItemProperties('fanart_image', '')
            return

        from resources.lib.tmdb import cTMDb
        TMDb = cTMDb()

        sTitle = self.__sFileName
        sTitle = sTitle.replace('version longue', '')

        if metaType == 3:
            sTitle = sTitle.replace('integrales', '')
            sTitle = sTitle.replace('integrale', '')
            sTitle = sTitle.replace('2 films', '')
            sTitle = sTitle.replace('6 films', '')
            sTitle = sTitle.replace('7 films', '')
            sTitle = sTitle.replace('trilogie', '')
            sTitle = sTitle.replace('trilogy', '')
            sTitle = sTitle.replace('quadrilogie', '')
            sTitle = sTitle.replace('pentalogie', '')
            sTitle = sTitle.replace('octalogie', '')
            sTitle = sTitle.replace('hexalogie', '')
            sTitle = sTitle.replace('tetralogie', '')
            sTitle = sTitle.strip()
            if sTitle.endswith(' les'):
                sTitle = sTitle[:-4]
            elif sTitle.endswith(' la'):
                sTitle = sTitle[:-3]
            elif sTitle.endswith(' l'):
                sTitle = sTitle[:-2]
            sTitle = sTitle.strip()

        if metaType in (2, 4, 5, 6):
            tvshowtitle = self.getItemValue('tvshowtitle')
            if tvshowtitle:
                sTitle = tvshowtitle

        sType = str(metaType).replace('1', 'movie').replace('2', 'tvshow').replace('3', 'collection')\
                             .replace('4', 'anime').replace('5', 'season').replace('6', 'episode')\
                             .replace('7', 'person').replace('8', 'network')

        meta = {}
        try:
            if sType:
                args = (sType, sTitle)
                kwargs = {}
                if self.__ImdbId:
                    kwargs['imdb_id'] = self.__ImdbId
                if self.__TmdbId:
                    kwargs['tmdb_id'] = self.__TmdbId
                if self.__Year:
                    kwargs['year'] = self.__Year
                if self.__Season:
                    kwargs['season'] = self.__Season
                if self.__Episode:
                    kwargs['episode'] = self.__Episode

                meta = TMDb.get_meta(*args, **kwargs)
                if not meta:
                    return
            else:
                return
        except:
            return

        if 'media_type' in meta:
            meta.pop('media_type')

        if 'imdb_id' in meta:
            imdb_id = meta.pop('imdb_id')
            if imdb_id:
                self.__ImdbId = imdb_id

        if 'tmdb_id' in meta:
            tmdb_id = meta.pop('tmdb_id')
            if tmdb_id:
                self.__TmdbId = tmdb_id

        if 'tvdb_id' in meta:
            meta.pop('tvdb_id')

        # Temporary fix to avoid showing wrong images of Arabic Series/Movies
        if bool(re.search(r"[\u0600-\u06FF]", self.__sTitle)) is False:
            if 'backdrop_path' in meta:
                url = meta.pop('backdrop_path')
                if url:
                    self.addItemProperties('fanart_image', url)
                    self.__sFanart = url
                else:
                    self.addItemProperties('fanart_image', '')

            if 'poster_path' in meta:
                url = meta.pop('poster_path')
                if url:
                    self.__sThumbnail = url
                    self.__sPoster = url

        if 'poster_thumb' in meta:
            url = meta.pop('poster_thumb')
            if url:
                self.__sThumbnail = url
                # self.__sPoster = url

        if 'trailer' in meta and meta['trailer']:
            self.__sTrailer = meta['trailer']

        if 'guest_stars' in meta:
            meta.pop('guest_stars')

        if 'nbseasons' in meta:
            meta['season'] = meta.pop('nbseasons')

        if 'vote' in meta:
            meta.pop('vote')
        if 'runtime' in meta:
            meta.pop('runtime')
        if 'crew' in meta:
            meta.pop('crew')
        if 'overview' in meta:
            meta.pop('overview')
        if 'vote_average' in meta:
            meta.pop('vote_average')
        if 'vote_count' in meta:
            meta.pop('vote_count')
        if 'backdrop_url' in meta:
            meta.pop('backdrop_url')

        for key, value in meta.items():
            self.addItemValues(key, value)

        return

    def getItemValues(self):
        self.addItemValues('title', self.getTitle())

        # - Video Values:
        # - genre : string (Comedy)
        # - year : integer (2009)
        # - episode : integer (4)
        # - season : integer (1)
        # - top250 : integer (192)
        # - tracknumber : integer (3)
        # - rating : float (6.4) - range is 0..10
        # - watched : depreciated - use playcount instead
        # - playcount : integer (2) - number of times this item has been played
        # - overlay : integer (2) - range is 0..8. See GUIListItem.h for values
        # - cast : list (Michal C. Hall)
        # - castandrole : list (Michael C. Hall|Dexter)
        # - director : string (Dagur Kari)
        # - mpaa : string (PG-13)
        # - plot : string (Long Description)
        # - plotoutline : string (Short Description)
        # - title : string (Big Fan)
        # - originaltitle : string (Big Fan)
        # - sorttitle : string (Big Fan)
        # - duration : string (3:18)
        # - studio : string (Warner Bros.)
        # - tagline : string (An awesome movie) - short description of movie
        # - writer : string (Robert D. Siegel)
        # - tvshowtitle : string (Heroes)
        # - premiered : string (2005-03-04)
        # - status : string (Continuing) - status of a TVshow
        # - code : string (tt0110293) - IMDb code
        # - aired : string (2008-12-07)
        # - credits : string (Andy Kaufman) - writing credits
        # - lastplayed : string (Y-m-d h:m:s = 2009-04-05 23:16:04)
        # - album : string (The Joshua Tree)
        # - artist : list (['U2'])
        # - votes : string (12345 votes)
        # - trailer : string (/home/user/trailer.avi)
        # - dateadded : string (Y-m-d h:m:s = 2009-04-05 23:16:04)

        if self.getMetaAddon() == 'true':
            self.getMetadonne()
        if self.getTmdbId():
            self.addItemProperties('TmdbId', str(self.getTmdbId()))
            self.addItemValues('DBID', str(self.getTmdbId()))   # utiliser par certains addons tel que Trakt pour le scrobbling
        if self.getImdbId():
            self.addItemProperties('ImdbId', str(self.getImdbId()))
        if not self.getItemValue('plot') and self.getDescription():
            self.addItemValues('plot', self.getDescription())
        if not self.getItemValue('year') and self.getYear():
            self.addItemValues('year', self.getYear())
        if not self.getItemValue('genre') and self.getGenre():
            self.addItemValues('genre', self.getGenre())
        # if not self.getItemValue('cover_url') and self.getThumbnail():
            # self.addItemValues('cover_url', self.getThumbnail())
        # if not self.getItemValue('backdrop_path') and self.getPoster():
            # self.addItemValues('backdrop_path', self.getPoster())
        if not self.getItemValue('trailer'):
            if self.getTrailer():
                self.addItemValues('trailer', self.getTrailer())
            else:
                self.addItemValues('trailer', 'plugin')

        sCat = self.getCat()
        try:
            if sCat and sCat in (1, 2, 3, 4, 5, 8, 9):
                if self.getWatched():
                    self.addItemValues('playcount', 1)
        except:
            sCat = None

        self.addItemProperties('siteUrl', self.getSiteUrl())
        self.addItemProperties('sCleanTitle', self.getFileName())
        self.addItemProperties('sId', self.getSiteName())
        self.addItemProperties('sFav', self.getFunction())
        self.addItemProperties('sMeta', str(self.getMeta()))
        if isNexus():
            self.addItemValues('resumetime', self.getResumeTime())
            self.addItemValues('totaltime', self.getTotalTime())
        else:
            self.addItemProperties('resumetime', self.getResumeTime())
            self.addItemProperties('totaltime', self.getTotalTime())

        if sCat:
            self.addItemProperties('sCat', sCat)
            mediatypes = {1: 'movie', 2: 'tvshow', 3: 'tvshow', 4: 'season', 5: 'video',
                          6: 'video', 7: 'season', 8: 'episode', 9: 'tvshow'}
            if sCat in mediatypes.keys():
                mediatype = mediatypes.get(sCat)
                self.addItemValues('mediatype', mediatype)

        if self.getSeason():
            self.addItemValues('season', int(self.getSeason()))

        if self.getEpisode():
            self.addItemValues('episode', int(self.getEpisode()))

        return self.__aItemValues

    def addItemProperties(self, sPropertyKey, mPropertyValue):
        if sPropertyKey not in self.__aProperties:
            self.__aProperties[sPropertyKey] = mPropertyValue

    def getItemProperties(self):
        return self.__aProperties

    def addContextItem(self, oContextElement):
        self.__aContextElements.append(oContextElement)

    def getContextItems(self):
        return self.__aContextElements
