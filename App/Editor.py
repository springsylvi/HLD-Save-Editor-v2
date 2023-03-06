from json import loads, dumps
import base64
from os.path import splitext
import datetime


class Savedata():
    """
    Contains savedata as a dictionary.
    """

    # all valid fields and their types.
    # types are a sequence of any of str, num, list, map.
    # list takes 1 arg, map takes 2
    fields = {"badass": ["num"],
              "bosses": ["map", "num", "list", "num"],
              "bossGearbits": ["list", "str"],
              "cape": ["num"],
              "cCapes": ["list", "num"],
              "CH": ["num"],
              "charDeaths": ["num"],
              "checkAmmo": ["num"],
              "checkBat": ["num"],
              "checkCID": ["num"],
              "checkHP": ["num"],
              "checkRoom": ["num"],
              "checkStash": ["num"],
              "checkX": ["num"],
              "checkY": ["num"],
              "cl": ["map", "num", "list", "num"],
              "compShell": ["num"],
              "cShells": ["list", "num"],
              "cSwords": ["list", "num"],
              "cues": ["list", "num"],
              "dateTime": ["num"],
              "destruct": ["map", "num", "list", "num"],
              "drifterkey": ["num"],
              "enemies": ["map", "num", "list", "num"],
              "eq00": ["num"],
              "eq01": ["num"],
              "events": ["list", "num"],
              "fireplaceSave": ["num"],
              "gameName": ["str"],
              "gear": ["num"],
              "gearReminderTimes": ["num"],
              "gunReminderTimes": ["num"],
              "halluc": ["num"],
              "hasMap": ["num"],
              "healthKits": ["list", "num"],
              "healthUp": ["num"],
              "mapMod": ["map", "num", "list", "num"],
              "newcomerHoardeMessageShown": ["num"],
              "noSpawn": ["list", "num"],
              "noviceMode": ["num"],
              "permaS": ["map", "num", "num"],
              "playT": ["num"],
              "rooms": ["list", "num"],
              "sc": ["list", "num"],
              "scUp": ["list", "num"],
              "scK": ["map", "num", "num"],
              "skill": ["list", "num"],
              "specialUp": ["num"],
              "successfulCollectTimes": ["num"],
              "successfulHealTimes": ["num"],
              "successfulWarpTimes": ["num"],
              "sword": ["num"],
              "tablet": ["list", "num"],
              "tutHeal": ["num"],
              "values": ["map", "str", "num"],
              "warp": ["list", "num"],
              "well": ["list", "num"],
              "wellMap": ["list", "num"]}

    def __init__(self, data):
        self.savedata_map = data

    def get_field(self, field):
        return self.savedata_map.get(field)

    def set_field(self, field, value):
        if (field in fields):
            self.savedata_map[field] = value

    # parse data from .hlds file
    def parse_hlds(hldsdata):
        savedata_map = {1:2} #placeholder
        # TODO - parse hlds
        return savedata_map

    # save data to .hlds file
    def save_hlds(filename):
        pass
        # TODO - save hlds

    # parse data from .sav file
    def parse_savefile(jsondata):
        savedata_map = loads(jsondata)
        # parse list/map structures
        for key, value in savedata_map.items():
            fieldtype = Savedata.fields[key]
            if len(fieldtype) > 1:
                savedata_map[key] = Savedata.parse_savedata_collection(value, fieldtype)
        # handle special cases
        try:
            # bossGearbit format is "G(room_id)(boss_instance_id)(bit_num)"
            savedata_map["bossGearbits"] = [[int(x[1:4]), int(x[4:-1]), int(x[-1])] for x in savedata_map["bossGearbits"]] # TODO -  add support for non 3-digit room numbers
        except:
            pass
        # TODO - dateTime?
        print(savedata_map)
        return savedata_map

    # export data to .sav file
    def export_savefile(filename):
        pass


    # convert list/map in savedata format to list/map object
    def parse_savedata_collection(raw, fieldtype):
        if fieldtype[0] == "list":
            if "&" in raw:
                sep = "&"
            else:
                sep = "+"
            list_obj = raw.split(sep)[:-1]
            if fieldtype[1] == "num":
                list_obj = [float(x) for x in list_obj]
            return list_obj
        if fieldtype[0] == "map":
            raw = raw.replace("'", "") # picking up keys sometimes creates stray ' characters
            map_obj = {x.split("=")[0] : x.split("=")[1] for x in raw.split(">")[:-1]}
            if fieldtype[1] == "num":
                map_obj = {float(a) : b for a, b in map_obj.items()}
            if fieldtype[2] == "num":
                map_obj = {a : float(b) for a, b in map_obj.items()}
            if fieldtype[2] == "list":
                map_obj = {a : Savedata.parse_savedata_collection(b, fieldtype[2:4]) for a, b in map_obj.items()}
            return map_obj


class Editor():
    """
    Utilities for loading, editing and saving files.

    Editor instance created on startup, contains the currently loaded Savedata instance.
    """

    def __init__(self, savefile_path):
        self.path = savefile_path
        self.filename = None # name of loaded .hlds file
        self.savedata = None

    def load(self, filename):
        ext = splitext(filename)[1]
        if ext == ".hlds":
            savefile = open(filename, "rt")
            self.savedata = Savedata(Savedata.parse_hlds(savefile.read()))
            self.filename = filename
        elif ext == ".sav":
            savefile = open(filename, "rb", buffering=0)
            jsondata = base64.standard_b64decode(savefile.read())[60:-1].decode()
            self.savedata = Savedata(Savedata.parse_savefile(jsondata))
        elif ext == "":
            return
        else:
            raise FileNotFoundError("Invald file type")
        

    def save(self, filename=None):
        savefile = open(filename, "wt")
        # TODO - write hlds

    def export(self, slot):
        print(slot)
        # TODO

    def __str__(self):
        if self.savedata:
            return self.savedata
        else:
            return "No save loaded."

