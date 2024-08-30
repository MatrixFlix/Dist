# -*- coding: utf-8 -*-

from resources.lib.home import cHome
from resources.lib.gui.gui import cGui
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import progress, VSlog, addon, window, siteManager
from resources.lib.search import cSearch

DEBUG = False

if DEBUG:

    import sys 
    sys.path.append('H:\Program Files\Kodi\system\Python\Lib\pysrc')

    try:
        import pysrc.pydevd as pydevd
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        try:
            import pydevd 
            pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
        except ImportError:
            sys.stderr.write("Error: " + "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")


class main:

    def __init__(self):
        self.parseUrl()

    def parseUrl(self):
        oPluginHandler = cPluginHandler()
        pluginPath = oPluginHandler.getPluginPath()
        if pluginPath == 'plugin://plugin.video.matrixflix/extrafanart/':
            return

        oInputParameterHandler = cInputParameterHandler()

        if oInputParameterHandler.exist('function'):
            sFunction = oInputParameterHandler.getValue('function')
        else:
            VSlog('call load methode')
            sFunction = "load"

        if sFunction == 'setSetting':
            if oInputParameterHandler.exist('id'):
                plugin_id = oInputParameterHandler.getValue('id')
            else:
                return

            if oInputParameterHandler.exist('value'):
                value = oInputParameterHandler.getValue('value')
            else:
                return

            setSetting(plugin_id, value)
            return

        if sFunction == 'setSettings':
            setSettings(oInputParameterHandler)
            return

        if sFunction == 'DoNothing':
            return

        if not oInputParameterHandler.exist('site'):
            plugins = __import__('resources.lib.home', fromlist=['home']).cHome()
            function = getattr(plugins, 'load')
            function()
            return

        if oInputParameterHandler.exist('site'):
            sSiteName = oInputParameterHandler.getValue('site')
            VSlog('load site ' + sSiteName + ' and call function ' + sFunction)

            if isHosterGui(sSiteName, sFunction):
                return

            if isGui(sSiteName, sFunction):
                return

            if isFav(sSiteName, sFunction):
                return
            
            if isWatched(sSiteName, sFunction):
                return

            if isViewing(sSiteName, sFunction):
                return

            if isLibrary(sSiteName, sFunction):
                return

            if isDl(sSiteName, sFunction):
                return

            if isHome(sSiteName, sFunction):
                return

            if isSearch(sSiteName, sFunction):
                return

            if isTrakt(sSiteName, sFunction):
                return

            if sSiteName == 'globalRun':
                __import__('resources.lib.runscript', fromlist=['runscript'])
                return

            if sSiteName == 'globalSources':
                oGui = cGui()
                aPlugins = oPluginHandler.getAvailablePlugins(force = (sFunction == 'globalSources'))
                
                sitesManager = siteManager()
                if len(aPlugins) == 0:
                    addons = addon()
                    addons.openSettings()
                    oGui.updateDirectory()
                else:
                    for aPlugin in aPlugins:
                        
                        sitename = aPlugin[0]
                        if not sitesManager.isActive(aPlugin[1]):
                            sitename = '[COLOR red][OFF] ' + sitename + '[/COLOR]'
                        oOutputParameterHandler = cOutputParameterHandler()
                        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
                        icon = 'sites/%s.png' % (aPlugin[1])
                        oGui.addDir(aPlugin[1], 'load', sitename, icon, oOutputParameterHandler)

                oGui.setEndOfDirectory()
                return

            if sSiteName == 'globalParametre':
                addons = addon()
                addons.openSettings()
                return

            try:
                plugins = __import__('resources.sites.%s' % sSiteName, fromlist=[sSiteName])
                function = getattr(plugins, sFunction)
                function()
            except Exception as e:
                progress().VSclose() 
                VSlog('could not load site: ' + sSiteName + ' error: ' + str(e))
                import traceback
                traceback.print_exc()
                return


def setSetting(plugin_id, value):
    addons = addon()
    setting = addons.getSetting(plugin_id)

    if setting != value:
        addons.setSetting(plugin_id, value)
        return True

    return False

def setSettings(oInputParameterHandler):
    addons = addon()

    for i in range(1, 100):
        plugin_id = oInputParameterHandler.getValue('id' + str(i))
        if plugin_id:
            value = oInputParameterHandler.getValue('value' + str(i))
            value = value.replace('\n', '')
            oldSetting = addons.getSetting(plugin_id)
            if oldSetting != value:
                addons.setSetting(plugin_id, value)

    return True


def isHosterGui(sSiteName, sFunction):
    if sSiteName == 'cHosterGui':
        plugins = __import__('resources.lib.gui.hoster', fromlist=['cHosterGui']).cHosterGui()
        function = getattr(plugins, sFunction)
        function()
        return True
    return False

def isGui(sSiteName, sFunction):
    if sSiteName == 'cGui':
        oGui = cGui()
        exec("oGui." + sFunction + "()")
        return True
    return False


def isFav(sSiteName, sFunction):
    if sSiteName == 'cFav':
        plugins = __import__('resources.lib.bookmark', fromlist=['cFav']).cFav()
        function = getattr(plugins, sFunction)
        function()
        return True
    return False

def isWatched(sSiteName, sFunction):
    if sSiteName == 'cWatched':
        plugins = __import__('resources.lib.watched', fromlist=['cWatched']).cWatched()
        function = getattr(plugins, sFunction)
        function()
        return True
    return False

def isViewing(sSiteName, sFunction):
    if sSiteName == 'cViewing':
        plugins = __import__('resources.lib.viewing', fromlist=['cViewing']).cViewing()
        function = getattr(plugins, sFunction)
        function()
        return True
    return False


def isLibrary(sSiteName, sFunction):
    if sSiteName == 'cLibrary':
        plugins = __import__('resources.lib.library', fromlist=['cLibrary']).cLibrary()
        function = getattr(plugins, sFunction)
        function()
        return True
    return False


def isDl(sSiteName, sFunction):
    if sSiteName == 'cDownload':
        plugins = __import__('resources.lib.download', fromlist=['cDownload']).cDownload()
        function = getattr(plugins, sFunction)
        function()
        return True
    return False


def isHome(sSiteName, sFunction):
    if sSiteName == 'cHome':
        oHome = cHome()
        exec("oHome." + sFunction + "()")
        return True
    return False

def isSearch(sSiteName, sFunction):
    if sSiteName == 'cSearch' or sSiteName == 'globalSearch':
        oSearch = cSearch()
        if sSiteName == 'globalSearch':
            exec("oSearch.searchGlobal()")
        else:
            exec("oSearch." + sFunction + "()")
        return True
    return False

def isTrakt(sSiteName, sFunction):
    if sSiteName == 'cTrakt':
        plugins = __import__('resources.lib.trakt', fromlist=['cTrakt']).cTrakt()
        function = getattr(plugins, sFunction)
        function()
        return True
    return False

def _pluginSearch(plugin, sSearchText):

    window(10101).setProperty('search', 'true')

    try:
        plugins = __import__('resources.sites.%s' % plugin['identifier'], fromlist=[plugin['identifier']])
        function = getattr(plugins, plugin['search'][1])
        sUrl = plugin['search'][0] + str(sSearchText)

        function(sUrl)

        VSlog('Load Search: ' + str(plugin['identifier']))
    except:
        VSlog(plugin['identifier'] + ': search failed')

    window(10101).setProperty('search', 'false')

main()
