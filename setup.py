#  setup.py
#
#  Copyright 2015 Sylvan Mostert <smostert.dev@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

# Use the command: python setup.py py2exe

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
