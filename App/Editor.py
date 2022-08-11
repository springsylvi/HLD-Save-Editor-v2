from json import loads, dumps


class Savedata():
    """
    Contains savedata as a dictionary.
    """

    def __init__(self, data):
        self.data = data

    def get_field(self, field):
        return self.data.get(field)

    def set_field(self, field, value):
        # TODO - check if field is a valid string
        self.data[field] = value


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
        # replace special chars and parse json
        pass

    def save(self, filename=None):
        if filename is None:
            filename = self.filename
        pass

    def __str__(self):
        if self.savedata:
            return self.savedata
        else:
            return "No save loaded."

