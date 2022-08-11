from tkinter import *
from tkinter import ttk
from tkinter import filedialog

class Interface():
    """
    GUI manager
    """

    # file -> load
    def load(self):
        filename = filedialog.askopenfilename(initialdir=self.app.savefile_path)
        self.editor.load(filename)


    # file -> save
    def save(self):
        pass


    # file -> save as
    def saveas(self):
        pass

    
    # file -> export
    def export(self):
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

