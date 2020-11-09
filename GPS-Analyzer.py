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

class Controller(tk.Tk):

    def __init__(self, path_app):
        super().__init__()
        self.title('Extended PyGISS')
        path_icon = abspath(join(path_app, pardir, 'images'))
        
        # generate the PSF tk images
        img_psf = ImageTk.Image.open(join(path_icon, 'node.png'))
        selected_img_psf = ImageTk.Image.open(join(path_icon, 'selected_node.png'))
        self.psf_button_image = ImageTk.PhotoImage(img_psf.resize((100, 100)))
        self.node_image = ImageTk.PhotoImage(img_psf.resize((40, 40)))
        self.selected_node_image = ImageTk.PhotoImage(selected_img_psf.resize((40, 40)))

        for widget in (
                       'Button',
                       'Label', 
                       'Labelframe', 
                       'Labelframe.Label', 
                       ):
            ttk.Style().configure('T' + widget, background='#A1DBCD')

        self.map = Map(self)
        self.map.pack(side='right', fill='both', expand=1)

        self.menu = Menu(self)
        self.menu.pack(side='right', fill='both', expand=1)

        menu = tk.Menu(self)
        menu.add_command(label="Import shapefile", command=self.map.import_map)
        self.config(menu=menu)

        # if motion is called, the left-click button was released and we 
        # can stop the drag and drop process
        self.bind_all('<Motion>', self.stop_drag_and_drop)
        self.drag_and_drop = False

        self.image = None
        self.bind_all('<B1-Motion>', lambda _:_)

    def stop_drag_and_drop(self, event):
        self.drag_and_drop = False

    def start_drag_and_drop(self, event):
        self.drag_and_drop = True

class Menu(tk.Frame):

    def __init__(self, controller):            
        super().__init__(controller)
        self.configure(background='#A1DBCD')   

        lf_creation = ttk.Labelframe(
            self, 
            text = 'Object management', 
            padding = (6, 6, 12, 12)
        )
        lf_creation.grid(row=0, column=0, padx=5, pady=5)

        psf_object_label = tk.Label(
            self, 
            image = controller.psf_button_image, 
            relief = 'flat', 
            bg = '#A1DBCD'
        )
        psf_object_label.bind('<Button-1>', controller.start_drag_and_drop)
        psf_object_label.grid(row=0, column=0, pady=10, padx=55, in_=lf_creation)

        import_nodes_button = ttk.Button(
            self,
            text='Import nodes',
            command=controller.map.import_nodes,
            width=20
        )
        import_nodes_button.grid(row=2, column=0, pady=5, in_=lf_creation)

        lf_projection = ttk.Labelframe(
            self, 
            text = 'Projection management', 
            padding = (6, 6, 12, 12)
        )
        lf_projection.grid(row=1, column=0, padx=5, pady=5)

        self.projection_list = ttk.Combobox(self, width=18)
        self.projection_list['values'] = tuple(controller.map.projections)
        self.projection_list.current(0)
        self.projection_list.grid(row=0, column=0, in_=lf_projection)

        change_projection_button = ttk.Button(
            self,
            text='Change projection',
            command=controller.map.change_projection,
            width=20
        )
        change_projection_button.grid(row=1, column=0, pady=5, in_=lf_projection)

        lf_map_management = ttk.Labelframe(
            self, 
            text = 'Map management', 
            padding = (6, 6, 12, 12)
        )
        lf_map_management.grid(row=2, column=0, padx=5, pady=5)

        delete_map = ttk.Button(
            self,
            text='Delete map',
            command=controller.map.delete_map,
            width=20
        )
        delete_map.grid(row=0, column=0, pady=5, in_=lf_map_management)

        delete_selection = ttk.Button(
            self,
            text='Delete selected nodes',
            command=controller.map.delete_selected_nodes,
            width=20
        )
        delete_selection.grid(row=1, column=0, pady=5, in_=lf_map_management)
