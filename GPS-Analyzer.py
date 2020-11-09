import sys
import tkinter as tk
import warnings
from inspect import stack
from os.path import abspath, dirname, pardir, join
from PIL import ImageTk
from tkinter import ttk, filedialog
try:
    import pyproj
    import shapefile
    import shapely.geometry
except ImportError:
    from tkinter import messagebox
    tk.messagebox.showinfo('Some libraries are missing', 
                    'Pyproj, Shapefile and Shapely are required (see README)')
    sys.exit(1)
try:
    import xlrd
except ImportError:
    warnings.warn('Excel libraries missing: excel import/export disabled')

# prevent python from writing *.pyc files / __pycache__ folders
sys.dont_write_bytecode = True

path_app = dirname(abspath(stack()[0][1]))

if path_app not in sys.path:
    sys.path.append(path_app)
