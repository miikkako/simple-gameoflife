# 'python3 setup.py bdist_mac' or 'bdist_msi' on windows

application_title = "Game of Life" 
main_python_file = "gameoflife.py" 

import sys

from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

includes = ["pygame"]

setup(
        name = application_title,
        version = "0.1",
        description = "Game of Life setup",
        options = {"build_exe" : {"includes" : includes }},
        executables = [Executable(main_python_file, base = base)])