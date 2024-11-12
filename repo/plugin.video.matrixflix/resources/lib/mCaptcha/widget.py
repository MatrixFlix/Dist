import xbmc
import os
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('8.8.8.8', 80))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

ip_address = get_ip()
port = 9001

def get_kodi_script_path(script_name):
    """Gets the full path to a script within the Kodi add-on.

    Args:
        script_name: The name of the script.

    Returns:
        The full path to the script.
    """

    addon_path = ('special://home/addons/plugin.video.matrixflix/resources/lib/')
    script_path = os.path.join(addon_path, 'mCaptcha', script_name + '.py')
    return script_path

def execute_captcha(script_path, captcha):
    """Executes a Python script within the Kodi environment.

    Args:
        script_path: The full path to the script.
    """

    xbmc.executebuiltin('RunScript(' + script_path + ' "%s" "%s" "%s"' % (captcha, ip_address, port) + ')')

