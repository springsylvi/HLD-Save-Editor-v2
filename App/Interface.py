from tkinter import *
from tkinter import ttk

class Interface():
    """
    GUI manager
    """

    # file -> load
    def load():
        # TODO - popup window
        filename = "temp"
        self.editor.load(filename)


    # file -> save
    def save():
        pass


    # file -> save as
    def saveas():
        pass

    
    # file -> export
    def export():
        pass
    

    def __init__(self, editor, app):
        self.editor = editor
        self.app = app
        self.tk = Tk(screenName="Editor")
        
        # menu
        self.menu = Menu(self.tk)
        self.filemenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Load", command=self.load)
        self.filemenu.add_command(label="Save", command=self.save)
        self.filemenu.add_command(label="Save As", command=self.saveas)
        self.filemenu.add_command(label="Export", command=self.export)
        self.tk.config(menu=self.menu)

