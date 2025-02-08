﻿# -*- coding: utf-8 -*-

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import VSlog, siteManager, addon

SITE_IDENTIFIER = 'linkbox'
SITE_NAME = 'Telebox [COLOR orange]- Linkbox -[/COLOR]'
SITE_DESC = 'A Box Linking The World'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

URL_SEARCH = ('https://www.zain3.com/api/search?kw=', 'GetSearch')
FUNCTION_SEARCH = 'GetSearch'

def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30330), 'search.png', oOutputParameterHandler)

    sList = [
            ('2024 اشهر واقوى المسلسلات والافلام','nLw3cuO','sites/linkbox.png'),
            ('Anime Box','app01e2f1adf1aca0a1a1a4a7a2a0adf2aca0a1a1a4a7a2a0','sites/linkbox.png'),
            ('HTM Animes','app01e2f1adf2acaeafa1a3a1a0a0adf1acaeafa1a3a1a0a0','sites/linkbox.png'),
            ('Cinema Baghdad','UiLE7sU','sites/linkbox.png'),
            ('Cinema-Club (أفلام)','app01e2f1adf1aca4a3a2a1a7aea4adf2aca4a3a2a1a7aea4','sites/cimaclub.png'),
            ('Cinema-Club (أفلام و مسلسلات الأنمي)','app01e2f1adf1aca4a3a5aea3aea0adf2aca4a3a5aea3aea0','sites/cimaclub.png'),
            ('Cinema Crown','app01e2f1adf1aca7a4a5a3a1a3aeadf2aca7a4a5a3a1a3ae','sites/linkbox.png'),
            ('Egybest 1','xgLMOew','sites/egybest.png'),
            ('Egybest 2','app01e2f1adf2aca7a3a6a0a1a1a5adf1aca7a3a6a0a1a1a5','sites/egybest.png'),
            ('Marvel Morocco','SD9p5bO','sites/linkbox.png'),
            ('Movies Plus','app01e2f1adf1aca0a2a3a1a0a6adf2aca0a2a3a1a0a6','sites/linkbox.png'),
            ('Netflix','_ig_app01e2f1adf0f2acf0e6a5fda0aea6a6a6f3afe0_2674587_0ddd','sites/netflix.png'),
            ('NewQ','_ig_app01e2f1adf0f2acf0e6a5fafae5a6a6f4f2aff4_4606358_e7ba','sites/linkbox.png'),
            ('OneCima TV','app01e2f1adf1aca7a5a2a5a5a4a2adf2aca7a5a2a5a5a4a2','sites/linkbox.png'),
            ('Star Cinema','app01e2f1adf1aca1afaea6a7adf2aca1afaea6a7','sites/linkbox.png'),
            ('Showtime Movies','app01e2f1adf1aca2a4a7afa5afa7adf2aca2a4a7afa5afa7','sites/linkbox.png'),
            ('English Films | افلام اجنبي','_ig_app01e2f1adf0f2acf0e6a5f1e2a6a6a6a5a6efe3_752951_b7af','sites/linkbox.png'),
            ('(رياضة) ThrowLob','NZKr9gl','sites/linkbox.png'),
            ('The Movie Muse','ZmM9DaP','sites/linkbox.png'),
            ('Yalla Anime','app01e2f1adf2aca4afa3a5a1a5aeadf1aca4afa3a5a1a5ae','sites/linkbox.png'),
            ('مجتمع الأفلام والمسلسلات | Documentary Films','app01e2f1adf2acaea7a5a2a3a5a4adf1acaea7a5a2a3a5a4','sites/linkbox.png'),
            ('فرجني | Faragny','_ig_app01e2f1adf0f2acf0e6a5fcaff5a6a6a6afa7fe_2609502_fdae','sites/linkbox.png'),
            ('افلام شوفها','app01e2f1adf2aca4afa5a5a6a2aeadf1aca4afa5a5a6a2ae','sites/linkbox.png'),
            ('موطن المفيز Movies المدبلج','app01e2f1adf2aca0aea6a2a5a3adf1aca0aea6a2a5a3','sites/linkbox.png'),
            ('سينما أونلاين','app01e2f1adf1aca5a2aea1a2a6a3adf2aca5a2aea1a2a6a3','sites/linkbox.png'),
            ('مسلسلات أجنبية أكشن إثارة','_ig_app01e2f1adf0f2acf0e6a5fbe6fda6a6a6eef4ff_6032611_496c','sites/linkbox.png'),
            ('أفلام مجان نت','app01e2f1adf2aca4a7a5a7a0aeafadf1aca4a7a5a7a0aeaf','sites/linkbox.png'),
            ('كيدراما (الأسيوية)','app01e2f1adf1aca4a3a6afa0a6adf2aca4a3a6afa0a6','sites/linkbox.png'),
            ('مسلسلات وأفلام أسيوية','app01e2f1adf2aca0a0a0afa0aeadf1aca0a0a0afa0ae','sites/linkbox.png'),
            ('سلاسل أفلام','_ig_app01e2f1adf0f2acf0e6a5fbefe1a6a6fca0fff2_728149_b0d7','sites/linkbox.png'),
            ('تسس موفيز','app01e2f1adf2aca5a2a6afafa7adf1aca5a2a6afafa7','sites/linkbox.png'),
            ('أنميات (انمي)','app01e2f1adf2acaeaea5a2aea4afadf1acaeaea5a2aea4af','sites/linkbox.png'),
            ('شانكس ساما (انمي)','app01e2f1adf2aca0aeaeafa2a1adf1aca0aeaeafa2a1','sites/linkbox.png'),
            ('تارو ساما (انمي)','app01e2f1adf2aca0a5a5a3a0adf1aca0a5a5a3a0','sites/linkbox.png'),
            ('(انمي) عالم الأنمي','app01e2f1adf2aca4aea5a4a6a1a3adf1aca4aea5a4a6a1a3','sites/linkbox.png'),
            ('لوفي ساما (انمي)','lUprnhl','sites/linkbox.png')]
    
    for sServer in sList:
            icon = sServer[2]
            if icon != '':
                icon = sServer[2]
            else:
                icon = 'host.png'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sServer[1])
            oGui.addDir(SITE_IDENTIFIER, 'showContent', sServer[0], icon, oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'https://www.zain3.com/api/search?kw={sSearchText}&pageSize=50&pageNo=1'
        GetSearch(sUrl)
        oGui.setEndOfDirectory()
        return

def showContent():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oInputParameterHandler = cInputParameterHandler()

    sUrl = oInputParameterHandler.getValue('siteUrl')
    spage = int(oInputParameterHandler.getValue('page'))   
    spid = oInputParameterHandler.getValue('spid')
 
    ListCount = 50
    shareToken = sUrl

    page = 1
    pid = spid

    page = spage if spage > 1 else 1

    sUrl = f'{URL_MAIN}api/file/share_out_list/?sortField=name&sortAsc=1&pageNo={str(page)}&pageSize={str(ListCount)}&shareToken={shareToken}&pid={str(pid)}&needTpInfo=1&scene=singleGroup&name=&platform=web&pf=web&lan=en'

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('connection', 'Keep-Alive')
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    sCount = 0
    data = sHtmlContent.get("data")
    if data and isinstance(data, dict):
        data = data.get("list", [])
    else:
        data = []

    if not data:
        oGui.addText(SITE_IDENTIFIER, '[COLOR orange]لم يتم العثور على نتائج ، ربما تم حظره بسبب شكوى انتهاك حقوق النشر[/COLOR]')

    else:
        oOutputParameterHandler.addParameter('spid', pid) 
        oOutputParameterHandler.addParameter('siteUrl',shareToken)
        oGui.addDir(SITE_IDENTIFIER, 'showGroupSearch', '[COLOR yellow] Search Files within Group [/COLOR]', 'search.png', oOutputParameterHandler) 

        for aEntry in data:

            sTitle = re.sub(r"[^\w\s]", "", clean_html_tags(aEntry.get('name', ''))).replace('mp4', '')
            sType = aEntry.get('type', '')
            pid = aEntry.get('id', '')
            spid = aEntry.get('pid', '')
            sThumb = 'host.png'
            link = aEntry.get('url', '')
            size = int(aEntry.get('size', 0) / 1024**2)
            sCount += 1

            oOutputParameterHandler.addParameter('spid', pid) 
            oOutputParameterHandler.addParameter('sTitle', sTitle)            
            oOutputParameterHandler.addParameter('sThumb', sThumb) 
            oOutputParameterHandler.addParameter('siteUrl',shareToken)
            
            if sType =='dir':
                oGui.addDir(SITE_IDENTIFIER, 'showContent', sTitle, sThumb, oOutputParameterHandler)
                
            if sCount + 1 > ListCount:
                page = page + 1
                oOutputParameterHandler.addParameter('page', page)
                oOutputParameterHandler.addParameter('siteUrl',shareToken)
                oOutputParameterHandler.addParameter('spid', spid) 
                oGui.addDir(SITE_IDENTIFIER, 'showContent', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

            if sType in ['video', 'audio']:
                icon = aEntry.get('cover', '').split('&x-image-process', 1)[0] if '&x-image-process' in aEntry.get('cover', '') else aEntry.get('cover', '')
                sHosterUrl = link.replace('<nil>', '')
                sDisplayTitle = f"{sTitle} [COLOR yellow]({size}MB)[/COLOR]"

                oHoster = cHosterGui().getHoster('direct_link')        
                if oHoster:
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, icon)              

    oGui.setEndOfDirectory()


def GetSearch(sSearch = ''):
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()  
    oInputParameterHandler = cInputParameterHandler() 

    ListCount = 50
    shareToken = sSearch

    spage = int(oInputParameterHandler.getValue('page'))  
    page = spage if spage > 1 else 1

    oRequestHandler = cRequestHandler(sSearch)
    oRequestHandler.addHeaderEntry('connection', 'Keep-Alive')
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    sCount = 0
    data = sHtmlContent.get("data")
    if data and isinstance(data, dict):
        data = data.get("list", [])
    else:
        data = []

    if not data:
        oGui.addText(SITE_IDENTIFIER, '[COLOR orange]لم يتم العثور على نتائج[/COLOR]')

    else:
        for aEntry in data:
            
            sCount += 1
            sTitle = re.sub(r"[^\w\s]", "", clean_html_tags(aEntry.get('name', ''))).replace('mp4', '')
            sThumb = 'host.png'
            siteUrl = aEntry.get('url', '').replace('/f/', '/s/')
            if '/s/' in siteUrl:
                shareToken, pid = (siteUrl.split('/s/')[1].split('?pid=') + ['0'])[:2]
            elif '?pid=' in siteUrl:
                pid = siteUrl.split('?pid=')[0] or '0'
            else:
                pid = aEntry.get('id', '0')

            if sCount > ListCount:
                page += 1

            oOutputParameterHandler.addParameter('page',page)
            oOutputParameterHandler.addParameter('spid', pid) 
            oOutputParameterHandler.addParameter('sTitle', sTitle)            
            oOutputParameterHandler.addParameter('sThumb', sThumb) 
            oOutputParameterHandler.addParameter('siteUrl',shareToken)

            oGui.addDir(SITE_IDENTIFIER, 'showContent', sTitle, sThumb, oOutputParameterHandler)            
 
    oGui.setEndOfDirectory()

def showGroupSearch(sSearchText = ''):
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()

    oOutputParameterHandler = cOutputParameterHandler()  
    oInputParameterHandler = cInputParameterHandler()

    sUrl = oInputParameterHandler.getValue('siteUrl')
    spage = int(oInputParameterHandler.getValue('page'))   
    spid = oInputParameterHandler.getValue('spid')

    ListCount = 50
    shareToken = sUrl

    pid = spid
    page = spage if spage > 1 else 1

    sUrl = f'{URL_MAIN}api/file/share_out_list/?sortField=name&sortAsc=1&pageNo={str(page)}&pageSize={str(ListCount)}&shareToken={shareToken}&pid={str(pid)}&needTpInfo=1&scene=singleGroup&name={sSearchText}&platform=web&pf=web&lan=en'

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('connection', 'Keep-Alive')
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    sCount = 0
    data = sHtmlContent.get("data")
    if data and isinstance(data, dict):
        data = data.get("list", [])
    else:
        data = []

    if not data:
        oGui.addText(SITE_IDENTIFIER, '[COLOR orange]لم يتم العثور على نتائج[/COLOR]')

    else:
        for aEntry in data:

            sCount += 1
            pid = aEntry.get('id', '')
            spid = 0
            sTitle = re.sub(r"[^\w\s]", "", clean_html_tags(aEntry.get('name', ''))).replace('mp4', '')
            sType = aEntry.get('type', '')
            sThumb = 'host.png'
            siteUrl = aEntry.get('url', '')
            sSize = int(aEntry.get('size', 0) / 1024**2)
            shareToken = shareToken

            oOutputParameterHandler.addParameter('spid', pid) 
            oOutputParameterHandler.addParameter('sTitle', sTitle)            
            oOutputParameterHandler.addParameter('sThumb', sThumb) 
            oOutputParameterHandler.addParameter('siteUrl', shareToken)
                
            if sCount + 1 > ListCount:
                page = page + 1
                oOutputParameterHandler.addParameter('page', page)
                oOutputParameterHandler.addParameter('siteUrl', shareToken)
                oOutputParameterHandler.addParameter('spid', spid) 
                oOutputParameterHandler.addParameter('sSearchText', sSearchText) 
                
                oGui.addDir(SITE_IDENTIFIER, 'showGroupSearchNext', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

            elif sType in ['video', 'audio']:
                sThumb = aEntry.get('cover', '').split('&x-image-process', 1)[0] if '&x-image-process' in aEntry.get('cover', '') else aEntry.get('cover', '')

                sHosterUrl = clean_html_tags(siteUrl)
                sDisplayTitle = f'{sTitle} [COLOR yellow]({str(sSize)}MB)[/COLOR]'
                oHoster = cHosterGui().getHoster('direct_link')        
                if oHoster:
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)         
 
    oGui.setEndOfDirectory()

def showGroupSearchNext(sSearchText = ''):
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()  
    oInputParameterHandler = cInputParameterHandler()

    sUrl = oInputParameterHandler.getValue('siteUrl')
    sSearchText = oInputParameterHandler.getValue('sSearchText')
    spage = int(oInputParameterHandler.getValue('page'))   
    spid = oInputParameterHandler.getValue('spid')

    ListCount = 50
    shareToken = sUrl

    page = spage if spage > 1 else 1

    sUrl = f'{URL_MAIN}api/file/share_out_list/?sortField=name&sortAsc=1&pageNo={str(page)}&pageSize={str(ListCount)}&shareToken={shareToken}&pid=0&needTpInfo=1&scene=singleGroup&name={sSearchText}&platform=web&pf=web&lan=en'

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('connection', 'Keep-Alive')
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    sCount = 0
    data = sHtmlContent.get("data")
    if data and isinstance(data, dict):
        data = data.get("list", [])
    else:
        data = []

    if not data:
        oGui.addText(SITE_IDENTIFIER, '[COLOR orange]لم يتم العثور على نتائج[/COLOR]')

    else:    
        for aEntry in data:

            sCount += 1
            sTitle = re.sub(r"[^\w\s]", "", clean_html_tags(aEntry.get('name', ''))).replace('mp4', '')
            sType = aEntry.get('type','')
            sThumb  = 'host.png'
            spid = 0       

            siteUrl  = aEntry.get('url','')
            sSize = int(aEntry.get('size', 0) / 1024**2)
            shareToken = shareToken

            if sCount + 1 > ListCount:
                page = page + 1
                oOutputParameterHandler.addParameter('page', page)
                oOutputParameterHandler.addParameter('siteUrl', shareToken)
                oOutputParameterHandler.addParameter('spid', spid) 
                oOutputParameterHandler.addParameter('sSearchText', sSearchText) 

                oGui.addDir(SITE_IDENTIFIER, 'showGroupSearchNext', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

            elif sType in ['video', 'audio']:
                sThumb = aEntry.get('cover', '').split('&x-image-process', 1)[0] if '&x-image-process' in aEntry.get('cover', '') else aEntry.get('cover', '')

                sHosterUrl = clean_html_tags(siteUrl)
                sDisplayTitle = f'{sTitle} [COLOR yellow]({str(sSize)}MB)[/COLOR]'

                oHoster = cHosterGui().getHoster('direct_link')        
                if oHoster:
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)          
 
    oGui.setEndOfDirectory()

def clean_html_tags(text):
    clean_text = re.sub(r'<.*?>', '', text)
    return clean_text