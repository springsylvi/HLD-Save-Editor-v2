import os.path
import math
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror
from HLDConstants import HLDConstants


class FullCB():
    """
    Tk Checkbutton + IntVar
    """

    def __init__(self, master, value, text):
        self.var = IntVar(value=int(value))
        self.cb = Checkbutton(master=master, text=text, variable=self.var)

    def get(self):
        return self.var.get()

    def pack(self, **kw):
        self.cb.pack(**kw)

    def grid(self, **kw):
        self.cb.grid(**kw)


class FullEntry():
    """
    Tk Entry + Label
    """

    def __init__(self, master, value, text, valuetype):
        if valuetype == "int":
            self.valuetype_func = lambda x: int(float(x))
        elif valuetype == "float":
            self.valuetype_func = float
        else:
            self.valuetype_func = lambda x: x
        self.entry = Entry(master, width=10)
        self.entry.insert(0, self.valuetype_func(value))
        self.label = Label(master, text=text)

    def get(self):
        return self.valuetype_func(self.entry.get())

    def set_value(self, value):
        self.entry.delete(0, END)
        self.entry.insert(0, self.valuetype_func(value))


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


        # data stored in display fields; list of (name, object) tuples.
        # type of object depends on display type of field
        self.input_fields = []


    # open a window to choose room by name, write choice into pos_value # TODO - add entrance choosing too
    def get_entrance(self, pos_entries):
        top = Toplevel(self.tk)
        top.title("Entrance Chooser")
        room = IntVar(master=top, value=int(float(pos_entries[2].get()))) # TODO - remove this typescasting after figuring out display types
        print(pos_entries[2].get())
        i = 0
        for room_id, (room_iname, room_cname) in HLDConstants.roomNames.items():
            x = Radiobutton(top, text=room_cname, variable=room, value=room_id)
            x.grid(column=i//31, row=i%31)
            i = i+1
        ok_button = Button(top, text="OK", command=lambda: self.finish_entrance_selection(top, pos_entries, room.get()), width=20)
        ok_button.grid(pady=10, column=0, row=31, columnspan=6)
        

    # close window and write values after selecting entrance
    def finish_entrance_selection(self, win, pos_entries, room_num):
        pos_entries[0].set_value(-10.0)
        pos_entries[1].set_value(-10.0)
        pos_entries[2].set_value(room_num)
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

        #TODO - rewrite all of the rest of this func
        # iterate over displaydata list from editor, handle all special cases (this will be messy, can maybe clean up later?)
        # populate input_fields (need .get() to work on all values)

        # TODO - create UI elements for checkboxlists

        # well
        wellframe = Frame(collect)
        welllabel = Label(wellframe, text="Pillars")
        wellcbs = [FullCB(wellframe, x in savedata.get("well"), HLDConstants.well_ids.get(x)) for x in range(4)]
        welllabel.grid(column=0, row=0)
        for i in range(len(wellcbs)):
            wellcbs[i].grid(padx=5, column=0, row=i+1, sticky=W)
        self.input_fields.append(("well", wellcbs))
        wellframe.grid(pady=10, column=0, row=0, sticky=N)
        # warp
        # skill
        # modules

        # sc + scUp
        # outfits
        # monoliths

        # upgrades
        upgradesframe = Frame(collect)
        upgradesfields = ["healthUp", "specialUp"]
        upgradeslabel = Label(upgradesframe, text="Upgrades")
        upgradescbs = [FullCB(upgradesframe, savedata.get(x), HLDConstants.display_fields.get(x).get_title()) for x in upgradesfields]
        upgradeslabel.grid(column=0, row=0)
        for i in range(len(upgradesfields)):
            upgradescbs[i].grid(padx=5, column=0, row=i+1, sticky=W)
            self.input_fields.append((upgradesfields[i], upgradescbs[i]))
        upgradesframe.grid(pady=10, column=2, row=2, sticky=N)
        # misc_collect

        # gamemode
        gamemodeframe = Frame(misc)
        # misc_values


        # checkX/checkY/checkRoom + entrance warp
        drifter_pos = Frame(current)
        drifter_posfields = ["checkX", "checkY", "checkRoom"]
        drifter_pos_label = Label(drifter_pos, text="Current Location")
        drifter_pos_label.grid(column=0, row=0)
        drifter_posentries = [FullEntry(drifter_pos, savedata.get(x), HLDConstants.display_fields.get(x).get_title(), "float") for x in drifter_posfields] # TODO - remove the hardcoded float type once I figure out display types
        drifter_pos_button = Button(drifter_pos, text="Choose Room", command=lambda: self.get_entrance(drifter_posentries))
        for i in range(len(drifter_posentries)):
            drifter_posentries[i].entry.grid(column=0, row=1+i, sticky=E)
            drifter_posentries[i].label.grid(column=1, row=1+i, sticky=W)
        drifter_pos_button.grid(column=0, row=4, columnspan=2)
        drifter_pos.grid(pady=10, column=0, row=1)
            

    # copy changes in UI to savedata dict
    def sync_savedata(self):

        # TODO - reimplement this function to work with new init_editor_ui version
        # for each element of input_fields, look up name in HLDConstants.display_fields and call get method on that display type to pull raw data from tk obj

        for field, obj in self.input_fields:
            displayinfo = HLDConstants.display_fields.get("field")[1]
            displaytype = displayinfo.get_displaytype()
            if displaytype == ? # TODO - figure out what types displaytype needs to represent (use paper!) 

        """
        lists = {
            "well": HLDConstants.well_ids,
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
        """
