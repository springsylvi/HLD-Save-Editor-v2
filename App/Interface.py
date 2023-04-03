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
            self.var = IntVar(master=self, value=initial_value)
            self.obj = Checkbutton(self, text=text, variable=self.var)
            self.obj.grid(column=0, row=0)
        elif uitype == "Entry":
            self.var == None
            self.obj = Entry(self, width=10)
            self.obj.insert(0, initial_value)
            self.label = Label(self, text=text)
            self.obj.grid(column=0, row=0)
            self.label.grid(column=1, row=0)
        elif uitype == "OptionMenu":
            self.var = StringVar(master=self, value=initial_value)
            self.obj = OptionMenu(self, self.var, *menu_options)
            self.label = Label(self, text=text)
            self.obj.grid(column=0, row=0)
            self.label.grid(column=1, row=0)


    def get(self):
        if uitype == "Checkbutton" or uitype == "OptionMenu":
            return self.var.get()
        elif uitype == "Entry":
            return self.obj.get()
        else:
            raise Exception("Unknown uitype")



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


    # load page 1 of editor gui (collectable status)
    def init_page_1(self, savedata, page):

        # list of (iname, fieldtext, uitype, value, row_num, grid_pos, const_data) tuples where
        #   iname (str) : internal name of the field
        #   fieldtext (str) : text displayed above UI section
        #   uitype (str) : type of ui object used for editing this field (Checkbutton, Entry, OptionMenu)
        #   value (list) : current value in savedata, type of list elements depends on uitype
        #   row_num (int) : number of rows per column when displaying multiple checkbuttons/etc.
        #   grid_pos (int, int) : overall position in display grid
        #   const_data (list) : constant list of name/values associated with this field type
        field_specific_data = [
            ("well", "Pillars", "Checkbutton", [x in savedata.get("well") for x in range(4)], 4, (0,0), HLDConstants.pillar_ids),
            ("warp", "Warp Points", "Checkbutton", [x in savedata.get("warp") for x in range(5)], 5, (1,0), HLDConstants.area_ids),
            ("skill", "Skills", "Checkbutton", [x in savedata.get("skill") for x in range(1,7)], 3, (2,0), HLDConstants.skill_ids),
            ("sc", "Guns", "Checkbutton", [x in savedata.get("sc") for x, y in HLDConstants.gun_ids], 6, (3,0), HLDConstants.gun_ids),
            ("scUp", "Gun Upgrades", "Checkbutton", [x in savedata.get("scUp") for x, y in HLDConstants.gun_ids], 6, (4,0), HLDConstants.gun_ids)
            ]

        # TODO - loop
        for iname, fieldtext, uitype, value, row_num, grid_pos, const_data in field_specific_data:
            ff = Frame(page)
            ff_label = Label(ff, text=fieldtext)
            ff_editor_objs = []
            for i in range(len(value)):
                if uitype == "OptionMenu":
                    menu_options == [x[1] for x in const_data]
                else:
                    menu_options = None
                obj = EditorUIObj(ff, uitype, const_data[i][1], value[i], menu_options=menu_options)
                ff_editor_objs.append(obj)
                obj.grid(padx=5, column=i//row_num, row=1+(i%row_num), sticky="w")
                self.input_fields.append((iname, obj))
            ff_label.grid(padx=5, column=0, row=0, columnspan=math.ceil(len(value)/row_num), sticky="n")
            ff.grid(column=grid_pos[0], row=grid_pos[1], sticky="n")
            

        # OLD CODE BELOW


        upgrades = Frame(page) # medkit/grenade upgrades
        upgrades_entry = []
        upgrades_label = Label(upgrades, text="Other Upgrades")
        upgrades_labels = []
        for k, v in HLDConstants.misc_upgrade_fields:
            x = Entry(upgrades, width=10)
            x.insert(0, savedata.get(k))
            upgrades_entry.append(x)
            upgrades_labels.append(Label(upgrades, text=v))
            self.input_fields.append((k, x))
        upgrades_label.grid(padx=5, column=0, row=0, columnspan=2)
        for i in range(2):
            upgrades_entry[i].grid(padx=5, column=0, row=1+i, sticky="w")
            upgrades_labels[i].grid(padx=5, column=1, row=1+i, sticky="w")
        upgrades.grid(column=2, row=2, sticky="n")

        # TODO - fix checkbutton not initialising to variable state
        misc_collect = Frame(page) # keys, bits, map
        misc_collect_value = []
        hasmap = IntVar(master=misc_collect, value=savedata.get("hasMap"))
        misc_collect_label = Label(misc_collect, text="Other Values")
        misc_collect_entry = []
        misc_collect_entry_labels = []
        for k, v in HLDConstants.misc_collect_fields:
            x = Entry(misc_collect, width=10)
            x.insert(0, savedata.get(k))
            misc_collect_entry.append(x)
            misc_collect_entry_labels.append(Label(misc_collect, text=v))
            self.input_fields.append((k, x))
        hasmap_cb = Checkbutton(misc_collect, text="Map Collected", variable=hasmap)
        self.input_fields.append(("hasMap", hasmap))
        misc_collect_label.grid(padx=5, column=0, row=0, columnspan=2)
        for i in range(2):
            misc_collect_entry[i].grid(padx=5, column=0, row=1+i, sticky="w")
            misc_collect_entry_labels[i].grid(padx=5, column=1, row=1+i, sticky="w")
        hasmap_cb.grid(column=0, row=3, columnspan=2)
        misc_collect.grid(column=5, row=0, sticky="n")

        gamemode = Frame(page) # NG/Alt/Novice
        gamemode_value = []
        gamemode_label = Label(gamemode, text="Game Mode")
        gamemode_cbs = []
        for k, v in HLDConstants.gamemode_fields:
            x = IntVar(master=gamemode, value=savedata.get(k))
            gamemode_value.append(x)
            gamemode_cbs.append(Checkbutton(gamemode, text=v, variable=x))
            self.input_fields.append((k, x))
        gamemode_label.pack(padx=5, anchor="w")
        for i in range(2):
            gamemode_cbs[i].pack(padx=5, anchor="w")
        gamemode.grid(column=6, row=0, sticky="n")

        modules = Frame(page) # modules
        modulesN = []
        modulesE = []
        modulesS = []
        modulesW = []
        modulesN_cbs = []
        modulesE_cbs = []
        modulesS_cbs = []
        modulesW_cbs = []
        modules_label = Label(modules, text="Modules")
        modulesN_label = Label(modules, text="North")
        modulesE_label = Label(modules, text="East")
        modulesS_label = Label(modules, text="South")
        modulesW_label = Label(modules, text="West")
        for k, v in HLDConstants.north_modules:
            ids = savedata.get("cl").get(6)
            x = IntVar(master=modules, value=k in ids if ids is not None else 0)
            modulesN.append(x)
            modulesN_cbs.append(Checkbutton(modules, text=v, variable=x))
        for k, v in HLDConstants.east_modules:
            ids = savedata.get("cl").get(7)
            x = IntVar(master=modules, value=k in ids if ids is not None else 0)
            modulesE.append(x)
            modulesE_cbs.append(Checkbutton(modules, text=v, variable=x))
        for k, v in HLDConstants.south_modules:
            ids = savedata.get("cl").get(8)
            x = IntVar(master=modules, value=k in ids if ids is not None else 0)
            modulesS.append(x)
            modulesS_cbs.append(Checkbutton(modules, text=v, variable=x))
        for k, v in HLDConstants.west_modules:
            ids = savedata.get("cl").get(9)
            x = IntVar(master=modules, value=k in ids if ids is not None else 0)
            modulesW.append(x)
            modulesW_cbs.append(Checkbutton(modules, text=v, variable=x))
        self.input_fields.append(("modulesN", modulesN))
        self.input_fields.append(("modulesE", modulesE))
        self.input_fields.append(("modulesS", modulesS))
        self.input_fields.append(("modulesW", modulesW))
        modules_label.grid(padx=5, column=0, row=0, columnspan=4)
        modulesN_label.grid(padx=5, column=0, row=1)
        modulesE_label.grid(padx=5, column=1, row=1)
        modulesS_label.grid(padx=5, column=2, row=1)
        modulesW_label.grid(padx=5, column=3, row=1)
        for i in range(8):
            modulesN_cbs[i].grid(padx=5, column=0, row=2+i, sticky="w")
            modulesE_cbs[i].grid(padx=5, column=1, row=2+i, sticky="w")
            modulesS_cbs[i].grid(padx=5, column=2, row=2+i, sticky="w")
            modulesW_cbs[i].grid(padx=5, column=3, row=2+i, sticky="w")
        modules.grid(pady=20, column=0, row=1, columnspan=3, sticky="n")

        tablet = Frame(page) # monoliths
        tablet_value = []
        tablet_cbs = []
        tablet_label = Label(tablet, text="Monoliths")
        tablet_area_labels = [Label(tablet, text=t) for t in ["North", "South", "East", "West"]]
        for k, v in HLDConstants.tablet_ids:
            x = IntVar(master=tablet, value=k in savedata.get("tablet"))
            tablet_value.append(x)
            tablet_cbs.append(Checkbutton(tablet, text=v, variable=x))
        self.input_fields.append(("tablet", tablet_value))
        tablet_label.grid(padx=5, column=0, row=0, columnspan=4)
        for i in range(4):
            tablet_area_labels[i].grid(padx=5, column=i, row=1)
        for i in range(16):
            tablet_cbs[i].grid(padx=5, column=i//4, row=2+(i%4), sticky="w")
        tablet.grid(pady=20, column=3, row=1, columnspan=3, sticky="n")

        outfits = Frame(page) # outfits collected
        outfits_value = []
        outfits_label = Label(outfits, text="Outfits")
        outfits_cbs = []
        for k, v in HLDConstants.outfit_ids:
            x = IntVar(master=outfits, value=k in savedata.get("cShells"))
            outfits_value.append(x)
            outfits_cbs.append(Checkbutton(outfits, text=v, variable=x))
        self.input_fields.append(("cShells", outfits_value))
        self.input_fields.append(("cSwords", outfits_value))
        self.input_fields.append(("cCapes", outfits_value))
        outfits_label.grid(padx=5, column=0, row=0, columnspan=2)
        for i in range(12):
            outfits_cbs[i].grid(padx=5, column=i//6, row=1+(i%6), sticky="w")
        outfits.grid(column=0, row=2, columnspan=2, sticky="n")


    # current state page
    def init_page_2(self, savedata, page):

        cpstate = Frame(page) # scalar state values for current checkpoint
        cpstate_entry = []
        cpstate_label = Label(cpstate, text="Health/Ammo")
        cpstate_entrylabels = []
        for k, v in HLDConstants.cpstate_fields:
            x = Entry(cpstate, width=10)
            x.insert(0, savedata.get(k))
            cpstate_entry.append(x)
            cpstate_entrylabels.append(Label(cpstate, text=v))
            self.input_fields.append((k, x))
        cpstate_label.grid(padx=5, column=0, row=0, columnspan=2)
        for i in range(len(HLDConstants.cpstate_fields)):
            cpstate_entry[i].grid(padx=5, column=0, row=1+i, sticky="w")
            cpstate_entrylabels[i].grid(padx=5, column=1, row=1+i, sticky="w")
        cpstate.grid(column=0, row=0, sticky="n")

        outfit_eq = Frame(page) # currently equipped outfit (NOTE: game crashes when opening outfit equip menu if you don't own the currently equipped outfit. Maybe automatically add outfit to owned when editing this field?)
        outfit_eq_value = []
        outfit_eq_label = Label(outfit_eq, text="Equipped Outfit")
        outfit_eq_dds = []
        outfit_eq_colour_labels = []
        for k, v in HLDConstants.outfit_components:
            x = StringVar(master=outfit_eq, value=HLDConstants.outfit_ids[int(savedata.get(k))][1])
            outfit_eq_value.append(x)
            outfit_eq_dds.append(OptionMenu(outfit_eq, x, *[t[1] for t in HLDConstants.outfit_ids]))
            outfit_eq_colour_labels.append(Label(outfit_eq, text=v))
            self.input_fields.append((k, x))
        outfit_eq_label.grid(padx=5, column=0, row=0, columnspan=2)
        for i in range(3):
            outfit_eq_dds[i].grid(padx=5, column=0, row=1+i, sticky="e")
            outfit_eq_colour_labels[i].grid(padx=5, column=1, row=1+i, sticky="w")
        outfit_eq.grid(column=2, row=0, columnspan=2, sticky="n")


    # misc fields page
    def init_page_3(self, savedata, page):
        pass

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

        self.init_page_1(savedata, collect)
        self.init_page_2(savedata, current)
        self.init_page_3(savedata, misc)


    # copy changes in UI to savedata dict
    def sync_savedata(self):

        lists = {
            "well": HLDConstants.pillar_ids,
            "warp": HLDConstants.area_ids,
            "skill": HLDConstants.skill_ids,
            "sc": HLDConstants.gun_ids,
            "scUp": HLDConstants.gun_ids,
            "cShells": HLDConstants.outfit_ids,
            "cSwords": HLDConstants.outfit_ids,
            "cCapes": HLDConstants.outfit_ids,
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
