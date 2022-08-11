from json import loads, dumps
import base64


class Savedata():
    """
    Contains savedata as a dictionary.
    """

    def __init__(self, data):
        self.savedata_map = data

    def get_field(self, field):
        return self.savedata_map.get(field)

    def set_field(self, field, value):
        # TODO - check if field is a valid string
        self.savedata_map[field] = value

    # parse data from .sav file
    def parse_savefile(jsondata):
        savedata_map = {}
        # TODO - convert jsondata to fields and add to savedata_map
        return savedata_map


class Editor():
    """
    Utilities for loading, editing and saving files.

    Editor instance created on startup, contains the currently loaded Savedata instance.
    """

    def __init__(self, savefile_path):
        self.path = savefile_path
        self.filename = "No File"
        self.savedata = None

    def load(self, filename):
        # read file
        savefile = open(filename, "rb", buffering=0)
        jsondata = base64.standard_b64decode(savefile.read())[60:-1].decode()
        # create savedata object
        self.savedata = Savedata(Savedata.parse_savefile(jsondata))

    def save(self, filename=None):
        if filename is None:
            filename = self.filename
        pass

    def __str__(self):
        if self.savedata:
            return self.savedata
        else:
            return "No save loaded."

