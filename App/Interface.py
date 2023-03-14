from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror

class Interface():
    """
    GUI manager
    """

    # file -> load
    def load(self, event=None):
        try:
            filename = filedialog.askopenfilename(initialdir=self.app.savefile_path)
            self.editor.load(filename)
            self.init_editor_ui(self.editor)
        except Exception as e:
            showerror(title=type(e), message=e)


    # file -> save
    def save(self, event=None):
        try:
            filename = self.editor.filename
            if filename is None:
                filename = filedialog.asksaveasfilename(initialdir=self.app.savefile_path, defaultextension=".hlds", filetypes=[("HLDS File", "*.hlds")])
            self.editor.save(filename)
        except Exception as e:
            showerror(title=type(e), message=e)


    # file -> save as
    def saveas(self):
        try:
            filename = filedialog.asksaveasfilename(initialdir=self.app.savefile_path, defaultextension=".hlds", filetypes=[("HLDS File", "*.hlds")])
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

        # constant values
        north_modules = {
            -1084059: "After Pink Drifter",
            -1047430: "Pillar Room",
            -932471: "Drop Spiral",
            -902212: "Drop Arena",
            -1895481: "Crush Arena",
            -813235: "Cathedral Arena",
            -767783: "Birds",
            -1137428: "Dark Room"
            }
        east_modules = {
            -255100: "Water Tunnel",
            -187905: "Mega Huge Lab",
            -167326: "Flame Room",
            -53392: "After Pillar",
            -118694: "Docks Lab Arena",
            -88709: "Frog Arena",
            -68841: "Big Bog Lab",
            -18778: "Flame Dash Challenge"
            }
        south_modules = {
            -416223: "Mimic",
            -417825: "Scythe",
            -602007: "Pre-Baker 1",
            -596678: "Pre-Baker 2",
            -555279: "Bullet Baker",
            -398635: "Pre-Archer 1",
            -386457: "Pre-Archer 2",
            -676357: "Dash Challenge"
            }
        west_modules = {
            101387: "Bridge Vault",
            185267: "Tanuki Arena",
            206139: "Dogs",
            266784: "Cliffside Cells",
            335443: "Prison Hall",
            353953: "Thin Forest Secret",
            403666: "Meadow Vault",
            435082: "Tanuki Trouble"
            }


        # main window
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
        well_cbE = Checkbutton(well, text="East", variable=wellvalue[0], command=lambda: self.sync_savedata("well"))
        well_cbN = Checkbutton(well, text="North", variable=wellvalue[1], command=lambda: self.sync_savedata("well"))
        well_cbW = Checkbutton(well, text="West", variable=wellvalue[2], command=lambda: self.sync_savedata("well"))
        well_cbS = Checkbutton(well, text="South", variable=wellvalue[3], command=lambda: self.sync_savedata("well"))
        well_label.pack(padx=5, anchor="w")
        well_cbE.pack(padx=5, anchor="w")
        well_cbN.pack(padx=5, anchor="w")
        well_cbW.pack(padx=5, anchor="w")
        well_cbS.pack(padx=5, anchor="w")
        well.grid(column=0, row=0, sticky="n")

        warp = Frame(collect)
        warpvalue = [IntVar(master=warp, value=x in savedata.get("warp")) for x in range(4)]
        warp_label = Label(warp, text="Warp Points")
        warp_cbE = Checkbutton(warp, text="East", variable=warpvalue[0], command=lambda: self.sync_savedata("warp"))
        warp_cbN = Checkbutton(warp, text="North", variable=warpvalue[1], command=lambda: self.sync_savedata("warp"))
        warp_cbW = Checkbutton(warp, text="West", variable=warpvalue[2], command=lambda: self.sync_savedata("warp"))
        warp_cbS = Checkbutton(warp, text="South", variable=warpvalue[3], command=lambda: self.sync_savedata("warp"))
        warp_label.pack(padx=5, anchor="w")
        warp_cbE.pack(padx=5, anchor="w")
        warp_cbN.pack(padx=5, anchor="w")
        warp_cbW.pack(padx=5, anchor="w")
        warp_cbS.pack(padx=5, anchor="w")
        warp.grid(column=1, row=0, sticky="n")

        skill = Frame(collect)
        skillvalue = [IntVar(master=skill, value=x in savedata.get("skill")) for x in range(1,7)]
        skill_label = Label(skill, text="Skills")
        skill1 = Checkbutton(skill, text="Charge Slash", variable=skillvalue[0], command=lambda: self.sync_savedata("skill"))
        skill2 = Checkbutton(skill, text="Bullet Deflect", variable=skillvalue[1], command=lambda: self.sync_savedata("skill"))
        skill3 = Checkbutton(skill, text="Phantom Slash", variable=skillvalue[2], command=lambda: self.sync_savedata("skill"))
        skill4 = Checkbutton(skill, text="Chain Dash", variable=skillvalue[3], command=lambda: self.sync_savedata("skill"))
        skill5 = Checkbutton(skill, text="Bullet Shield", variable=skillvalue[4], command=lambda: self.sync_savedata("skill"))
        skill6 = Checkbutton(skill, text="Dash Stab", variable=skillvalue[5], command=lambda: self.sync_savedata("skill"))
        skill_label.grid(padx=5, column=0, row=0, columnspan=2)
        skill1.grid(padx=5, column=0, row=1, sticky="w")
        skill2.grid(padx=5, column=0, row=2, sticky="w")
        skill3.grid(padx=5, column=0, row=3, sticky="w")
        skill4.grid(padx=5, column=1, row=1, sticky="w")
        skill5.grid(padx=5, column=1, row=2, sticky="w")
        skill6.grid(padx=5, column=1, row=3, sticky="w")
        skill.grid(column=2, row=0, sticky="n")

        sc = Frame(collect)
        scvalue = [IntVar(master=sc, value=x in savedata.get("sc")) for x in [1, 2, 21, 21, 41, 43]] # TODO - factor out gun ids/names into loop with const dict
        scupvalue = [IntVar(master=sc, value=x in savedata.get("scUp")) for x in [1, 2, 21, 21, 41, 43]]
        sc_label = Label(sc, text="Guns + Upgrades")
        sc1 = Checkbutton(sc, text="Pistol", variable=scvalue[0], command=lambda: self.sync_savedata("sc"))
        sc2 = Checkbutton(sc, text="Zeliksa", variable=scvalue[1], command=lambda: self.sync_savedata("sc"))
        sc3 = Checkbutton(sc, text="Laser", variable=scvalue[2], command=lambda: self.sync_savedata("sc"))
        sc4 = Checkbutton(sc, text="Railgun", variable=scvalue[3], command=lambda: self.sync_savedata("sc"))
        sc5 = Checkbutton(sc, text="Shotgun", variable=scvalue[4], command=lambda: self.sync_savedata("sc"))
        sc6 = Checkbutton(sc, text="Diamond Shotgun", variable=scvalue[5], command=lambda: self.sync_savedata("sc"))
        scup1 = Checkbutton(sc, text="9 Ammo", variable=scupvalue[0], command=lambda: self.sync_savedata("sc"))
        scup2 = Checkbutton(sc, text="6 Ammo", variable=scupvalue[1], command=lambda: self.sync_savedata("sc"))
        scup3 = Checkbutton(sc, text="6 Ammo", variable=scupvalue[2], command=lambda: self.sync_savedata("sc"))
        scup4 = Checkbutton(sc, text="3 Ammo", variable=scupvalue[3], command=lambda: self.sync_savedata("sc"))
        scup5 = Checkbutton(sc, text="5 Ammo", variable=scupvalue[4], command=lambda: self.sync_savedata("sc"))
        scup6 = Checkbutton(sc, text="4 Ammo", variable=scupvalue[5], command=lambda: self.sync_savedata("sc"))
        sc_label.grid(padx=5, column=0, row=0, columnspan=2)
        sc1.grid(padx=5, column=0, row=1, sticky="w")
        sc2.grid(padx=5, column=0, row=2, sticky="w")
        sc3.grid(padx=5, column=0, row=3, sticky="w")
        sc4.grid(padx=5, column=0, row=4, sticky="w")
        sc5.grid(padx=5, column=0, row=5, sticky="w")
        sc6.grid(padx=5, column=0, row=6, sticky="w")
        scup1.grid(padx=5, column=1, row=1, sticky="w")
        scup2.grid(padx=5, column=1, row=2, sticky="w")
        scup3.grid(padx=5, column=1, row=3, sticky="w")
        scup4.grid(padx=5, column=1, row=4, sticky="w")
        scup5.grid(padx=5, column=1, row=5, sticky="w")
        scup6.grid(padx=5, column=1, row=6, sticky="w")
        sc.grid(column=3, row=0, sticky="n")

        misc_collect = Frame(collect)
        hasmap, fpsave = [IntVar(master=misc_collect, value=savedata.get(x)) for x in ["hasMap", "fireplaceSave"]]
        misc_collect_label = Label(misc_collect, text="Other Values")
        hasmap_cb = Checkbutton(misc_collect, text="Map Collected", variable=hasmap, command=lambda: self.sync_savedata("misc_collect"))
        fpsave_cb = Checkbutton(misc_collect, text="Game Completed", variable=fpsave, command=lambda: self.sync_savedata("misc_collect"))
        misc_collect_label.pack(padx=5, anchor="w")
        hasmap_cb.pack(padx=5, anchor="w")
        fpsave_cb.pack(padx=5, anchor="w")
        misc_collect.grid(column=4, row=0, sticky="n")

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
        for k, v in north_modules.items():
            ids = savedata.get("cl").get(6)
            x = IntVar(master=modules, value=k in ids if ids is not None else 0)
            modulesN.append(x)
            modulesN_cbs.append(Checkbutton(modules, text=v, variable=x, command=lambda: self.sync_savedata("modules")))
        for k, v in east_modules.items():
            ids = savedata.get("cl").get(7)
            x = IntVar(master=modules, value=k in ids if ids is not None else 0)
            modulesE.append(x)
            modulesE_cbs.append(Checkbutton(modules, text=v, variable=x, command=lambda: self.sync_savedata("modules")))
        for k, v in south_modules.items():
            ids = savedata.get("cl").get(8)
            x = IntVar(master=modules, value=k in ids if ids is not None else 0)
            modulesS.append(x)
            modulesS_cbs.append(Checkbutton(modules, text=v, variable=x, command=lambda: self.sync_savedata("modules")))
        for k, v in west_modules.items():
            ids = savedata.get("cl").get(9)
            x = IntVar(master=modules, value=k in ids if ids is not None else 0)
            modulesW.append(x)
            modulesW_cbs.append(Checkbutton(modules, text=v, variable=x, command=lambda: self.sync_savedata("modules")))
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
    def sync_savedata(self, field):
        match field:
            case "well":
                print("well")
                # TODO
            case "warp":
                print("warp")
                # TODO
            case _:
                print("?")

