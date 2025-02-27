#-*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.comaddon import progress, addon, xbmcgui, VSlog, dialog, VSPath
import xbmcvfs, datetime, time, _strptime, os

SITE_IDENTIFIER = 'Enregistrement'
SITE_NAME = 'enregistrement'

class cEnregistremement:

    def programmation_enregistrement(self, sUrl):
        oGui = cGui()
        ADDON = addon()
        if '.m3u8' in sUrl:
            header = '-fflags +genpts+igndts -y -i "' + sUrl + '"'
        else:
            header = '-re -reconnect 1 -reconnect_at_eof 1 -reconnect_streamed 1 -reconnect_delay_max 4294 -timeout 2000000000 -f mpegts -re -flags +global_header -fflags +genpts+igndts -y -i "' + sUrl +'" -headers "User-Agent: Mozilla/5.0+(X11;+Linux+i686)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Ubuntu+Chromium/48.0.2564.116+Chrome/48.0.2564.116+Safari/537.36" -sn -c:v libx264 -c:a copy -map 0 -segment_format mpegts -segment_time -1'

        pathEnregistrement = ADDON.getSetting('path_enregistrement_programmation')
        currentPath = ADDON.getSetting('path_enregistrement').replace('\\', '/')
        ffmpeg = ADDON.getSetting('path_ffmpeg').replace('\\', '/')

        heureFichier = oGui.showKeyBoard(heading = "Début d'enregistrement au format Jour-Heure-Minute, vide pour maintenant")
        heureFin = oGui.showKeyBoard(heading = "Heure de fin d'enregistrement au format Heure-Minute")
        if not heureFin:   # pas de fin, on annule
            return
        titre = oGui.showKeyBoard(heading = "Titre de l'enregistrement").replace("'", "\\'")
        if not titre:
            return


        # début non précisé -> enregistrement maintenant
        if not heureFichier:
            d = datetime.now()
            heureFichier = d.strftime('%d-%H-%M')

        heureDebut = GetTimeObject(heureFichier, '%d-%H-%M')
        heureFin = GetTimeObject(heureFin, '%H-%M')
        duree = heureFin - heureDebut

        marge = ADDON.getSetting('marge_auto')
        timedelta = datetime.timedelta(minutes = int(marge))

        duree += timedelta

        realPath = VSPath(pathEnregistrement + '/' + str(heureFichier) + '.py').replace('\\', '\\\\')

        f = xbmcvfs.File(realPath, 'w')
        read = f.write('''#-*- coding: utf-8 -*-
import os,subprocess
command = '"''' + ffmpeg + '''" ''' + header + ''' -t ''' + str(duree) + ''' "''' + currentPath + '/' + titre + '''.mkv"'
proc = subprocess.Popen(command, stdout=subprocess.PIPE)
p_status = proc.wait()
f = open("'''+currentPath+'''/test.txt",'w')
f.write('Fini avec code erreur ' + str(p_status))
f.close()''')
        f.close()
        oDialog = dialog().VSinfo('Restart Kodi to take the schedule into account', 'MatrixFlix', 10)
        oGui.setEndOfDirectory()

def GetTimeObject(duree, formats):
    try:
        res = datetime.datetime.strptime(duree, formats).time()
    except TypeError:
        res = datetime.datetime(*time.strptime(duree, formats)[0:6]).time()
    tmp_datetime = datetime.datetime.combine(datetime.date.today(), res)
    return tmp_datetime
