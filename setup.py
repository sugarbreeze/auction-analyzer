from distutils.core import setup
import py2exe

setup(
    windows=[{"script":"24au helper.py", "uac_info": "requireAdministrator", "icon_resources": [(1, "icon.ico")]}],
    options={"py2exe": {"includes":["grab","random","Tkinter","time","datetime","pickle","logging","lxml"]}}
)