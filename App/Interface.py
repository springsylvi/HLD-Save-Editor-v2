import os.path
import math
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror
from HLDConstants import HLDConstants


class EditorUIObj(Frame):
    """
    A generic UI object for editing savedata
    
    Contains one of Checkbutton, Entry + Label, or OptionMenu + Label, as well as its associated variables
    """

    def __init__(self, master, uitype, text, initial_value, menu_options=None, **kw):
        super().__init__(master=master, **kw)
        self.uitype = uitype
        if uitype == "Checkbutton":
            self.var = IntVar(master=self, value=int(initial_value))
            self.obj = Checkbutton(self, text=text, variable=self.var)
            self.obj.grid(column=0, row=0)
        elif uitype == "Entry":
            self.var = None
            self.obj = Entry(self, width=10)
            self.obj.insert(0, initial_value)
            self.label = Label(self, text=text)
            self.obj.grid(column=0, row=0)
            self.label.grid(column=1, row=0)
        elif uitype == "OptionMenu":
            self.var = StringVar(master=self, value=initial_value)
            self.omframe = Frame(master=self, width=30)
            self.obj = OptionMenu(self.omframe, self.var, *menu_options)
            self.label = Label(self, text=text)
            self.obj.pack(anchor="w")
            self.omframe.grid(column=0, row=0, sticky="w")
            self.label.grid(column=1, row=0, sticky="e")
            # TODO - tidy up this packing to align dropdowns


    def get(self):
        if self.uitype == "Checkbutton" or self.uitype == "OptionMenu":
            return self.var.get()
        elif self.uitype == "Entry":
            return self.obj.get()
        else:
            raise Exception("Unknown uitype")

    def set_value(self, value):
        if self.uitype == "Checkbutton":
            self.var.set(value)
        elif self.uitype == "Entry":
            self.obj.delete(0, END)
            self.obj.insert(0, value)
        elif self.uitype == "OptionMenu":
            pass
            # TODO


class Interface():
    """
    GUI manager
    """

    # file -> load
    def load(self, event=None):
        try:
            filename = filedialog.askopenfilename(initialdir=self.app.savefile_path)
            if filename is None or filename == "":
                return
            self.editor.load(filename)
            self.init_editor_ui(self.editor)
            self.set_status_message(f"loaded data from {os.path.basename(filename)}")
        except Exception as e:
            showerror(title=type(e), message=e)


    # file -> save
    def save(self, event=None):
        try:
            filename = self.editor.filename
            if filename is None:
                filename = filedialog.asksaveasfilename(initialdir=self.app.savefile_path, defaultextension=".hlds", filetypes=[("HLDS File", "*.hlds")])
            if filename is None or filename == "":
                return
            self.sync_savedata()
            self.editor.save(filename)
            self.set_status_message(f"saved data to {os.path.basename(filename)}")
        except Exception as e:
            showerror(title=type(e), message=e)


    # file -> save as
    def saveas(self):
        try:
            filename = filedialog.asksaveasfilename(initialdir=self.app.savefile_path, defaultextension=".hlds", filetypes=[("HLDS File", "*.hlds")])
            if filename is None or filename == "":
                return
            self.sync_savedata()
            self.editor.save(filename)
            self.set_status_message(f"saved data to {os.path.basename(filename)}")
        except Exception as e:
            showerror(title=type(e), message=e)

    
    # file -> export
    def export(self, slot):
        try:
            self.sync_savedata()
            self.editor.export(slot)
            self.set_status_message(f"exported data to slot {slot}")
        except Exception as e:
            showerror(title=type(e), message=e)


    # options -> import header
    def import_header(self):
        try:
            filename = filedialog.askopenfilename(initialdir=self.app.savefile_path, filetypes=[("Savefile", "*.sav")])
            self.editor.get_header(filename)
        except Exception as e:
            showerror(title=type(e), message=e)


    # set status bar text to message
    def set_status_message(self, message):
        self.sbar_label.config(text=message)
        # TODO - log past messages, including errors?


    def __init__(self, editor, app):
        self.editor = editor
        self.app = app
        self.tk = Tk(screenName="Editor")
        self.tk.option_add('*tearOff', FALSE)

        self.window = Frame(self.tk, width=500, height=500) # main window
        self.sbar = Frame(self.tk) # status bar
        
        # menus
        self.menu = Menu(self.tk)
        self.filemenu = Menu(self.menu)
        self.exportmenu = Menu(self.filemenu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.optionmenu = Menu(self.menu)
        self.menu.add_cascade(label="Options", menu=self.optionmenu)

        self.filemenu.add_command(label="Load", command=self.load, accelerator="Ctrl+L")
        self.filemenu.add_command(label="Save", command=self.save, accelerator="Ctrl+S")
        self.filemenu.add_command(label="Save As", command=self.saveas)
        self.filemenu.add_cascade(label="Export", menu=self.exportmenu)
        self.exportmenu.add_command(label="Slot 0", command=lambda: self.export(0), accelerator="Ctrl+0")
        self.exportmenu.add_command(label="Slot 1", command=lambda: self.export(1), accelerator="Ctrl+1")
        self.exportmenu.add_command(label="Slot 2", command=lambda: self.export(2), accelerator="Ctrl+2")
        self.exportmenu.add_command(label="Slot 3", command=lambda: self.export(3), accelerator="Ctrl+3")

        self.optionmenu.add_command(label="Import Header", command=self.import_header)

        # menu shortcuts
        self.tk.bind("<Control-KeyPress-0>", lambda x: self.export(0))
        self.tk.bind("<Control-KeyPress-1>", lambda x: self.export(1))
        self.tk.bind("<Control-KeyPress-2>", lambda x: self.export(2))
        self.tk.bind("<Control-KeyPress-3>", lambda x: self.export(3))
        self.tk.bind("<Control-l>", self.load)
        self.tk.bind("<Control-s>", self.save)
        self.tk.config(menu=self.menu)

        # status bar
        self.sbar_label = Label(self.sbar)
        self.sbar_label.pack(padx=5, pady=5, side=LEFT)

        self.window.pack()
        self.sbar.pack(side=BOTTOM, fill=X)


        # data stored in user input fields; list of (name, object) tuples
        self.input_fields = []


    # open a window to choose room by name, write choice into pos_value # TODO - add entrance choosing too
    def get_entrance(self, pos_value):
        top = Toplevel(self.tk)
        top.title("Entrance Chooser")
        room = IntVar(master=top, value=46)
        i = 0
        for room_id, (room_iname, room_cname) in HLDConstants.roomNames.items():
            x = Radiobutton(top, text=room_cname, variable=room, value=room_id)
            x.grid(column=i//31, row=i%31)
            i = i+1
        ok_button = Button(top, text="OK", command=lambda: self.finish_entrance_selection(top, pos_value, room.get()), width=20)
        ok_button.grid(pady=10, column=0, row=31, columnspan=6)
        

    # close window and write values after selecting entrance
    def finish_entrance_selection(self, win, pos_value, room_num):
        pos_value[0].set_value(-10.0)
        pos_value[1].set_value(-10.0)
        pos_value[2].set_value(room_num)
        win.destroy()


    # load widgets for editing savedata
    def init_editor_ui(self, editor):

        savedata = editor.savedata

        # main window
        try:
            self.notebook.destroy() # remove old window
        except:
            pass
        self.notebook = ttk.Notebook(self.window)
        collect = Frame(self.notebook)
        current = Frame(self.notebook)
        misc =  Frame(self.notebook)
        collect.pack()
        current.pack()
        misc.pack()
        self.notebook.add(collect, text="Collectable Status")
        self.notebook.add(current, text="Current State")
        self.notebook.add(misc, text="Misc")
        self.notebook.pack(padx=5, pady=5)

        # list of (iname, fieldtext, uitype, value, row_num, grid_pos, const_data, is_list) tuples where
        #   iname (str) : internal name of the field
        #   fieldtext (str) : text displayed above UI section
        #   uitype (str) : type of ui object used for editing this field (Checkbutton, Entry, OptionMenu)
        #   value (list) : current value in savedata, type of list elements depends on uitype
        #   row_num (int) : number of rows per column when displaying multiple checkbuttons/etc.
        #   grid_pos (int, int) : overall position in display grid
        #   page (Frame) : which page to diplay on
        #   const_data (list) : constant list of name/values associated with this field type (tuple of 2 lists for uitype == OptionMenu)
        #   is_list (bool) : whether the list corresponds to a single field, instead of a list of different fields
        field_specific_data = [
            ("well", "Pillars", "Checkbutton", [x in savedata.get("well") for x in range(4)], 4, (0,0), collect, HLDConstants.pillar_ids, True),
            ("warp", "Warp Points", "Checkbutton", [x in savedata.get("warp") for x in range(5)], 5, (1,0), collect, HLDConstants.area_ids, True),
            ("skill", "Skills", "Checkbutton", [x in savedata.get("skill") for x in range(1,7)], 3, (2,0), collect, HLDConstants.skill_ids, True),
            ("sc", "Guns", "Checkbutton", [x in savedata.get("sc") for x, y in HLDConstants.gun_ids], 6, (0,1), collect, HLDConstants.gun_ids, True),
            ("scUp", "Gun Upgrades", "Checkbutton", [x in savedata.get("scUp") for x, y in HLDConstants.gun_ids], 6, (1,1), collect, HLDConstants.gun_ids, True),
            ("cShells", "Outfits", "Checkbutton", [x in savedata.get("cShells") for x, y in HLDConstants.outfit_ids], 6, (2,1), collect, HLDConstants.outfit_ids, True),
            ("east_modules", "East Modules", "Checkbutton", [x in savedata.get("cl").get(7) for x, y in HLDConstants.east_modules], 8, (3,0), collect, HLDConstants.east_modules, True),
            ("north_modules", "North Modules", "Checkbutton", [x in savedata.get("cl").get(6) for x, y in HLDConstants.north_modules], 8, (4,0), collect, HLDConstants.north_modules, True),
            ("west_modules", "West Modules", "Checkbutton", [x in savedata.get("cl").get(9) for x, y in HLDConstants.west_modules], 8, (5,0), collect, HLDConstants.west_modules, True),
            ("south_modules", "South Modules", "Checkbutton", [x in savedata.get("cl").get(8) for x, y in HLDConstants.south_modules], 8, (6,0), collect, HLDConstants.south_modules, True),
            ("east_tablet", "East Monoliths", "Checkbutton", [x in savedata.get("tablet") for x, y in HLDConstants.east_tablet_ids], 4, (3,1), collect, HLDConstants.east_tablet_ids, True),
            ("north_tablet", "North Monoliths", "Checkbutton", [x in savedata.get("tablet") for x, y in HLDConstants.north_tablet_ids], 4, (4,1), collect, HLDConstants.north_tablet_ids, True),
            ("west_tablet", "West Monoliths", "Checkbutton", [x in savedata.get("tablet") for x, y in HLDConstants.west_tablet_ids], 4, (5,1), collect, HLDConstants.west_tablet_ids, True),
            ("south_tablet", "South Monoliths", "Checkbutton", [x in savedata.get("tablet") for x, y in HLDConstants.south_tablet_ids], 4, (6,1), collect, HLDConstants.south_tablet_ids, True),
            ("gamemode", "Game Mode", "Checkbutton", [savedata.get(x) for x, y in HLDConstants.gamemode_fields], 2, (0,2), collect, HLDConstants.gamemode_fields, False),
            ("misc_values", "Other Values", "Checkbutton", [savedata.get(x) for x, y in HLDConstants.misc_value_fields], 2, (1,2), collect, HLDConstants.misc_value_fields, False),
            ("upgrades", "Other Upgrades", "Entry", [savedata.get(x) for x, y in HLDConstants.misc_upgrade_fields], 2, (2,2), collect, HLDConstants.misc_upgrade_fields, False),
            ("misc_collect", "Other Collectables", "Entry", [savedata.get(x) for x, y in HLDConstants.misc_collect_fields], 2, (3,2), collect, HLDConstants.misc_collect_fields, False),
            ("cpstate", "Health/Ammo", "Entry", [savedata.get(x) for x, y in HLDConstants.cpstate_fields], 4, (0,0), current, HLDConstants.cpstate_fields, False),
            ("outfit_eq", "Equipped Outfit", "OptionMenu", [savedata.get(x) for x, y in HLDConstants.outfit_components], 3, (1,0), current, (HLDConstants.outfit_ids, HLDConstants.outfit_components), False)
            ]

        # load each section from field_specific_data
        for iname, fieldtext, uitype, value, row_num, grid_pos, page, const_data, is_list in field_specific_data:
            ff = Frame(page)
            ff_label = Label(ff, text=fieldtext)
            ff_editor_objs = []
            for i in range(len(value)):
                if uitype == "OptionMenu":
                    menu_options = [x[1] for x in const_data[0]] # list of possible choices
                    initial_value = const_data[0][int(value[i])][1] # look up current value in table to get name
                    text = const_data[1][i][1] # name of field
                    elem_iname = const_data[1][i][0]
                    obj = EditorUIObj(ff, uitype, text, initial_value, menu_options=menu_options)
                else:
                    elem_iname = const_data[i][0]
                    obj = EditorUIObj(ff, uitype, const_data[i][1], value[i])
                ff_editor_objs.append(obj)
                obj.grid(padx=5, column=i//row_num, row=1+(i%row_num), sticky="w")
                if not is_list: # add each individual element
                    self.input_fields.append((elem_iname, obj))
                    print(elem_iname, obj.get())
            if is_list: # add whole list
                self.input_fields.append((iname, ff_editor_objs))
                print(iname, [x.get() for x in ff_editor_objs])
            ff_label.grid(padx=5, column=0, row=0, columnspan=math.ceil(len(value)/row_num), sticky="n")
            ff.grid(pady=10, column=grid_pos[0], row=grid_pos[1], sticky="n")

        # checkX/checkY/checkRoom + entrance warp
        drifter_pos = Frame(current)
        drifter_pos_label = Label(drifter_pos, text="Current Location")
        drifter_pos_value = [EditorUIObj(drifter_pos, "Entry", v, savedata.get(k)) for k, v in HLDConstants.position_fields]
        drifter_pos_label.grid(column=0, row=0)
        drifter_pos_button = Button(drifter_pos, text="Choose Room", command=lambda: self.get_entrance(drifter_pos_value))
        for i in range(len(drifter_pos_value)):
            drifter_pos_value[i].grid(column=0, row=1+i, sticky="w")
        drifter_pos_button.grid(column=1, row=1)
        drifter_pos.grid(pady=10, column=0, row=1)
            

    # copy changes in UI to savedata dict
    def sync_savedata(self):

        # TODO - reimplement this function to work with new init_editor_ui version

        lists = {
            "well": HLDConstants.pillar_ids,
            "warp": HLDConstants.area_ids,
            "skill": HLDConstants.skill_ids,
            "sc": HLDConstants.gun_ids,
            "scUp": HLDConstants.gun_ids,
            "cShells": HLDConstants.outfit_ids
            }
        module_cltypes = {
            "modulesN": (HLDConstants.north_modules, 6),
            "modulesE": (HLDConstants.east_modules, 7),
            "modulesS": (HLDConstants.south_modules, 8),
            "modulesW": (HLDConstants.west_modules, 9)
            }

        # TODO - fill out and document this section
        for field, obj in self.input_fields:
            # determine type of obj based on field name
            if field in lists.keys():
                const_data = lists[field]
                sd = []
                for i in range(len(const_data)):
                    if obj[i].get():
                        sd.append(const_data[i][0])
                self.editor.savedata.set_field(field, sd)
                if field == "cShells": # copy value to other outfit component lists
                    self.editor.savedata.set_field("cSwords", sd)
                    self.editor.savedata.set_field("cCapes", sd)
            elif field[:-1] == "modules":
                const_data = module_cltypes[field]
                sd = []
                for i in range(len(const_data[0])):
                    if obj[i].get():
                        sd.append(const_data[0][i][0])
                self.editor.savedata.set_map_value("cl", const_data[1], sd)
            elif field in ["hasMap", "fireplaceSave", "checkHP", "checkStash", "checkBat", "checkAmmo", "healthUp", "specialUp", "drifterkey", "gear", "CH", "noviceMode"]: # single value -> float
                self.editor.savedata.set_field(field, float(obj.get()))
            elif field in ["compShell", "sword", "cape"]: # outfit name -> index
                index = [t[1] for t in HLDConstants.outfit_ids].index(obj.get())
                self.editor.savedata.set_field(field, float(index))
            else:
                print("?")
