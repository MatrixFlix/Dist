﻿# -*- coding: utf-8 -*-

import re
import base64
import json
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib import random_ua

UA = random_ua.get_ua()

SITE_IDENTIFIER = 'witanime'
SITE_NAME = 'WitAnime'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
if addon().getSetting('Use_alternative') == "true":
    URL_MAIN = siteManager().getUrlMain2(SITE_IDENTIFIER)

ANIM_MOVIES = (f'{URL_MAIN}anime-type/movie/', 'showMovies')
ANIM_NEWS = (f'{URL_MAIN}episode/' , 'showSeries')
ANIM_LIST = (True, 'showAnimesList')

URL_SEARCH = (f'{URL_MAIN}?search_param=animes&s=', 'showMovies')
URL_SEARCH_ANIMS = (f'{URL_MAIN}?search_param=animes&s=', 'showSeries')

FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30118), 'search.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', 'anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انمي', 'anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}anime-status/%d9%8a%d8%b9%d8%b1%d8%b6-%d8%a7%d9%84%d8%a7%d9%86/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'يعرض الان', 'anime.png', oOutputParameterHandler) 

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}anime-season/صيف-2024/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أنميات الموسم', 'anime.png', oOutputParameterHandler) 

    oOutputParameterHandler.addParameter('siteUrl', ANIM_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_LIST[1], 'قائمة الأنمي', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAnimesList():
    oGui = cGui()

    liste = []
    liste.append( ['#', f'{URL_MAIN}/en-anime-letter/228'] )
    liste.append( ['أ', f'{URL_MAIN}/ar-anime-letter/أ'] )
    liste.append( ['ب', f'{URL_MAIN}/ar-anime-letter/ب'] )
    liste.append( ['ت', f'{URL_MAIN}/ar-anime-letter/ت'] )
    liste.append( ['ث', f'{URL_MAIN}/ar-anime-letter/ث'] )
    liste.append( ['ج', f'{URL_MAIN}/ar-anime-letter/ج'] )
    liste.append( ['د', f'{URL_MAIN}/ar-anime-letter/د'] )
    liste.append( ['ر', f'{URL_MAIN}/ar-anime-letter/ر'] )
    liste.append( ['ز', f'{URL_MAIN}/ar-anime-letter/ز'] )
    liste.append( ['س', f'{URL_MAIN}/ar-anime-letter/س'] )
    liste.append( ['ش', f'{URL_MAIN}/ar-anime-letter/ش'] )
    liste.append( ['ط', f'{URL_MAIN}/ar-anime-letter/ط'] )
    liste.append( ['غ', f'{URL_MAIN}/ar-anime-letter/غ'] )
    liste.append( ['ف', f'{URL_MAIN}/ar-anime-letter/ف'] )
    liste.append( ['ك', f'{URL_MAIN}/ar-anime-letter/ك'] )
    liste.append( ['ل', f'{URL_MAIN}/ar-anime-letter/ل'] )
    liste.append( ['م', f'{URL_MAIN}/ar-anime-letter/م'] )
    liste.append( ['ن', f'{URL_MAIN}/ar-anime-letter/ن'] )
    liste.append( ['هـ', f'{URL_MAIN}/ar-anime-letter/ه'] )
    liste.append( ['و', f'{URL_MAIN}/ar-anime-letter/و'] )
    liste.append( ['ي', f'{URL_MAIN}/ar-anime-letter/ي'] )
    liste.append( ['A', f'{URL_MAIN}/en-anime-letter/A'] )
    liste.append( ['B', f'{URL_MAIN}/en-anime-letter/B'] )
    liste.append( ['C', f'{URL_MAIN}/en-anime-letter/C'] )
    liste.append( ['D', f'{URL_MAIN}/en-anime-letter/D'] )
    liste.append( ['E', f'{URL_MAIN}/en-anime-letter/E'] )
    liste.append( ['F', f'{URL_MAIN}/en-anime-letter/F'] )
    liste.append( ['G', f'{URL_MAIN}/en-anime-letter/G'] )
    liste.append( ['H', f'{URL_MAIN}/en-anime-letter/H'] )
    liste.append( ['I', f'{URL_MAIN}/en-anime-letter/I'] )
    liste.append( ['J', f'{URL_MAIN}/en-anime-letter/J'] )
    liste.append( ['K', f'{URL_MAIN}/en-anime-letter/K'] )
    liste.append( ['L', f'{URL_MAIN}/en-anime-letter/L'] )
    liste.append( ['M', f'{URL_MAIN}/en-anime-letter/M'] )
    liste.append( ['N', f'{URL_MAIN}/en-anime-letter/N'] )
    liste.append( ['O', f'{URL_MAIN}/en-anime-letter/O'] )
    liste.append( ['P', f'{URL_MAIN}/en-anime-letter/P'] )
    liste.append( ['Q', f'{URL_MAIN}/en-anime-letter/Q'] )
    liste.append( ['R', f'{URL_MAIN}/en-anime-letter/R'] )
    liste.append( ['S', f'{URL_MAIN}/en-anime-letter/S'] )
    liste.append( ['T', f'{URL_MAIN}/en-anime-letter/T'] )
    liste.append( ['U', f'{URL_MAIN}/en-anime-letter/U'] )
    liste.append( ['V', f'{URL_MAIN}/en-anime-letter/V'] )
    liste.append( ['W', f'{URL_MAIN}/en-anime-letter/W'] )
    liste.append( ['X', f'{URL_MAIN}/en-anime-letter/X'] )
    liste.append( ['Y', f'{URL_MAIN}/en-anime-letter/Y'] )
    liste.append( ['Z', f'{URL_MAIN}/en-anime-letter/Z'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Letter [COLOR coral]' + sTitle + '[/COLOR]', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}?search_param=animes&s={sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<img class="img-responsive" src="([^<]+)" alt="([^<]+)" />.+?data-content="([^<]+)".+?<h3><a href="([^<]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)		
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = cUtil().CleanMovieName(aEntry[1])
            siteUrl = aEntry[3]
            sThumb = re.sub(r'-\d+x\d{0,3}','', aEntry[0])  
            sDesc = aEntry[2]
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addTV(SITE_IDENTIFIER, 'ShowEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
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

    sPattern = '<img class="img-responsive" src="([^"]+)" alt="([^"]+)".+?data-content="([^"]+)".+?redirectTo.+?["\']([^"\']+)["\']'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1]
            siteUrl = base64.b64decode(aEntry[3]).decode('utf8',errors='ignore')
            sThumb = re.sub(r'-\d+x\d{0,3}','', aEntry[0])  
            sDesc = aEntry[2]
            sYear = ''
            sTitle = sTitle.split('الحلقة')[0].split('الموسم')[0]
            sTitle = sTitle.replace("Season ","S")

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addTV(SITE_IDENTIFIER, 'ShowEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def ShowEps():
    oGui = cGui()   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request() 

    oParser = cParser()
    sStart = '<div class="episodes-list-content">'
    sEnd = '<div class="space"></div>'
    sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<h3><a href=.+?onclick="(.+?)">([^<]+)</a></h3>.+?src="([^"]+)'
    aResult = oParser.parse(sHtmlContent1, sPattern)   
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sEp = aEntry[1].replace("الحلقة ","").replace("الفلم ","").replace("الخاصة ","")
            sTitle = f'{sMovieTitle} E{sEp}'
            EnCodedUrl = aEntry[0].replace("openEpisode('","").replace("')","")
            siteUrl = base64.b64decode(EnCodedUrl).decode('utf8',errors='ignore')
            sDesc = ''
            sYear = ''
            sThumb = re.sub(r'-\d+x\d{0,3}','', aEntry[2])  
 
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 
    else:
        sPattern = "processedEpisodeData = '([^']+)'"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:        
            sEps = decode(aResult[1][0])
            oOutputParameterHandler = cOutputParameterHandler()
            for item in sEps:
                sEp = item["number"]
                sTitle = f'{sMovieTitle} E{sEp}'
                siteUrl = item["url"]
                sDesc = ''
                sYear = ''
                sThumb = re.sub(r'-\d+x\d{0,3}','', item["screenshot"])  
    
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<link rel="next" href="([^<]+)" />'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:        
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = "sU\s*=\s*([^;]*)"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:        
        vds = json.loads(aResult[1][0])
        for item in vds:

                url = base64.b64decode(item).decode('utf8',errors='ignore')
                if url.startswith('//'):
                    url = 'http:' + url
                if 'yona' in url:
                    url = url + '&apiKey=9b2704f6-6b6f-4a48-b3f3-cd9cd4dbe494'
                    oRequestHandler = cRequestHandler(url)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
                    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
                    sData = oRequestHandler.request()
                    
                    sPattern = 'go_to_player(.+?)".+?<p>([^<]+)'
                    aResult = oParser.parse(sData, sPattern)
                    if aResult[0]:
                       for aEntry in reversed(aResult[1]):  
                            if 'mega' in aEntry[0]:
                               continue      
                            url = aEntry[0].replace(')','').replace('(','').replace("'","").replace('"','')
                            sQual = aEntry[1].replace('-','').replace(' ','')

                            try:
                                sHosterUrl = base64.b64decode(f'{url}==').decode('utf8',errors='ignore')
                            except:
                                sHosterUrl = url
                            if 'soraplay' in sHosterUrl:
                                sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'

                            oHoster = cHosterGui().checkHoster(sHosterUrl)
                            if oHoster:
                                sDisplayTitle = f'{sMovieTitle} [COLOR coral] Yonaplay ({sQual})[/COLOR]'
                                oHoster.setDisplayName(sDisplayTitle)
                                oHoster.setFileName(sMovieTitle)
                                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)                 

                else:
                    sHosterUrl = url
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        sDisplayTitle = f'{sMovieTitle}'
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = "_d\s*=\s*([^;]*)"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:        
        vds = json.loads(aResult[1][0])
        for item in vds:

                url = base64.b64decode(item).decode('utf8',errors='ignore')
                if url.startswith('//'):
                    url = 'http:' + url           

                sHosterUrl = url
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    sDisplayTitle = f'{sMovieTitle}'
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

	       
    oGui.setEndOfDirectory()

def decode(data: str):
        parts = data.split(".")
        if len(parts) != 2:
            raise VSlog("Bad data format")

        try:
            decoded_part1 = base64.b64decode(parts[0])
            decoded_part2 = base64.b64decode(parts[1])
        except Exception as err:
            return None, err

        decoded_data = bytearray(len(decoded_part1))
        for i in range(len(decoded_part1)):
            decoded_data[i] = decoded_part1[i] ^ decoded_part2[i % len(decoded_part2)]

        clean_data = decoded_data.decode('utf-8').replace(r'\"', '"')

        try:
            decoded_json = json.loads(clean_data)
        except json.JSONDecodeError as err:
            return None, err

        return decoded_json