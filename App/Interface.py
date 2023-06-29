import os.path, math, platform
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

    # convert a list of FullCBs to a list of id numbers, using a ListMap of the same length with id numbers as keys
    @staticmethod
    def convert_cblist(cblist, ids):
        ret = []
        for i in range(len(cblist)):
            if cblist[i].get():
                ret.append(ids.get_key(ids[i]))
        return ret


class FullDD():
    """
    Tk Optionmenu + related state + Label
    """

    def __init__(self, master, value, options, text):
        self.options = options # listmap of index, string pairs
        self.var = StringVar(master=master, value=value)
        self.dd = OptionMenu(master, self.var, *(options.get_values()))
        self.label = Label(master, text=text)

    # return index for selected value
    def get(self):
        return self.options.get_key(self.var.get())


class FullEntry():
    """
    Tk Entry + Label
    """

    def __init__(self, master, value, text, fieldname):
        valuetype = HLDConstants.display_fields.get(fieldname).get_displaytype()
        if valuetype == "int":
            self.valuetype_func = lambda x: int(x)
        elif valuetype == "float":
            self.valuetype_func = float
        else:
            self.valuetype_func = lambda x: x
        self.entry = Entry(master, width=10)
        self.entry.insert(0, self.valuetype_func(value))
        self.label = Label(master, text=text)
        self.title = text

    def get(self):
        try:
            return self.valuetype_func(self.entry.get())
        except ValueError:
            raise Exception(f"Non-integer value {self.entry.get()} entered into integer field '{self.title}'")

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
            header = self.editor.get_header(filename)
            self.set_status_message(f"local header set to {header}")
        except Exception as e:
            showerror(title=type(e), message=e)


    # set status bar text to message
    def set_status_message(self, message):
        self.sbar_label.config(text=message)

    def __init__(self, editor, app):
        self.editor = editor
        self.app = app
        self.tk = Tk()
        self.tk.title("Editor")
        self.tk.option_add('*tearOff', FALSE)

        self.window = Frame(self.tk, width=500, height=500) # main window
        self.sbar = Frame(self.tk) # status bar
        
        # determine modifier key
        sysname = platform.system()
        if sysname == "Darwin":
            modifier = "Command"
            modifier_display = "Cmd"
        else:
            modifier = "Control"
            modifier_display = "Ctrl"

        # menus
        self.menu = Menu(self.tk)
        self.filemenu = Menu(self.menu)
        self.exportmenu = Menu(self.filemenu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.optionmenu = Menu(self.menu)
        self.menu.add_cascade(label="Options", menu=self.optionmenu)

        self.filemenu.add_command(label="Load", command=self.load, accelerator=f"{modifier_display}+L")
        self.filemenu.add_command(label="Save", command=self.save, accelerator=f"{modifier_display}+S")
        self.filemenu.add_command(label="Save As", command=self.saveas)
        self.filemenu.add_cascade(label="Export", menu=self.exportmenu)
        self.exportmenu.add_command(label="Slot 0", command=lambda: self.export(0), accelerator=f"{modifier_display}+0")
        self.exportmenu.add_command(label="Slot 1", command=lambda: self.export(1), accelerator=f"{modifier_display}+1")
        self.exportmenu.add_command(label="Slot 2", command=lambda: self.export(2), accelerator=f"{modifier_display}+2")
        self.exportmenu.add_command(label="Slot 3", command=lambda: self.export(3), accelerator=f"{modifier_display}+3")

        self.optionmenu.add_command(label="Import Header", command=self.import_header)

        # menu shortcuts
        self.tk.bind(f"<{modifier}-KeyPress-0>", lambda x: self.export(0))
        self.tk.bind(f"<{modifier}-KeyPress-1>", lambda x: self.export(1))
        self.tk.bind(f"<{modifier}-KeyPress-2>", lambda x: self.export(2))
        self.tk.bind(f"<{modifier}-KeyPress-3>", lambda x: self.export(3))
        self.tk.bind(f"<{modifier}-l>", self.load)
        self.tk.bind(f"<{modifier}-s>", self.save)
        self.tk.config(menu=self.menu)

        # status bar
        self.sbar_label = Label(self.sbar)
        self.sbar_label.pack(padx=5, pady=5, side=LEFT)

        self.window.pack()
        self.sbar.pack(side=BOTTOM, fill=X)


        # data stored in display fields; list of (name, object) tuples.
        # type of object depends on display type of field
        self.input_fields = []


    # open a window to choose room by name, write choice into pos_value
    def get_entrance(self, pos_entries):
        top = Toplevel()
        top.title("Entrance Chooser")
        room = IntVar(master=top, value=int(pos_entries[2].get()))
        roomarealabels = [Label(top, text=x) for x in ["Intro + Town", "North", "South", "East", "West", "Abyss + Boss Rush"]]
        for i, label in enumerate(roomarealabels):
            label.grid(column=i, row=1, pady=10)
        print(pos_entries[2].get())
        gridrow = 0
        gridcol = 0

        room_display_column_ids = [79, 124, 165, 205, 253, 273] # last room id of area
        for room_id, (room_iname, room_cname) in HLDConstants.roomNames.items():
            roombutton = Radiobutton(top, text=room_cname, variable=room, value=room_id)
            for i, x in enumerate(room_display_column_ids):
                if room_id <= x: # i has reached correct column
                    if gridcol != i: # start of new column
                        gridcol = i
                        gridrow = 0
                    roombutton.grid(column=gridcol, row=gridrow+2, padx=5)
                    gridrow += 1
                    break
                          
        ok_button = Button(top, text="OK", command=lambda: self.finish_entrance_selection(top, pos_entries, room.get()), width=20)
        ok_button.grid(pady=10, column=0, row=0, columnspan=6)
        

    # close window and write values after selecting entrance
    @staticmethod
    def finish_entrance_selection(win, pos_entries, room_num):
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
        self.notebook.bind("<<NotebookTabChanged>>", lambda x: self.notebook.update_idletasks())
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

        # well
        wellframe = Frame(collect)
        welllabel = Label(wellframe, text="Pillars")
        wellcbs = [FullCB(wellframe, x in savedata.get("well"), HLDConstants.well_ids.get(x)) for x in range(4)]
        welllabel.grid(column=0, row=0)
        for i, x in enumerate(wellcbs):
            x.grid(padx=5, column=0, row=i+1, sticky=W)
        self.input_fields.append(("well", wellcbs))
        wellframe.grid(pady=10, column=0, row=0, sticky=N)
        # warp
        warpframe = Frame(collect)
        warplabel = Label(warpframe, text="Warps")
        warpcbs = [FullCB(warpframe, x in savedata.get("warp"), HLDConstants.area_ids.get(x)) for x in range(5)]
        warplabel.grid(column=0, row=0)
        for i, x in enumerate(warpcbs):
            x.grid(padx=5, column=0, row=i+1, sticky=W)
        self.input_fields.append(("warp", warpcbs))
        warpframe.grid(pady=10, column=1, row=0, sticky=N)
        # skill
        skillframe = Frame(collect)
        skilllabel = Label(skillframe, text="Skills")
        skillcbs = [FullCB(skillframe, x in savedata.get("skill"), HLDConstants.skill_ids.get(x)) for x in range(1,7)]
        skilllabel.grid(column=0, row=0, columnspan=2)
        for i, x in enumerate(skillcbs):
            x.grid(padx=5, column=i//3, row=i%3+1, sticky=W)
        self.input_fields.append(("skill", skillcbs))
        skillframe.grid(pady=10, column=2, row=0, sticky=N)
        # modules
        moduleframe = Frame(collect)
        modulelabel = Label(moduleframe, text="Modules")
        modulearealabels = [Label(moduleframe, text=x) for x in ["North", "South", "East", "West"]]
        northmodulecbs = [FullCB(moduleframe, x in savedata.get_map_value("cl", 6), y) for x,y in HLDConstants.north_modules.get_pairs()]
        southmodulecbs = [FullCB(moduleframe, x in savedata.get_map_value("cl", 8), y) for x,y in HLDConstants.south_modules.get_pairs()]
        eastmodulecbs = [FullCB(moduleframe, x in savedata.get_map_value("cl", 7), y) for x,y in HLDConstants.east_modules.get_pairs()]
        westmodulecbs = [FullCB(moduleframe, x in savedata.get_map_value("cl", 9), y) for x,y in HLDConstants.west_modules.get_pairs()]
        modulelabel.grid(column=0, row=0, columnspan=4)
        for i in range(len(northmodulecbs)):
            northmodulecbs[i].grid(padx=5, column=0, row=i+2, sticky=W)
            southmodulecbs[i].grid(padx=5, column=1, row=i+2, sticky=W)
            eastmodulecbs[i].grid(padx=5, column=2, row=i+2, sticky=W)
            westmodulecbs[i].grid(padx=5, column=3, row=i+2, sticky=W)
        for i in range(len(modulearealabels)):
            modulearealabels[i].grid(padx=5, column=i, row=1)
        self.input_fields.append(("northmodules", northmodulecbs))
        self.input_fields.append(("eastmodules", eastmodulecbs))
        self.input_fields.append(("southmodules", southmodulecbs))
        self.input_fields.append(("westmodules", westmodulecbs))
        moduleframe.grid(pady=10, column=4, row=0, columnspan=4, sticky=N)

        # outfits
        outfitframe = Frame(collect)
        outfitlabel = Label(outfitframe, text="Outfits")
        outfitcbs = [FullCB(outfitframe, x in savedata.get("cShells"), y) for x,y in HLDConstants.outfit_ids.get_pairs()]
        outfitlabel.grid(column=0, row=0, columnspan=2)
        for i, x in enumerate(outfitcbs):
            x.grid(padx=5, column=i//6, row=i%6+1, sticky=W)
        self.input_fields.append(("outfits", outfitcbs))
        outfitframe.grid(pady=10, column=0, row=1, columnspan=2, sticky=N)
        # sc + scUp
        scframe = Frame(collect)
        sclabel = Label(scframe, text="Guns + Upgrades")
        sccbs = [FullCB(scframe, x in savedata.get("sc"), y) for x,y in HLDConstants.gun_ids.get_pairs()]
        scupcbs = [FullCB(scframe, x in savedata.get("scUp"), y + " Upgrade") for x,y in HLDConstants.gun_ids.get_pairs()]
        sclabel.grid(column=0, row=0, columnspan=2)
        for i, x in enumerate(sccbs):
            x.grid(padx=5, column=0, row=i+1, sticky=W)
            scupcbs[i].grid(padx=5, column=1, row=i+1, sticky=W)
        self.input_fields.append(("sc", sccbs))
        self.input_fields.append(("scUp", scupcbs))
        scframe.grid(pady=10, column=2, row=1, columnspan=2, sticky=N)
        # monoliths
        tabletframe = Frame(collect)
        tabletlabel = Label(tabletframe, text="Monoliths")
        tabletarealabels = [Label(tabletframe, text=x) for x in ["North", "South", "East", "West"]]
        tabletcbs = [FullCB(tabletframe, x in savedata.get("tablet"), y) for x,y in HLDConstants.tablet_ids.get_pairs()]
        tabletlabel.grid(column=0, row=0, columnspan=4)
        for i, x in enumerate(tabletcbs):
            x.grid(padx=5, column=i//4, row=i%4+2, sticky=W)
        for i, x in enumerate(tabletarealabels):
            x.grid(padx=5, column=i, row=1)
        self.input_fields.append(("tablet", tabletcbs))
        tabletframe.grid(pady=10, column=4, row=1, columnspan=4, sticky=N)

        # upgrades
        upgradesframe = Frame(collect)
        upgradesfields = ["healthUp", "specialUp"]
        upgradeslabel = Label(upgradesframe, text="Upgrades")
        upgradesentries = [FullEntry(upgradesframe, savedata.get(x), HLDConstants.display_fields.get(x).get_title(), x) for x in upgradesfields]
        upgradeslabel.grid(column=0, row=0, columnspan=2)
        for i, x in enumerate(upgradesentries):
            x.entry.grid(padx=5, column=0, row=i+1, sticky=W)
            x.label.grid(padx=5, column=1, row=i+1, sticky=W)
            self.input_fields.append((upgradesfields[i], x))
        upgradesframe.grid(pady=10, column=0, row=2, columnspan=2, sticky=N)
        # misc_collect
        misccollectframe = Frame(collect)
        misccollectfields = ["gear", "drifterkey"]
        misccollectlabel = Label(misccollectframe, text="Other Collectables")
        misccollectentries = [FullEntry(misccollectframe, savedata.get(x), HLDConstants.display_fields.get(x).get_title(), x) for x in misccollectfields]
        misccollectlabel.grid(column=0, row=0, columnspan=2)
        for i, x in enumerate(misccollectentries):
            x.entry.grid(padx=5, column=0, row=i+1, sticky=W)
            x.label.grid(padx=5, column=1, row=i+1, sticky=W)
            self.input_fields.append((misccollectfields[i], x))
        misccollectframe.grid(pady=10, column=2, row=2, columnspan=2, sticky=N)

        # equipped outfit
        outfiteqframe = Frame(current)
        outfiteqfields = ["sword", "cape", "compShell"]
        outfiteqlabel = Label(outfiteqframe, text="Equipped Outfit")
        outfiteqdds = [FullDD(outfiteqframe, HLDConstants.outfit_ids.get(savedata.get(x)), HLDConstants.outfit_ids, HLDConstants.display_fields.get(x).get_title()) for x in outfiteqfields]
        outfiteqlabel.grid(column=0, row=0, columnspan=2)
        for i, x in enumerate(outfiteqdds):
            x.dd.grid(column=0, row=1+i, sticky=E)
            x.label.grid(column=1, row=1+i, sticky=W)
            self.input_fields.append((outfiteqfields[i], x))
        outfiteqframe.grid(pady=10, column=0, row=0, columnspan=2, sticky=N)
        # equipped guns
        sceqframe = Frame(current)
        sceqfields = ["eq00", "eq01"]
        sceqlabel = Label(sceqframe, text="Equipped Guns")
        sceqdds = [FullDD(sceqframe, HLDConstants.gun_ids.get(savedata.get(x)), HLDConstants.gun_ids, HLDConstants.display_fields.get(x).get_title()) for x in sceqfields]
        sceqlabel.grid(column=0, row=0, columnspan=2)
        for i, x in enumerate(sceqdds):
            x.dd.grid(column=0, row=1+i, sticky=E)
            x.label.grid(column=1, row=1+i, sticky=W)
            self.input_fields.append((sceqfields[i], x))
        sceqframe.grid(pady=10, column=2, row=0, columnspan=2, sticky=N)
        # checkX/checkY/checkRoom + entrance warp
        drifter_pos = Frame(current)
        drifter_posfields = ["checkX", "checkY", "checkRoom"]
        drifter_pos_label = Label(drifter_pos, text="Current Location")
        drifter_pos_label.grid(column=0, row=0, columnspan=2)
        drifter_posentries = [FullEntry(drifter_pos, savedata.get(x), HLDConstants.display_fields.get(x).get_title(), x) for x in drifter_posfields]
        drifter_pos_button = Button(drifter_pos, text="Choose Room", command=lambda: self.get_entrance(drifter_posentries))
        for i, x in enumerate(drifter_posentries):
            x.entry.grid(column=0, row=1+i, sticky=E)
            x.label.grid(column=1, row=1+i, sticky=W)
            self.input_fields.append((drifter_posfields[i], x))
        drifter_pos_button.grid(column=0, row=4, columnspan=2)
        drifter_pos.grid(pady=10, column=0, row=1)
        # drifterstats (health + ammo)
        drifterstatsframe = Frame(current)
        drifterstatsfields = ["checkHP", "checkBat", "checkAmmo", "checkStash"]
        drifterstatslabel = Label(drifterstatsframe, text="Health/Ammo")
        drifterstatsentries = [FullEntry(drifterstatsframe, savedata.get(x), HLDConstants.display_fields.get(x).get_title(), x) for x in drifterstatsfields]
        drifterstatslabel.grid(column=0, row=0, columnspan=2)
        for i, x in enumerate(drifterstatsentries):
            x.entry.grid(padx=5, column=0, row=i+1, sticky=W)
            x.label.grid(padx=5, column=1, row=i+1, sticky=W)
            self.input_fields.append((drifterstatsfields[i], x))
        drifterstatsframe.grid(pady=10, column=2, row=1, sticky=N)

        # bosses
        bossframe = Frame(misc)
        bosslabel = Label(bossframe, text="Bosses Killed")
        bosscbs = [FullCB(bossframe, x in savedata.get("bosses"), y) for x,y in HLDConstants.boss_ids.get_pairs()]
        bosslabel.grid(column=0, row=0)
        for i, x in enumerate(bosscbs):
            x.grid(padx=5, column=0, row=i+1, sticky=W)
        self.input_fields.append(("bosses", bosscbs))
        bossframe.grid(pady=10, column=0, row=0, sticky=N)
        # dog cutscenes
        dogcsframe = Frame(misc)
        dogcslabel = Label(dogcsframe, text="Dog Encounters")
        dogcscbs = [FullCB(dogcsframe, x in savedata.get("noSpawn"), y) for x,y in HLDConstants.nospawn_flags.get_pairs()]
        dogcslabel.grid(column=0, row=0)
        for i, x in enumerate(dogcscbs):
            x.grid(padx=5, column=0, row=i+1, sticky=W)
        self.input_fields.append(("noSpawn", dogcscbs))
        dogcsframe.grid(pady=10, column=1, row=0, sticky=N)
        # cough cutscenes
        coughframe = Frame(misc)
        coughlabel = Label(coughframe, text="Cough Cutscenes")
        coughcbs = [FullCB(coughframe, x in savedata.get("events"), y) for x, y in HLDConstants.cough_cs_flags.get_pairs()]
        coughlabel.grid(column=0, row=0)
        for i, x in enumerate(coughcbs):
            x.grid(padx=5, column=0, row=i+1, sticky=W)
        self.input_fields.append(("coughs", coughcbs))
        coughframe.grid(pady=10, column=2, row=0, sticky=N)
        # terminals
        terminalframe = Frame(misc)
        terminallabel = Label(terminalframe, text="Terminals")
        terminalcbs = [FullCB(terminalframe, x in savedata.get("events"), y) for x, y in HLDConstants.terminal_flags.get_pairs()]
        terminallabel.grid(column=0, row=0, columnspan=3)
        for i, x in enumerate(terminalcbs):
            x.grid(padx=5, column=i//12, row=(i%12)+1, sticky=W)
        self.input_fields.append(("terminals", terminalcbs))
        terminalframe.grid(pady=10, column=3, row=0, columnspan=3, sticky=N)
        # gamemode
        gamemodeframe = Frame(misc)
        gamemodefields = ["CH", "noviceMode"]
        gamemodelabel = Label(gamemodeframe, text="Game Mode")
        gamemodecbs = [FullCB(gamemodeframe, savedata.get(x), HLDConstants.display_fields.get(x).get_title()) for x in gamemodefields]
        gamemodelabel.grid(column=0, row=0, columnspan=2)
        for i, x in enumerate(gamemodecbs):
            x.grid(padx=5, column=0, row=i+1, sticky=W)
            self.input_fields.append((gamemodefields[i], x))
        gamemodeframe.grid(pady=10, column=0, row=1, sticky=N)
        # misc bools
        miscboolsframe = Frame(misc)
        miscboolsfields = ["hasMap", "fireplaceSave"]
        miscboolslabel = Label(miscboolsframe, text="Misc Values 1")
        miscboolscbs = [FullCB(miscboolsframe, savedata.get(x), HLDConstants.display_fields.get(x).get_title()) for x in miscboolsfields]
        miscboolslabel.grid(column=0, row=0, columnspan=2)
        for i, x in enumerate(miscboolscbs):
            x.grid(padx=5, column=0, row=i+1, sticky=W)
            self.input_fields.append((miscboolsfields[i], x))
        miscboolsframe.grid(pady=10, column=1, row=1, sticky=N)
        # misc ints
        miscintsframe = Frame(misc)
        miscintsfields = ["badass", "charDeaths"]
        miscintslabel = Label(miscintsframe, text="Misc Values 2")
        miscintsentries = [FullEntry(miscintsframe, savedata.get(x), HLDConstants.display_fields.get(x).get_title(), x) for x in miscintsfields]
        miscintslabel.grid(column=0, row=0, columnspan=2)
        for i, x in enumerate(miscintsentries):
            x.entry.grid(padx=5, column=0, row=i+1, sticky=W)
            x.label.grid(padx=5, column=1, row=i+1, sticky=W)
            self.input_fields.append((miscintsfields[i], x))
        miscintsframe.grid(pady=10, column=2, row=1, sticky=N)
        # TODO - add values
        # shortcuts
        shortcutframe = Frame(misc)
        shortcutlabel = Label(shortcutframe, text="Other Shortcuts")
        shortcutcbs = [FullCB(shortcutframe, x in savedata.get("permaS"), y) for x, y in HLDConstants.shortcut_permastate_flags.get_pairs()]
        shortcutlabel.grid(column=0, row=0)
        for i, x in enumerate(shortcutcbs):
            x.grid(padx=5, column=0, row=i+1, sticky=W)
        self.input_fields.append(("shortcuts", shortcutcbs))
        shortcutframe.grid(pady=10, column=3, row=1, sticky=N)
        # arenas
        arenaframe = Frame(misc)
        arenalabel = Label(arenaframe, text="Arenas")
        arenacbs = [FullCB(arenaframe, (x in savedata.get("permaS") if x is not None else y in savedata.get("events")), z) for x, y, z in HLDConstants.arena_flags]
        arenalabel.grid(column=0, row=0)
        for i, x in enumerate(arenacbs):
            x.grid(padx=5, column=0, row=i+1, sticky=W)
        self.input_fields.append(("arenas", arenacbs))
        arenaframe.grid(pady=10, column=4, row=1, sticky=N)


    # copy changes in UI to savedata dict
    def sync_savedata(self):

        savedata = self.editor.savedata

        temp_events = [] # build event list across multiple display fields
        temp_permastate = [] # TODO - add uneditable flags directly from savedata (these flags are currently deleted whenever saving a file)

        # TODO - fix bossgearbits

        for field, obj in self.input_fields:
            displayinfo = HLDConstants.display_fields.get(field)
            displaytype = displayinfo.get_displaytype()
            print(field, ":", displaytype)

            if displaytype == "checkboxlist":
                const_data = displayinfo.get_const_data()
                value = FullCB.convert_cblist(obj, const_data)
                print(value)

                if field[-7:] == "modules":
                    # set cl type
                    module_cltypes = {"northmodules" : 6, "eastmodules" : 7, "southmodules" : 8, "westmodules" : 9}
                    savedata.set_map_value("cl", module_cltypes.get(field), value)
                elif field == "outfits":
                    # set all 3 outfit parts
                    for outfit_part in ["cShells", "cSwords", "cCapes"]:
                        savedata.set_field(outfit_part, value)
                elif field in ["coughs", "terminals"]: # TODO - add other event flags
                    # add to events list
                    temp_events += value
                    if field == "terminals":
                        # set corresponding permastate flags
                        for event_id, permastate_id in HLDConstants.terminal_permastate_flags.get_pairs():
                            if event_id in value:
                                temp_permastate.append(permastate_id)
                elif field in ["shortcuts"]:
                    # add to permastate list
                    temp_permastate += value
                else:
                    # set field normally
                    savedata.set_field(field, value)
            elif displaytype in ["int", "float", "dropdown", "checkbox"]:
                value = obj.get()
                print(value)

                if field in ["sword", "cape", "compShell"]:
                    # add equipped outfit to collected outfits (avoids crash when swapping outfits ingame)
                    for outfit_part in ["cShells", "cSwords", "cCapes"]:
                        if value not in savedata.get(outfit_part):
                            savedata.get(outfit_part).append(value)

                if field in ["eq00", "eq01"]:
                    # add equipped weapon to collected weapons
                    if value not in savedata.get("sc"):
                        savedata.get("sc").append(value)

                savedata.set_field(field, value)
            elif field == "bosses":
                value = {}
                for i in range(len(HLDConstants.boss_ids)):
                    boss_id = HLDConstants.boss_ids.get_key_from_index(i)
                    if obj[i].get():
                        boss_coords = savedata.get("bosses").get(boss_id)
                        if boss_coords is None:
                            boss_coords = list(HLDConstants.boss_coords.get(boss_id))
                        value[boss_id] = boss_coords
                print(value)
                savedata.set_field(field, value)
            elif field == "arenas":
                for i, (permastate_id, event_id, x) in enumerate(HLDConstants.arena_flags):
                    if obj[i].get():
                        if permastate_id is not None:
                            temp_permastate.append(permastate_id)
                        if event_id is not None:
                            temp_events.append(event_id)
            else:
                raise Exception(f"sync_savedata not implemented for field {field}")

        savedata.set_field("events", temp_events)
        savedata.set_field("permaS", temp_permastate)
                

