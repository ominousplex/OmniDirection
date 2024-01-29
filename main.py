import tkinter
from tkinter import *
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk
from flask import Flask, render_template, send_file, request
import threading
import os
import webbrowser
import tempfile
import sys
temp_dir = tempfile.TemporaryDirectory()



print(temp_dir.name)

app = Flask(__name__)
#app.template_folder()
@app.route('/',methods=["GET","POST"])
def hello_world():
   if request.method == "GET":
      return send_file("C:\\Users\\mason\\Downloads\\OmniDirection.lua")
   if request.method == "POST":
      data = request.get_json(force=True)
      # with open(temp_dir.name+f"\\{data['name']}.lua","w") as file:
      #    file.write(data['data'])
      #    file.close()
      inserted_files = []
      for entry in data:
         try:
            if entry["parent_id"] == "ROOT":
               if entry["ClassName"] != "Folder":
                  with open(temp_dir.name+f"\\{entry['name']}.lua","w") as file:
                     file.write(entry['data'])
                     file.close()
                     inserted_files.append({"path":temp_dir.name+f"\\{entry['name']}.lua","uuid":entry["uuid"],"ClassName":entry["ClassName"]})
               if entry["ClassName"] == "Folder":
                  os.mkdir(temp_dir.name+f"/{entry['name']}")
                  inserted_files.append({"path": temp_dir.name + f"\\{entry['name']}", "uuid": entry["uuid"],
                                         "ClassName": entry["ClassName"]})
            else:
               for second_entry in inserted_files:
                  #print(second_entry)
                  if entry["parent_id"] == second_entry["uuid"]:
                     if second_entry["ClassName"] == "Folder":
                        if (entry["ClassName"] == "Script" or entry["ClassName"] == "LocalScript" or entry["ClassName"] == "ModuleScript"):
                           with open(second_entry["path"]+f"\\{entry['name']}.lua", "w") as file:
                              file.write(entry['data'])
                              file.close()
                              inserted_files.append({"path": second_entry["path"]+f"\\{entry['name']}.lua", "uuid": entry["uuid"],
                                                     "ClassName": entry["ClassName"]})
                        if entry["ClassName"] == "Folder":
                           os.mkdir(second_entry["path"]+ f"/{entry['name']}")
                           inserted_files.append(
                              {"path": second_entry["path"] + f"\\{entry['name']}", "uuid": entry["uuid"],
                               "ClassName": entry["ClassName"]})
                     elif (second_entry["ClassName"] == "Script" or second_entry["ClassName"] == "LocalScript" or second_entry["ClassName"] == "ModuleScript"):
                        os.mkdir(f"{second_entry['path']}.children")
                        path = f"{second_entry['path']}.children"
                        if (entry["ClassName"] == "Script" or entry["ClassName"] == "LocalScript" or entry["ClassName"] == "ModuleScript"):
                           with open(path+f"\\{entry['name']}.lua", "w") as file:
                              file.write(entry['data'])
                              file.close()
                              inserted_files.append({"path": path+f"\\{entry['name']}.lua", "uuid": entry["uuid"],
                                                     "ClassName": entry["ClassName"]})
                        if entry["ClassName"] == "Folder":
                           os.mkdir(path+ f"/{entry['name']}")
                           inserted_files.append(
                              {"path": path + f"\\{entry['name']}", "uuid": entry["uuid"],
                               "ClassName": entry["ClassName"]})
         except Exception as e:
            print(e)

      return "200"

current_directory = os.path.dirname(os.path.abspath(__file__))

# Specify the icon file relative to the current directory
icon_path = os.path.join(current_directory, "icon.ico")




def run_flask():
   app.run()
#image_path = os.path.join(sys._MEIPASS,"image.png")

# Create an instance of tkinter frame or window
win=Tk()
win.title("OmniDirection")
win.iconbitmap(icon_path)#"image.ico")
tkinter.Label(win, text=f"Your OmniDirection server is now running on port 5000, click X to hide this window to taskbar.\n\nhttp://localhost:5000/\n\nProject workspace can be found here:\n{temp_dir.name}\n\nMake sure to connect to the server to load your files.\nFollow proper file naming conventions to avoid bugs/file deletions.").pack()
# Set the size of the window
win.geometry("600x150")

# Define a function for quit the window
def quit_window(icon, item):
   icon.stop()
   win.destroy()

# Define a function to show the window again
def show_window(icon, item):
   icon.stop()
   win.after(0,win.deiconify())

# Hide the window and show on the system taskbar
def hide_window():
   win.destroy()
   # win.withdraw()
   # image=Image.open(icon_path)
   # menu=(item('Quit', quit_window), item('Show', show_window))
   # icon=pystray.Icon("OmniServer", image, "OmniDirectionServer", menu)
   # webbrowser.open("http://localhost:5000")
   # icon.run()


t1 = threading.Thread(target=run_flask,daemon=True)

def backendstart():
   t1.start()



win.protocol('WM_DELETE_WINDOW', hide_window)
#win.after_idle(backendstart)
backendstart()
win.mainloop()
