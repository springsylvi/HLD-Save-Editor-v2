import os.path
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror
from HLDConstants import HLDConstants

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
            print(filename)
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

        # collectable status page
        well = Frame(collect)
        wellvalue = [IntVar(master=well, value=x in savedata.get("well")) for x in range(0,4)]
        well_label = Label(well, text="Pillars")
        well_cbs = [Checkbutton(well, text=v, variable=wellvalue[k]) for k, v in HLDConstants.pillar_ids]
        self.input_fields.append(("well", wellvalue))
        well_label.pack(padx=5, anchor="w")
        for cb in well_cbs:
            cb.pack(padx=5, anchor="w")
        well.grid(column=0, row=0, sticky="n")

        warp = Frame(collect)
        warpvalue = [IntVar(master=warp, value=x in savedata.get("warp")) for x in range(5)]
        warp_label = Label(warp, text="Warp Points")
        warp_cbs = [Checkbutton(warp, text=v, variable=warpvalue[k]) for k, v in HLDConstants.area_ids]
        self.input_fields.append(("warp", warpvalue))
        warp_label.pack(padx=5, anchor="w")
        for cb in warp_cbs:
            cb.pack(padx=5, anchor="w")
        warp.grid(column=1, row=0, sticky="n")

        skill = Frame(collect)
        skillvalue = [IntVar(master=skill, value=x in savedata.get("skill")) for x in range(1,7)]
        skill_label = Label(skill, text="Skills")
        skill_cbs = [Checkbutton(skill, text=v, variable=skillvalue[k-1]) for k, v in HLDConstants.skill_ids]
        self.input_fields.append(("skill", skillvalue))
        skill_label.grid(padx=5, column=0, row=0, columnspan=2)
        for i in range(6):
            cb = skill_cbs[i]
            cb.grid(padx=5, column=0 if i < 3 else 1, row=(i % 3) + 1, sticky="w")
        skill.grid(column=2, row=0, sticky="n")

        sc = Frame(collect)
        scvalue = []
        sc_cbs = []
        scupvalue = []
        scup_cbs = []
        sc_label = Label(sc, text="Guns + Upgrades")
        for k, v in HLDConstants.gun_ids:
            ids = savedata.get("sc")
            ids2 = savedata.get("scUp")
            x = IntVar(master=sc, value=k in ids)
            scvalue.append(x)
            sc_cbs.append(Checkbutton(sc, text=v, variable=x))
            y = IntVar(master=sc, value=k in ids2)
            scupvalue.append(y)
            scup_cbs.append(Checkbutton(sc, text="Upgrade", variable=y))
        self.input_fields.append(("sc", scvalue))
        self.input_fields.append(("scUp", scupvalue))
        sc_label.grid(padx=5, column=0, row=0, columnspan=2)
        for i in range(6):
            cb = sc_cbs[i]
            cb.grid(padx=5, column=0, row=i+1, sticky="w")
            cb2 = scup_cbs[i]
            cb2.grid(padx=5, column=1, row=i+1, sticky="w")
        sc.grid(column=3, row=0, sticky="n")

        upgrades = Frame(collect) # medkit/grenade upgrades
        upgrades_entry = []
        upgrades_label = Label(upgrades, text="Other Upgrades")
        upgrades_labels = []
        for k, v in HLDConstants.misc_upgrade_fields:
            x = Entry(upgrades) # TODO - make the entry box smaller
            x.insert(0, savedata.get(k))
            upgrades_entry.append(x)
            upgrades_labels.append(Label(upgrades, text=v))
            self.input_fields.append((k, x))
        upgrades_label.grid(padx=5, column=0, row=0, columnspan=2)
        for i in range(2):
            upgrades_entry[i].grid(padx=5, column=0, row=1+i, sticky="w")
            upgrades_labels[i].grid(padx=5, column=1, row=1+i, sticky="w")
        upgrades.grid(column=4, row=0, sticky="n")

        # TODO - fix checkbutton not initialising to variable state
        misc_collect = Frame(collect)
        hasmap, fpsave = [IntVar(master=misc_collect, value=savedata.get("hasMap")), IntVar(master=misc_collect, value=savedata.get("fireplaceSave"))]
        misc_collect_label = Label(misc_collect, text="Other Values")
        hasmap_cb = Checkbutton(misc_collect, text="Map Collected", variable=hasmap)
        fpsave_cb = Checkbutton(misc_collect, text="Game Completed", variable=fpsave)
        self.input_fields.append(("hasMap", hasmap))
        self.input_fields.append(("fireplaceSave", fpsave))
        misc_collect_label.pack(padx=5, anchor="w")
        hasmap_cb.pack(padx=5, anchor="w")
        fpsave_cb.pack(padx=5, anchor="w")
        misc_collect.grid(column=5, row=0, sticky="n")

        # TODO - fix radiobutton
        char = Frame(collect)
        charvalue = IntVar(master=char, value=(2 if savedata.get("CH") else savedata.get("noviceMode"))) # 0 = normal, 1 = novice, 2 = alt
        char_label = Label(char, text="Character")
        char_alt = Radiobutton(char, text="Alt Drifter", variable=charvalue, value=2)
        char_novice = Radiobutton(char, text="Novice Mode", variable=charvalue, value=1)
        char_ng = Radiobutton(char, text="New Game", variable=charvalue, value=0)
        # TODO - append to self.input_fields
        char_label.pack(padx=5, anchor="w")
        char_alt.pack(padx=5, anchor="w")
        char_novice.pack(padx=5, anchor="w")
        char_ng.pack(padx=5, anchor="w")
        char.grid(column=6, row=0, sticky="n")

        modules = Frame(collect) # modules
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

        tablet = Frame(collect) # monoliths
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

        outfits = Frame(collect) # outfits collected
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
        cpstate = Frame(current) # scalar state values for current checkpoint
        cpstate_entry = []
        cpstate_label = Label(cpstate, text="Health/Ammo")
        cpstate_entrylabels = []
        for k, v in HLDConstants.cpstate_fields:
            x = Entry(cpstate)
            x.insert(0, savedata.get(k))
            cpstate_entry.append(x)
            cpstate_entrylabels.append(Label(cpstate, text=v))
            self.input_fields.append((k, x))
        cpstate_label.grid(padx=5, column=0, row=0, columnspan=2)
        for i in range(len(HLDConstants.cpstate_fields)):
            cpstate_entry[i].grid(padx=5, column=0, row=1+i, sticky="w")
            cpstate_entrylabels[i].grid(padx=5, column=1, row=1+i, sticky="w")
        cpstate.grid(column=0, row=0, sticky="n")

        outfit_eq = Frame(current) # currently equipped outfit (NOTE: game crashes when opening outfit equip menu if you don't own the currently equipped outfit. Maybe automatically add outfit to owned when editing this field?)
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
            elif field in ["hasMap", "fireplaceSave", "checkHP", "checkStash", "checkBat", "checkAmmo", "healthUp", "specialUp"]: # single value -> float
                self.editor.savedata.set_field(field, float(obj.get()))
            elif field in ["compShell", "sword", "cape"]: # outfit name -> index
                index = [t[1] for t in HLDConstants.outfit_ids].index(obj.get())
                self.editor.savedata.set_field(field, float(index))
            else:
                print("?")
