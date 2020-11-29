import requests
import pandas as pd
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
                    'Pyproj, Shapefile and Shapely are required')
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

lat=0
lon=0

def weather_analyze():
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None
    lat_long = "lat=" + str(lat)+ "&lon=" + str(lon)
    coord_API_endpoint = "http://api.openweathermap.org/data/2.5/weather?"
    join_key = "&appid=" + "7686f25ddee9d045def41fd27e2c576c"
    units = "&units=metric"
    current_coord_weather_url = coord_API_endpoint + lat_long + "&units=metric&&appid=9d06d9b4825f10f79591ff063769f070"
    print(lat,lon)

    json_data = requests.get(current_coord_weather_url).json()
    print(json_data)

    df_all_current_weather = pd.DataFrame()

    # Create empty lists to store the JSON Data
    current_time = []
    city = []
    latitude = []
    longitude = []
    country = []
    timezone = []
    sunrise = []
    sunset = []
    temperature = []
    temperature_feel = []
    temperature_min = []
    temperature_max = []
    pressure = []
    humidity = []
    main = []
    main_description = []
    clouds = []
    wind_speed = []
    wind_degree = []
    visibility = []

    # Add JSON Data to the lists
    current_time.append(pd.Timestamp.now())
    city.append(json_data['name'])
    latitude.append(json_data['coord']['lat'])
    longitude.append(json_data['coord']['lon'])
    country.append(json_data['sys']['country'])
    if json_data['timezone'] >0 :
        timezone.append(("+" + str((json_data['timezone'])/3600)))
    else:
        timezone.append(((json_data['timezone'])/3600))
    sunrise.append(json_data['sys']['sunrise'])
    sunset.append(json_data['sys']['sunset'])
    temperature.append(json_data['main']['temp'])
    temperature_feel.append(json_data['main']['feels_like'])
    temperature_min.append(json_data['main']['temp_min'])
    temperature_max.append(json_data['main']['temp_max'])
    pressure.append(json_data['main']['pressure'])
    humidity.append(json_data['main']['humidity'])
    main.append(json_data['weather'][0]['main'])
    main_description.append(json_data['weather'][0]['description'])
    clouds.append(json_data['clouds']['all'])
    wind_speed.append(json_data['wind']['speed'])
    wind_degree.append(json_data['wind']['deg'])
    visibility.append(json_data['visibility'])

    # Write Lists to DataFrame
    df_all_current_weather['current_time'] = current_time
    # df_all_current_weather['own_city_id'] = own_city_id
    df_all_current_weather['city'] = city
    df_all_current_weather['latitude'] = latitude
    df_all_current_weather['longitude'] = longitude
    df_all_current_weather['country'] = country
    df_all_current_weather['timezone'] = timezone
    df_all_current_weather['sunrise'] = sunrise
    df_all_current_weather['sunset'] = sunset
    df_all_current_weather['temperature'] = temperature
    df_all_current_weather['temperature_feel'] = temperature_feel
    df_all_current_weather['temperature_min'] = temperature_min
    df_all_current_weather['temperature_max'] = temperature_max
    df_all_current_weather['pressure'] = pressure
    df_all_current_weather['humidity'] = humidity
    df_all_current_weather['main'] = main
    df_all_current_weather['main_description'] = main_description
    df_all_current_weather['clouds'] = clouds
    df_all_current_weather['wind_speed'] = wind_speed
    df_all_current_weather['wind_degree'] = wind_degree
    df_all_current_weather['visibility'] = visibility

    root = tk.Tk()
    root.title("Weather Module")
    root.configure(background = "light green")
    headlabel = tk.Label(root, text = "Weather Module", fg = 'black', bg = 'red')
    
    time_label = tk.Label(root, text = "Date/Time - ", fg = 'black', bg = 'light green')
    time_label.grid(row = 0, column = 0)
    time_field = tk.Entry(root,width=100)
    time_field.grid(row = 0 , column = 1)
    time_field.insert(500, str(current_time)[12:-13])
    
    time_label = tk.Label(root, text = "City - ", fg = 'black', bg = 'light green')
    time_label.grid(row = 1, column = 0)
    time_field = tk.Entry(root,width=100)
    time_field.grid(row = 1 , column = 1)
    time_field.insert(500, str(city)[2:-2])
    
    time_label = tk.Label(root, text = "Latitude - ", fg = 'black', bg = 'light green')
    time_label.grid(row = 2, column = 0)
    time_field = tk.Entry(root,width=100)
    time_field.grid(row = 2 , column = 1)
    time_field.insert(500, str(latitude)[1:-1]+"°")
    
    time_label = tk.Label(root, text = "Longitude - ", fg = 'black', bg = 'light green')
    time_label.grid(row = 3, column = 0)
    time_field = tk.Entry(root,width=100)
    time_field.grid(row = 3, column = 1)
    time_field.insert(500, str(longitude)[1:-1]+"°")
    
    time_label = tk.Label(root, text = "Country- ", fg = 'black', bg = 'light green')
    time_label.grid(row = 4, column = 0)
    time_field = tk.Entry(root,width=100)
    time_field.grid(row = 4 , column = 1)
    time_field.insert(500, str(country)[2:-2])
    
    time_label = tk.Label(root, text = "TimeZone - ", fg = 'black', bg = 'light green')
    time_label.grid(row = 5, column = 0)
    time_field = tk.Entry(root,width=100)
    time_field.grid(row = 5 , column = 1)
    time_field.insert(500, "UTC "+str(timezone)[2:-2])
    
    time_label = tk.Label(root, text = "Temperature - ", fg = 'black', bg = 'light green')
    time_label.grid(row = 6, column = 0)
    time_field = tk.Entry(root,width=100)
    time_field.grid(row = 6 , column = 1)
    time_field.insert(500, str(temperature)[1:-1]+" °Celcius")
    
    time_label = tk.Label(root, text = "Maximum Temperature - ", fg = 'black', bg = 'light green')
    time_label.grid(row = 7, column = 0)
    time_field = tk.Entry(root,width=100)
    time_field.grid(row = 7 , column = 1)
    time_field.insert(500, str(temperature_max)[1:-1]+" °Celcius")
    
    time_label = tk.Label(root, text = "Minimum Temperature - ", fg = 'black', bg = 'light green')
    time_label.grid(row = 8, column = 0)
    time_field = tk.Entry(root,width=100)
    time_field.grid(row = 8 , column = 1)
    time_field.insert(500, str(temperature_min)[1:-1]+" °Celcius")
    
    time_label = tk.Label(root, text = "Pressure - ", fg = 'black', bg = 'light green')
    time_label.grid(row = 9, column = 0)
    time_field = tk.Entry(root,width=100)
    time_field.grid(row = 9 , column = 1)
    time_field.insert(500, str(pressure)[1:-1]+" millibar")
    
    time_label = tk.Label(root, text = "Humidity - ", fg = 'black', bg = 'light green')
    time_label.grid(row = 10, column = 0)
    time_field = tk.Entry(root,width=100)
    time_field.grid(row = 10 , column = 1)
    time_field.insert(500, str(humidity)[1:-1]+"%")
    
    time_label = tk.Label(root, text = "Wind Speed - ", fg = 'black', bg = 'light green')
    time_label.grid(row = 11, column = 0)
    time_field = tk.Entry(root,width=100)
    time_field.grid(row = 11 , column = 1)
    time_field.insert(500, str(wind_speed)[1:-1]+"mph")
    
    time_label = tk.Label(root, text = "Wind Degree - ", fg = 'black', bg = 'light green')
    time_label.grid(row = 12, column = 0)
    time_field = tk.Entry(root,width=100)
    time_field.grid(row = 12 , column = 1)
    time_field.insert(500, str(wind_degree)[1:-1]+"°")
    
    time_label = tk.Label(root, text = "Visibility - ", fg = 'black', bg = 'light green')
    time_label.grid(row = 13, column = 0)
    time_field = tk.Entry(root,width=100)
    time_field.grid(row = 13 , column = 1)
    time_field.insert(500, str(visibility)[1:-1]+" m") 
    root.mainloop()
    
    print(df_all_current_weather.head())


class Controller(tk.Tk):

    def __init__(self, path_app):
        super().__init__()
        self.title('GPS Data Analyzer')
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
            text = '', 
            padding = (6, 6, 12, 12)
        )
        lf_projection.grid(row=1, column=0, padx=5, pady=5)

        self.projection_list = ttk.Combobox(self, width=18)
        self.projection_list['values'] = tuple(controller.map.projections)
        self.projection_list.current(0)
        self.projection_list.grid(row=0, column=0, in_=lf_projection)

        change_projection_button = ttk.Button(
            self,
            text='Analyze',
            command=weather_analyze,
            width=22
        )
        change_projection_button.grid(row=0, column=0, pady=5, in_=lf_projection)

        from_label=ttk.Label(self,text="From Date")
        from_label.grid(row=1, column=0, pady=5, in_=lf_projection)

        from_date = ttk.Entry(
            self,
            width=22
        )
        from_date.insert(0,"DD-MM-YYYY")

        from_date.grid(row=3, column=0, pady=5, in_=lf_projection)

        from_label=ttk.Label(self,text="To Date")
        from_label.grid(row=5, column=0, pady=5, in_=lf_projection)

        to_date = ttk.Entry(
            self,
            width=22
        )
        to_date.grid(row=7, column=0, pady=5, in_=lf_projection)
        to_date.insert(0,"DD-MM-YYYY")

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


class PSF_Object():

    type = 'node'

    def __init__(self, id, label_id, x, y):
        self.id = id
        self.label_id = label_id
        self.x, self.y = x, y
        self.longitude, self.latitude = 0, 0


class Map(tk.Canvas):

    projections = {
    'Mercator': pyproj.Proj(init="epsg:3395"),
    'Azimuthal orthographic': pyproj.Proj('+proj=ortho +lon_0=28 +lat_0=47')
    }

    size = 10

    def __init__(self, controller):
        super().__init__(controller, bg='white', width=1300, height=800)
        self.controller = controller
        self.node_id_to_node = {}
        self.drag_item = None
        self.start_position = [None]*2
        self.start_pos_main_node = [None]*2
        self.dict_start_position = {}
        self.selected_nodes = set()
        self.filepath = None
        self.proj = 'Mercator'
        self.ratio, self.offset = 1, (0, 0)
        self.bind('<MouseWheel>', self.zoomer)
        self.bind('<Button-4>', lambda e: self.zoomer(e, 1.3))
        self.bind('<Button-5>', lambda e: self.zoomer(e, 0.7))
        self.bind('<ButtonPress-3>', lambda e: self.scan_mark(e.x, e.y))
        self.bind('<B3-Motion>', lambda e: self.scan_dragto(e.x, e.y, gain=1))
        self.bind('<Enter>', self.drag_and_drop, add='+')
        self.bind('<ButtonPress-1>', self.start_point_select_objects, add='+')
        self.bind('<B1-Motion>', self.rectangle_drawing)
        self.bind('<ButtonRelease-1>', self.end_point_select_nodes, add='+')
        self.tag_bind('node', '<Button-1>', self.find_closest_node)
        self.tag_bind('node', '<B1-Motion>', self.node_motion)

    def update_coordinates(function):
        def wrapper(self, event, *others):
            event.x, event.y = self.canvasx(event.x), self.canvasy(event.y)
            function(self, event, *others)
        return wrapper

    def to_canvas_coordinates(self, longitude, latitude):
        px, py = self.projections[self.proj](longitude, latitude)
        return px*self.ratio + self.offset[0], -py*self.ratio + self.offset[1]

    def to_geographical_coordinates(self, x, y):
        global lon
        global lat
        px, py = (x - self.offset[0])/self.ratio, (self.offset[1] - y)/self.ratio
        lon,lat=list(self.projections[self.proj](px, py, inverse=True))
        return self.projections[self.proj](px, py, inverse=True)

    def import_map(self):
        filepath = tk.filedialog.askopenfilenames(title='Import shapefile')
        if not filepath: 
            return
        else: 
            self.filepath ,= filepath
        self.draw_map()

    def draw_map(self):
        if not self.filepath:
            return
        self.delete('land', 'water')
        self.ratio, self.offset = 1, (0, 0)
        self.draw_water()
        sf = shapefile.Reader(self.filepath)       
        polygons = sf.shapes() 
        for polygon in polygons:
            polygon = shapely.geometry.shape(polygon)
            if polygon.geom_type == 'Polygon':
                polygon = [polygon]
            for land in polygon:
                self.create_polygon(
                    sum((self.to_canvas_coordinates(*c) for c in land.exterior.coords), ()),    
                    fill = 'green3', 
                    outline = 'black', 
                    tags = ('land',)
                )
        self.redraw_nodes()

    def delete_map(self):
        self.delete('land', 'water')
        self.filepath = None

    def delete_selected_nodes(self):
        for node in self.selected_nodes:
            self.node_id_to_node.pop(node.id)
            self.delete(node.id, node.label_id)
        self.selected_nodes.clear()

    def draw_water(self):
        if self.proj == 'Mercator':
            x0, y0 = self.to_canvas_coordinates(-180, 84)
            x1, y1 = self.to_canvas_coordinates(180, -84)
            self.water_id = self.create_rectangle(x1, y1, x0, y0,
                        outline='black', fill='deep sky blue', tags=('water',))
        else:
            cx, cy = self.to_canvas_coordinates(28, 47)
            R = 6378000*self.ratio
            self.water_id = self.create_oval(cx - R, cy - R, cx + R, cy + R,
                        outline='black', fill='deep sky blue', tags=('water',))

    def change_projection(self):
        self.proj = self.controller.menu.projection_list.get()
        self.draw_map()

    def redraw_nodes(self):
        for node_id, node in self.node_id_to_node.items():
            cx, cy = self.to_canvas_coordinates(node.longitude, node.latitude)
            node.x, node.y = cx, cy
            self.coords(node_id, cx, cy)
            self.update_node_label(node)
            self.tag_raise(node_id)
            self.tag_raise(node.label_id)

    @update_coordinates
    def zoomer(self, event, factor=None):
        if not factor: 
            factor = 1.3 if event.delta > 0 else 0.7
        self.scale('all', event.x, event.y, factor, factor)
        self.configure(scrollregion=self.bbox('all'))
        self.ratio *= float(factor)
        self.offset = (self.offset[0]*factor + event.x*(1 - factor), 
                       self.offset[1]*factor + event.y*(1 - factor))
        # we update all node's coordinates
        for node_id, node in self.node_id_to_node.items():
            node.x, node.y = self.coords(node_id)
            self.update_node_label(node)

    def update_node_label(self, node):
        node.longitude, node.latitude = self.to_geographical_coordinates(
                                                                node.x, node.y)
        label = '({:.5f}, {:.5f})'.format(node.longitude, node.latitude)
        self.coords(node.label_id, node.x - 5, node.y + 30)
        self.itemconfig(node.label_id, text=label)

    @update_coordinates            
    def drag_and_drop(self, event):
        if controller.drag_and_drop:
            self.create_object(event.x, event.y)
            controller.drag_and_drop = False

    def create_object(self, x, y):
        # create the node's image
        id = self.create_image(x, y,image = controller.node_image, tags = ('node',))
        # create the node's label
        label_id = self.create_text(x - 5, y + 30)
        # create the node object
        node = PSF_Object(id, label_id, x, y)
        # update the value of its label
        self.update_node_label(node)
        # store the node in the (node ID -> node) dictionnary
        self.node_id_to_node[id] = node

    @update_coordinates
    def find_closest_node(self, event):
        self.dict_start_position.clear()
        self.drag_item = self.find_closest(event.x, event.y)[0]
        main_node_selected = self.node_id_to_node[self.drag_item]
        self.start_pos_main_node = event.x, event.y
        if main_node_selected in self.selected_nodes:
            for sn in self.selected_nodes:
                self.dict_start_position[sn] = [sn.x, sn.y]
        else:
            self.unselect_all()
            self.dict_start_position[main_node_selected] = self.start_pos_main_node 
            self.select_objects(main_node_selected)

    def select_objects(self, *objects):
        for obj in objects:
            self.selected_nodes.add(obj)
            self.itemconfig(
                            obj.id, 
                            image = self.controller.selected_node_image
                            )

    def unselect_objects(self, *objects):
        for obj in objects:
            self.selected_nodes.discard(obj)
            self.itemconfig(
                            obj.id, 
                            image = self.controller.node_image
                            )

    def unselect_all(self):
        self.unselect_objects(*self.selected_nodes)

    @update_coordinates
    def start_point_select_objects(self, event):
        # create the temporary line, only if there is nothing below
        # this is to avoid drawing a rectangle when moving a node
        below = self.find_overlapping(event.x-1, event.y-1, event.x+1, event.y+1)
        tags_below = ''.join(''.join(self.itemcget(id, 'tags')) for id in below)
        # if no object is below the selection process can start
        if 'node' not in tags_below:
            self.unselect_all()
            self.start_position = event.x, event.y
            self.temp_rectangle = self.create_rectangle(
                event.x, 
                event.y, 
                event.x, 
                event.y
            )
            self.tag_raise(self.temp_rectangle)

    @update_coordinates
    def rectangle_drawing(self, event):
        # draw the line only if they were created in the first place
        if self.start_position != [None]*2:
            # update the position of the temporary lines
            x0, y0 = self.start_position
            self.coords(self.temp_rectangle, x0, y0, event.x, event.y)

    @update_coordinates
    def end_point_select_nodes(self, event):
        if self.start_position != [None]*2:
            # delete the temporary lines
            self.delete(self.temp_rectangle)
            # select all nodes enclosed in the rectangle
            start_x, start_y = self.start_position
            for obj in self.find_enclosed(start_x, start_y, event.x, event.y):
                if obj in self.node_id_to_node:
                    enclosed_obj = self.node_id_to_node[obj]
                    self.select_objects(enclosed_obj)
            self.start_position = [None]*2

    @update_coordinates
    def node_motion(self, event):
        node = self.node_id_to_node[self.drag_item]
        for selected_node in self.selected_nodes:
            # the main node initial position, the main node current position, 
            # and the other node initial position form a rectangle.
            # we find the position of the fourth vertix.
            x0, y0 = self.start_pos_main_node
            x1, y1 = self.dict_start_position[selected_node]
            selected_node.x = x1 + (event.x - x0)
            selected_node.y = y1 + (event.y - y0)
            # move the node itself
            self.coords(selected_node.id, selected_node.x, selected_node.y)
            # update the label
            self.update_node_label(selected_node)

    def import_nodes(self):
        filepath = filedialog.askopenfilenames(filetypes = (('xls files','*.xls'),))
        if not filepath:
            return
        else:
            filepath ,= filepath
        book = xlrd.open_workbook(filepath)
        try:
            sheet = book.sheet_by_index(0)
        # if the sheet cannot be found, there's nothing to import
        except xlrd.biffh.XLRDError:
            warnings.warn('the excel file is empty: import failed')
        for row_index in range(1, sheet.nrows):
            x, y = self.to_canvas_coordinates(*sheet.row_values(row_index))
            self.create_object(x, y)

if str.__eq__(__name__, '__main__'):
    controller = Controller(path_app)
    controller.mainloop()
