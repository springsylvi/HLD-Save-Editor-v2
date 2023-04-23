import platform, getpass, os
from Interface import *
from Editor import *
from atexit import register

class App:
	"""
	Main application class.
	"""
	
	def read_config():

		config = configparser.ConfigParser()
		try:
			config_file = open("config.ini", "r")
		except FileNotFoundError:
			config_file = open("config.ini", "x+")
		config.read_file(config_file)
		config_file.close()
		return config


	def get_savefile_path(config):

		savefile_path = config.get("main", "path", fallback=None)
		if savefile_path is None:
			sysname = platform.system()
			username = getpass.getuser()
			if (sysname == "Windows"):
				savefile_path = "C:\\Users\\{}\\AppData\\Local\\HyperLightDrifter".format(username)
			elif (sysname == "Darwin"):
				savefile_path = "/Users/{}/Library/Application Support/com.HeartMachine.HyperLightDrifter".format(username)
			elif (sysname == "Linux"):
				savefile_path = "/home/{}/.config/HyperLightDrifter".format(username)
			else:
				raise Exception("Unknown OS, cannot find savefile location")

		if os.path.exists(savefile_path):
			if not "main" in config:
				config.add_section("main")
			config["main"]["path"] = savefile_path
			with open("config.ini", "w+") as config_ini:
				config.write(config_ini)
			return savefile_path
		else:
			raise Exception("Savefile Directory does not exist (likey because HLD is not installed)")


	def __init__(self):

		# load config
		self.config = App.read_config()
		self.savefile_path = App.get_savefile_path(self.config)
		# create Editor instance
		self.editor = Editor(self.savefile_path, self.config)
	

	def main(self):
		# set up gui & loop
		self.ui = Interface(self.editor, self)
		self.ui.tk.mainloop()

	def config_cleanup(self):
		with open("config.ini", "w+") as config_file:
			self.config.write(config_file)


app = App()
register(app.config_cleanup)
app.main()
