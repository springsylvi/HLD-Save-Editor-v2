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
            if filename is None:
                return
            self.editor.load(filename)
            self.init_editor_ui(self.editor)
        except Exception as e:
            showerror(title=type(e), message=e)


    # file -> save
    def save(self, event=None):
        try:
            filename = self.editor.filename
            if filename is None:
                filename = filedialog.asksaveasfilename(initialdir=self.app.savefile_path, defaultextension=".hlds", filetypes=[("HLDS File", "*.hlds")]) # don't ask if user wants to overwrite save
            if filename is None:
                return
            self.editor.save(filename)
        except Exception as e:
            showerror(title=type(e), message=e)


    # file -> save as
    def saveas(self):
        try:
            filename = filedialog.asksaveasfilename(initialdir=self.app.savefile_path, defaultextension=".hlds", filetypes=[("HLDS File", "*.hlds")])
            if filename is None:
                return
            self.editor.save(filename)
        except Exception as e:
            showerror(title=type(e), message=e)

    
    # file -> export
    def export(self, slot):
        try:
            self.editor.export(slot)
        except Exception as e:
            showerror(title=type(e), message=e)


    # options -> import header
    def import_header(self):
        try:
            filename = filedialog.askopenfilename(initialdir=self.app.savefile_path, filetypes=[("Savefile", "*.sav")])
            self.editor.get_header(filename)
        except Exception as e:
            showerror(title=type(e), message=e)
    

    def __init__(self, editor, app):
        self.editor = editor
        self.app = app
        self.tk = Tk(screenName="Editor")
        self.tk.option_add('*tearOff', FALSE)
        
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

        self.tk.bind("<Control-KeyPress-0>", lambda x: self.export(0))
        self.tk.bind("<Control-KeyPress-1>", lambda x: self.export(1))
        self.tk.bind("<Control-KeyPress-2>", lambda x: self.export(2))
        self.tk.bind("<Control-KeyPress-3>", lambda x: self.export(3))
        self.tk.bind("<Control-l>", self.load)
        self.tk.bind("<Control-s>", self.save)
        self.tk.config(menu=self.menu)


    

    # load widgets for editing savedata
    def init_editor_ui(self, editor):

        savedata = editor.savedata

        # main window
        try:
            self.notebook.destroy() # remove old window
        except:
            pass
        self.notebook = ttk.Notebook(self.tk, width=1200, height=600)
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

        # collectable status
        well = Frame(collect)
        wellvalue = [IntVar(master=well, value=x in savedata.get("well")) for x in range(0,4)]
        well_label = Label(well, text="Pillars")
        well_cbs = [Checkbutton(well, text=v, variable=wellvalue[k], command=lambda: self.sync_savedata("well", wellvalue)) for k, v in HLDConstants.pillar_ids]
        well_label.pack(padx=5, anchor="w")
        for cb in well_cbs:
            cb.pack(padx=5, anchor="w")
        well.grid(column=0, row=0, sticky="n")

        warp = Frame(collect)
        warpvalue = [IntVar(master=warp, value=x in savedata.get("warp")) for x in range(5)]
        warp_label = Label(warp, text="Warp Points")
        warp_cbs = [Checkbutton(warp, text=v, variable=warpvalue[k], command=lambda: self.sync_savedata("warp", warpvalue)) for k, v in HLDConstants.area_ids]
        warp_label.pack(padx=5, anchor="w")
        for cb in warp_cbs:
            cb.pack(padx=5, anchor="w")
        warp.grid(column=1, row=0, sticky="n")

        skill = Frame(collect)
        skillvalue = [IntVar(master=skill, value=x in savedata.get("skill")) for x in range(1,7)]
        skill_label = Label(skill, text="Skills")
        skill_cbs = [Checkbutton(skill, text=v, variable=skillvalue[k-1], command=lambda: self.sync_savedata("skill", skillvalue)) for k, v in HLDConstants.skill_ids]
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
            sc_cbs.append(Checkbutton(sc, text=v, variable=x, command=lambda: self.sync_savedata("sc", scvalue)))
            y = IntVar(master=sc, value=k in ids2)
            scupvalue.append(y)
            scup_cbs.append(Checkbutton(sc, text="Upgrade", variable=y, command=lambda: self.sync_savedata("scUp", scupvalue)))
        sc_label.grid(padx=5, column=0, row=0, columnspan=2)
        for i in range(6):
            cb = sc_cbs[i]
            cb.grid(padx=5, column=0, row=i+1, sticky="w")
            cb2 = scup_cbs[i]
            cb2.grid(padx=5, column=1, row=i+1, sticky="w")
        sc.grid(column=3, row=0, sticky="n")

        misc_collect = Frame(collect)
        hasmap, fpsave = [IntVar(master=misc_collect, value=savedata.get(x)) for x in ["hasMap", "fireplaceSave"]]
        print(hasmap.get())
        misc_collect_label = Label(misc_collect, text="Other Values")
        hasmap_cb = Checkbutton(misc_collect, text="Map Collected", variable=hasmap, command=lambda: self.sync_savedata("hasMap", hasmap))
        fpsave_cb = Checkbutton(misc_collect, text="Game Completed", variable=fpsave, command=lambda: self.sync_savedata("fireplaceSave", fpsave))
        misc_collect_label.pack(padx=5, anchor="w")
        hasmap_cb.pack(padx=5, anchor="w")
        fpsave_cb.pack(padx=5, anchor="w")
        misc_collect.grid(column=4, row=0, sticky="n")

        # TODO - fix radiobutton
        char = Frame(collect)
        charvalue = IntVar(master=char, value=(2 if savedata.get("CH") else savedata.get("noviceMode"))) # 0 = normal, 1 = novice, 2 = alt
        char_label = Label(char, text="Character")
        char_alt = Radiobutton(char, text="Alt Drifter", variable=charvalue, value=2, command=lambda: self.sync_savedata("char"))
        char_novice = Radiobutton(char, text="Novice Mode", variable=charvalue, value=1, command=lambda: self.sync_savedata("char"))
        char_ng = Radiobutton(char, text="New Game", variable=charvalue, value=0, command=lambda: self.sync_savedata("char"))
        char_label.pack(padx=5, anchor="w")
        char_alt.pack(padx=5, anchor="w")
        char_novice.pack(padx=5, anchor="w")
        char_ng.pack(padx=5, anchor="w")
        char.grid(column=5, row=0, sticky="n")

        modules = Frame(collect)
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
        for k, v in HLDConstants.north_modules.items():
            ids = savedata.get("cl").get(6)
            x = IntVar(master=modules, value=k in ids if ids is not None else 0)
            modulesN.append(x)
            modulesN_cbs.append(Checkbutton(modules, text=v, variable=x, command=lambda: self.sync_savedata("modules", modulesN)))
        for k, v in HLDConstants.east_modules.items():
            ids = savedata.get("cl").get(7)
            x = IntVar(master=modules, value=k in ids if ids is not None else 0)
            modulesE.append(x)
            modulesE_cbs.append(Checkbutton(modules, text=v, variable=x, command=lambda: self.sync_savedata("modules", modulesE)))
        for k, v in HLDConstants.south_modules.items():
            ids = savedata.get("cl").get(8)
            x = IntVar(master=modules, value=k in ids if ids is not None else 0)
            modulesS.append(x)
            modulesS_cbs.append(Checkbutton(modules, text=v, variable=x, command=lambda: self.sync_savedata("modules", modulesS)))
        for k, v in HLDConstants.west_modules.items():
            ids = savedata.get("cl").get(9)
            x = IntVar(master=modules, value=k in ids if ids is not None else 0)
            modulesW.append(x)
            modulesW_cbs.append(Checkbutton(modules, text=v, variable=x, command=lambda: self.sync_savedata("modules", modulesW)))
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
        modules.grid(column=0, row=1, columnspan=3, sticky="n")

    # copy changes in UI to savedata dict
    def sync_savedata(self, field, value):

        print(field, value.get())
        lists = {
            "well": HLDConstants.pillar_ids,
            "warp": HLDConstants.area_ids,
            "skill": HLDConstants.skill_ids,
            "sc": HLDConstants.gun_ids,
            "scUp": HLDConstants.gun_ids
            }

        if field in lists.keys():
            const_data = lists[field]
            sd = []
            for i in range(len(const_data)):
                if value[i].get():
                    sd.append(const_data[i][0])
            self.editor.savedata.set_field(field, sd)
        elif field in ["hasMap", "fireplaceSave"]:
            self.editor.savedata.set_field(field, float(value.get()))
        elif field == "modules":
            pass
            #TODO
        else:
            print("?")

