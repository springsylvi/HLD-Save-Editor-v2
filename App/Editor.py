from json import loads, dumps
import base64
from os.path import splitext, join
import datetime
import configparser


class Savedata():
    """
    Contains savedata as a dictionary.
    """

    # all valid fields and their types.
    # types are a sequence of any of str, int, float, list, map.
    # list takes 1 arg, map takes 2
    fields = {"badass": ["float"],
              "bosses": ["map", "int", "list", "int"],
              "bossGearbits": ["list", "str"],
              "cape": ["float"],
              "cCapes": ["list", "int"],
              "CH": ["float"],
              "charDeaths": ["float"],
              "checkAmmo": ["float"],
              "checkBat": ["float"],
              "checkCID": ["float"],
              "checkHP": ["float"],
              "checkRoom": ["float"],
              "checkStash": ["float"],
              "checkX": ["float"],
              "checkY": ["float"],
              "cl": ["map", "int", "list", "int"],
              "compShell": ["float"],
              "cShells": ["list", "int"],
              "cSwords": ["list", "int"],
              "cues": ["list", "int"],
              "dateTime": ["float"],
              "destruct": ["map", "int", "list", "float"],
              "drifterkey": ["float"],
              "enemies": ["map", "int", "list", "float"], # TODO - list contains multiple types (int, float, str), needs to handle special case
              "eq00": ["float"],
              "eq01": ["float"],
              "events": ["list", "int"],
              "fireplaceSave": ["float"],
              "gameName": ["str"],
              "gear": ["float"],
              "gearReminderTimes": ["float"],
              "gunReminderTimes": ["float"],
              "halluc": ["float"],
              "hasMap": ["float"],
              "healthKits": ["list", "int"],
              "healthUp": ["float"],
              "mapMod": ["map", "int", "list", "int"],
              "newcomerHoardeMessageShown": ["float"],
              "noSpawn": ["list", "int"],
              "noviceMode": ["float"],
              "permaS": ["map", "int", "int"],
              "playT": ["float"],
              "rooms": ["list", "int"],
              "sc": ["list", "int"],
              "scUp": ["list", "int"],
              "scK": ["map", "int", "int"],
              "skill": ["list", "int"],
              "specialUp": ["float"],
              "successfulCollectTimes": ["float"],
              "successfulHealTimes": ["float"],
              "successfulWarpTimes": ["float"],
              "sword": ["float"],
              "tablet": ["list", "int"],
              "tutHeal": ["float"],
              "values": ["map", "str", "int"],
              "warp": ["list", "int"],
              "well": ["list", "int"],
              "wellMap": ["list", "int"]}

    def __init__(self, data):
        self.savedata_map = data

    def get(self, field):
        return self.savedata_map.get(field)

    def set_field(self, field, value):
        if (field in Savedata.fields):
            self.savedata_map[field] = value
        else:
            raise Exception("Invalid field name")

    # set an element of a map object
    def set_map_value(self, field, key, value):
        if (field in Savedata.fields):
            self.savedata_map[field][key] = value
        else:
            raise Exception("Invalid field name")

    # parse data from .hlds file
    def parse_hlds(hldsdata):
        savedata_map = loads(hldsdata)
        # convert string keys to numbers
        for key, value in savedata_map.items():
            if type(value) == dict:
                new = {}
                for a, b in value.items():
                    try:
                        a = float(a)
                    except:
                        pass
                    new[a] = b
                savedata_map[key] = new
        return savedata_map

    # save data to .hlds file
    def save_hlds(self, hldsfile):
        hlds = dumps(self.savedata_map)
        hldsfile.write(hlds)

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
            savedata_map["bossGearbits"] = [[int(x[1:4]), int(x[4:-1]), int(x[-1])] for x in savedata_map["bossGearbits"]]
            # TODO - add support for non 3-digit room numbers
        except:
            pass
        # TODO - dateTime?
        return savedata_map

    # export data to .sav file
    def export_savefile(self, savefile, header):
        temp_sdmap = self.savedata_map.copy()
        # handle special cases
        try:
            # bossGearbit format is "G(room_id)(boss_instance_id)(bit_num)"
            temp_sdmap["bossGearbits"] = ["G" + str(x[0]) + str(x[1]) + str(x[2]) for x in self.savedata_map["bossGearbits"]]
        except:
            pass
        # format list/map objects
        for key, value in self.savedata_map.items():
            fieldtype = Savedata.fields[key]
            if len(fieldtype) > 1:
                temp_sdmap[key] = Savedata.export_savedata_collection(value, fieldtype, "+")
        savedata_text = dumps(temp_sdmap) + " "
        savedata_enc = base64.standard_b64encode(header + savedata_text.encode())
        savefile.write(savedata_enc)
        # TODO - cache output?


    # convert list/map in savedata format to list/map object
    # TODO - tidy up this function
    def parse_savedata_collection(raw, fieldtype):
        if fieldtype[0] == "list":
            sep = "&" if "&" in raw else "+"
            list_obj = raw.split(sep)[:-1]
            if fieldtype[1] == "float":
                list_obj = [float(x) for x in list_obj]
            if fieldtype[1] == "int":
                list_obj = [int(x) for x in list_obj]
            return list_obj
        if fieldtype[0] == "map":
            raw = raw.replace("'", "") # picking up keys sometimes creates stray ' characters
            map_obj = {x.split("=")[0] : x.split("=")[1] for x in raw.split(">")[:-1]}
            if fieldtype[1] == "float":
                map_obj = {float(a) : b for a, b in map_obj.items()}
            if fieldtype[1] == "int":
                map_obj = {int(a) : b for a, b in map_obj.items()}
            if fieldtype[2] == "float":
                map_obj = {a : float(b) for a, b in map_obj.items()}
            if fieldtype[2] == "int":
                map_obj = {a : int(b) for a, b in map_obj.items()}
            if fieldtype[2] == "list":
                map_obj = {a : Savedata.parse_savedata_collection(b, fieldtype[2:4]) for a, b in map_obj.items()}
            return map_obj

    # convert list/map object to savedata format
    def export_savedata_collection(obj, fieldtype, listsep):
        print(fieldtype)
        if fieldtype[0] == "list":
            ret = ""
            for x in obj:
                ret += str(x) + listsep
            return ret
        if fieldtype[0] == "map":
            ret = ""
            for a, b in obj.items():
                ret += str(a) + "=" + (Savedata.export_savedata_collection(b, fieldtype[2:4], "&") if fieldtype[2] == "list" else str(b)) + ">"
            return ret


class Editor():
    """
    Utilities for loading, editing and saving files.

    Editor instance created on startup, contains the currently loaded Savedata instance.
    """

    def __init__(self, savefile_path, config):
        self.path = savefile_path
        self.config = config
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
        savefile.close()
        
    def save(self, filename):
        if self.savedata is None:
            raise Exception("No Savefile Loaded")
        with open(filename, "wt") as hldsfile:
            self.savedata.save_hlds(hldsfile)

    def export(self, slot):
        if self.savedata is None:
            raise Exception("No Savefile Loaded")
        header_text = self.config.get("main", "header", fallback=None)
        if header_text is None:
            raise Exception("Cannot export savefile without header. Set header from the options menu first.")
        header = base64.standard_b64decode(header_text)
        with open(join(self.path, "HyperLight_RecordOfTheDrifter_{0}.sav".format(slot)), "wb", buffering=0) as savefile:
            self.savedata.export_savefile(savefile, header)
        print("exported data to slot {0}".format(slot))

    # add header from savefile to config
    def get_header(self, filename):
        savefile = open(filename, "rb", buffering=0)
        header = base64.standard_b64decode(savefile.read())[0:60]
        header_text = base64.standard_b64encode(header).decode()
        print(header_text)
        self.config["main"]["header"] = header_text
        savefile.close()
        
    def __str__(self):
        if self.savedata:
            return self.savedata
        else:
            return "No save loaded."

