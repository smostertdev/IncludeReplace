#python setup.py py2exe
# setup.py
from distutils.core import setup
import py2exe


dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll',
                'tk84.dll','MSVCP90.dll']

setup(
    data_files = ["icon.ico"],
    options = {"py2exe": {"compressed": 2,
                          "optimize": 2,
                          #"includes": includes,
                          #"excludes": excludes,
                          #"packages": packages,
                          "dll_excludes": dll_excludes,
                          "bundle_files": 1,
                          "dist_dir": "dist",
                          "xref": False,
                          "skip_archive": False,
                          "ascii": False,
                          "custom_boot_script": ''
                         }
              },
    zipfile = None,
    windows = [{"script": "IncludeReplace.py", "icon_resources": [(1, "icon.ico")]}]
    )
