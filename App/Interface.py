import os.path
import math
import platform
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
        

    # convert a list of FullCBs to a list of id numbers, using a ListMap of the same length with id numbers as keys
    def convert_cblist(cblist, ids):
        ret = []
        for i in range(len(cblist)):
            if cblist[i].get():
                ret.append(ids.get_key(ids[i]))
        return ret


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
        warpframe = Frame(collect)
        warplabel = Label(warpframe, text="Warps")
        warpcbs = [FullCB(warpframe, x in savedata.get("warp"), HLDConstants.area_ids.get(x)) for x in range(5)]
        warplabel.grid(column=0, row=0)
        for i in range(len(warpcbs)):
            warpcbs[i].grid(padx=5, column=0, row=i+1, sticky=W)
        self.input_fields.append(("warp", warpcbs))
        warpframe.grid(pady=10, column=1, row=0, sticky=N)
        # skill
        skillframe = Frame(collect)
        skilllabel = Label(skillframe, text="Skills")
        skillcbs = [FullCB(skillframe, x in savedata.get("skill"), HLDConstants.skill_ids.get(x)) for x in range(1,7)]
        skilllabel.grid(column=0, row=0, columnspan=2)
        for i in range(len(skillcbs)):
            skillcbs[i].grid(padx=5, column=i//3, row=i%3+1, sticky=W)
        self.input_fields.append(("skill", skillcbs))
        skillframe.grid(pady=10, column=2, row=0, sticky=N)
        # modules
        moduleframe = Frame(collect)
        modulelabel = Label(moduleframe, text="Modules")
        northmodulecbs = [FullCB(moduleframe, x in savedata.get("cl").get(6), y) for x,y in HLDConstants.north_modules.get_pairs()]
        eastmodulecbs = [FullCB(moduleframe, x in savedata.get("cl").get(7), y) for x,y in HLDConstants.east_modules.get_pairs()]
        southmodulecbs = [FullCB(moduleframe, x in savedata.get("cl").get(8), y) for x,y in HLDConstants.south_modules.get_pairs()]
        westmodulecbs = [FullCB(moduleframe, x in savedata.get("cl").get(9), y) for x,y in HLDConstants.west_modules.get_pairs()]
        # TODO -  add area labels
        modulelabel.grid(column=0, row=0, columnspan=4)
        for i in range(len(northmodulecbs)):
            northmodulecbs[i].grid(padx=5, column=0, row=i+1, sticky=W)
            eastmodulecbs[i].grid(padx=5, column=1, row=i+1, sticky=W)
            southmodulecbs[i].grid(padx=5, column=2, row=i+1, sticky=W)
            westmodulecbs[i].grid(padx=5, column=3, row=i+1, sticky=W)
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
        for i in range(len(outfitcbs)):
            outfitcbs[i].grid(padx=5, column=i//6, row=i%6+1, sticky=W)
        self.input_fields.append(("outfits", outfitcbs))
        outfitframe.grid(pady=10, column=0, row=1, columnspan=2, sticky=N)
        # sc + scUp
        scframe = Frame(collect)
        sclabel = Label(scframe, text="Guns + Upgrades")
        sccbs = [FullCB(scframe, x in savedata.get("sc"), y) for x,y in HLDConstants.gun_ids.get_pairs()]
        scupcbs = [FullCB(scframe, x in savedata.get("scUp"), y + " Upgrade") for x,y in HLDConstants.gun_ids.get_pairs()]
        sclabel.grid(column=0, row=0, columnspan=2)
        for i in range(len(sccbs)):
            sccbs[i].grid(padx=5, column=0, row=i+1, sticky=W)
            scupcbs[i].grid(padx=5, column=1, row=i+1, sticky=W)
        self.input_fields.append(("sc", sccbs))
        self.input_fields.append(("scUp", scupcbs))
        scframe.grid(pady=10, column=2, row=1, columnspan=2, sticky=N)
        # monoliths
        tabletframe = Frame(collect)
        tabletlabel = Label(tabletframe, text="Monoliths")
        tabletcbs = [FullCB(tabletframe, x in savedata.get("tablet"), y) for x,y in HLDConstants.tablet_ids.get_pairs()]
        tabletlabel.grid(column=0, row=0, columnspan=4)
        for i in range(len(tabletcbs)):
            tabletcbs[i].grid(padx=5, column=i//4, row=i%4+1, sticky=W)
        self.input_fields.append(("tablet", tabletcbs))
        tabletframe.grid(pady=10, column=4, row=1, columnspan=4, sticky=N)

        # upgrades
        upgradesframe = Frame(collect)
        upgradesfields = ["healthUp", "specialUp"]
        upgradeslabel = Label(upgradesframe, text="Upgrades")
        upgradesentries = [FullEntry(upgradesframe, savedata.get(x), HLDConstants.display_fields.get(x).get_title(), "int") for x in upgradesfields]
        upgradeslabel.grid(column=0, row=0, columnspan=2)
        for i in range(len(upgradesfields)):
            upgradesentries[i].entry.grid(padx=5, column=0, row=i+1, sticky=W)
            upgradesentries[i].label.grid(padx=5, column=1, row=i+1, sticky=W)
            self.input_fields.append((upgradesfields[i], upgradesentries[i]))
        upgradesframe.grid(pady=10, column=0, row=2, columnspan=2, sticky=N)
        # misc_collect
        misccollectframe = Frame(collect)
        misccollectfields = ["gear", "drifterkey"]
        misccollectlabel = Label(misccollectframe, text="Other Collectables")
        misccollectentries = [FullEntry(misccollectframe, savedata.get(x), HLDConstants.display_fields.get(x).get_title(), "int") for x in misccollectfields]
        misccollectlabel.grid(column=0, row=0, columnspan=2)
        for i in range(len(misccollectfields)):
            misccollectentries[i].entry.grid(padx=5, column=0, row=i+1, sticky=W)
            misccollectentries[i].label.grid(padx=5, column=1, row=i+1, sticky=W)
            self.input_fields.append((misccollectfields[i], misccollectentries[i]))
        misccollectframe.grid(pady=10, column=2, row=2, columnspan=2, sticky=N)

        # equipped outfit
        outfiteqframe = Frame(current)
        outfiteqfields = ["sword", "cape", "compShell"]
        outfiteqlabel = Label(outfiteqframe, text="Equipped Outfit")
        outfiteqdds = [FullDD(outfiteqframe, HLDConstants.outfit_ids.get(savedata.get(x)), HLDConstants.outfit_ids, HLDConstants.display_fields.get(x).get_title()) for x in outfiteqfields]
        outfiteqlabel.grid(column=0, row=0, columnspan=2)
        for i in range(len(outfiteqdds)):
            outfiteqdds[i].dd.grid(column=0, row=1+i, sticky=E)
            outfiteqdds[i].label.grid(column=1, row=1+i, sticky=W)
            self.input_fields.append((outfiteqfields[i], outfiteqdds[i]))
        outfiteqframe.grid(pady=10, column=0, row=0, columnspan=2, sticky=N)

        # gamemode
        gamemodeframe = Frame(misc)
        gamemodefields = ["CH", "noviceMode"]
        gamemodelabel = Label(gamemodeframe, text="Game Mode")
        gamemodecbs = [FullCB(gamemodeframe, savedata.get(x), HLDConstants.display_fields.get(x).get_title()) for x in gamemodefields]
        gamemodelabel.grid(column=0, row=0, columnspan=2)
        for i in range(len(gamemodefields)):
            gamemodecbs[i].grid(padx=5, column=0, row=i+1, sticky=W)
            self.input_fields.append((gamemodefields[i], gamemodecbs[i]))
        gamemodeframe.grid(pady=10, column=0, row=0, sticky=N)
        # misc_values
        miscboolsframe = Frame(misc)
        miscboolsfields = ["hasMap", "fireplaceSave"]
        miscboolslabel = Label(miscboolsframe, text="Misc Values")
        miscboolscbs = [FullCB(miscboolsframe, savedata.get(x), HLDConstants.display_fields.get(x).get_title()) for x in miscboolsfields]
        miscboolslabel.grid(column=0, row=0, columnspan=2)
        for i in range(len(miscboolsfields)):
            miscboolscbs[i].grid(padx=5, column=0, row=i+1, sticky=W)
            self.input_fields.append((miscboolsfields[i], miscboolscbs[i]))
        miscboolsframe.grid(pady=10, column=1, row=0, sticky=N)
        


        # checkX/checkY/checkRoom + entrance warp
        drifter_pos = Frame(current)
        drifter_posfields = ["checkX", "checkY", "checkRoom"]
        drifter_pos_label = Label(drifter_pos, text="Current Location")
        drifter_pos_label.grid(column=0, row=0, columnspan=2)
        drifter_posentries = [FullEntry(drifter_pos, savedata.get(x), HLDConstants.display_fields.get(x).get_title(), "float") for x in drifter_posfields] # TODO - remove the hardcoded float type once I figure out display types
        drifter_pos_button = Button(drifter_pos, text="Choose Room", command=lambda: self.get_entrance(drifter_posentries))
        for i in range(len(drifter_posentries)):
            drifter_posentries[i].entry.grid(column=0, row=1+i, sticky=E)
            drifter_posentries[i].label.grid(column=1, row=1+i, sticky=W)
            self.input_fields.append((drifter_posfields[i], drifter_posentries[i]))
        drifter_pos_button.grid(column=0, row=4, columnspan=2)
        drifter_pos.grid(pady=10, column=0, row=1)
            

    # copy changes in UI to savedata dict
    def sync_savedata(self):

        # TODO - reimplement this function to work with new init_editor_ui version
        # for each element of input_fields, look up name in HLDConstants.display_fields and call get method on that display type to pull raw data from tk obj
        for field, obj in self.input_fields:
            displayinfo = HLDConstants.display_fields.get(field)
            displaytype = displayinfo.get_displaytype()
            print(field, ":", displaytype)

            if displaytype == "checkboxlist":
                const_data = displayinfo.get_const_data()
                value = Interface.convert_cblist(obj, const_data)
                print(value)

                if field[-7:] == "modules":
                    # set cl type
                    module_cltypes = {"northmodules" : 6, "eastmodules" : 7, "southmodules" : 8, "westmodules" : 9}
                    self.editor.savedata.set_map_value("cl", module_cltypes.get(field), value)
                elif field == "outfits":
                    # set all 3 outfit parts
                    for outfit_part in ["cShells", "cSwords", "cCapes"]:
                        self.editor.savedata.set_field(outfit_part, value)
                else:
                    # set field normally
                    self.editor.savedata.set_field(field, value)
            elif displaytype in ["int", "float", "dropdown", "checkbox"]:
                value = obj.get()
                print(value)

                self.editor.savedata.set_field(field, value)
            else:
                print("unknown display type")

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
