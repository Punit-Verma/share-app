#! /usr/bin/python3.8

import os
import zipfile
from tkinter import *
from tkinterdnd2 import *
from tkinter import ttk
import main

class ShareApp(Frame):
    def __init__(self, master):
        super().__init__(master)

        # theme
        self.tk.call("source", "theme/forest-dark.tcl")
        ttk.Style().theme_use("forest-dark")

        self.resource = None
        self.is_server_started = False

        self.master = master
        self.master.title("Share")
        self.master.geometry("470x300")

        self.drop_frame = ttk.Frame(self.master)
        self.drop_frame.pack(expand=True, fill=BOTH)

        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind("<<Drop>>", self.set_selected_resource)

        self.resource_label = ttk.Label(
            self.drop_frame,
            text="Drop a File or Dir",
            font=("Helvetica", 20),
        )
        self.resource_label.pack(expand=True)

        # log frame
        self.log_frame = ttk.Frame(self.master)
        self.log_frame.pack(side=BOTTOM, fill=X, padx=10, pady=5)

        self.log = ttk.Label(self.log_frame, text="Gui loaded")
        self.log.pack(side=BOTTOM, fill="both", expand=True)

        self.bottom_frame = ttk.Frame(self.master)
        self.bottom_frame.pack(side=BOTTOM, fill=X, padx=10, pady=10)

        self.text_entry = ttk.Entry(self.bottom_frame)
        self.text_entry.pack(side=LEFT, fill="both", expand=True, padx=(0, 10))

        self.share_button = ttk.Button(
            self.bottom_frame,
            style="Accent.TButton",
            text="Share",
            command=self.handle_share_button,
        )
        self.share_button.pack(side=RIGHT)

        self.auto_zip = False
        self.auto_zip_var = IntVar()
        self.auto_zip_checkbutton = ttk.Checkbutton(
            self.bottom_frame,
            text="Auto Zip",
            style="Switch",
            variable=self.auto_zip_var,
            command=self.toggle_auto_zip,
        )
        self.auto_zip_checkbutton.pack(side=RIGHT, padx=(0, 10))

        self.isDir = False

    def set_selected_resource(self, event):
        file_or_folder = event.data
        self.resource = file_or_folder
        self.resource_label.config(text=os.path.basename(file_or_folder))
        self.text_entry.delete(0, END)
        self.text_entry.insert(0, file_or_folder)
        self.isDir = os.path.isdir(file_or_folder)
        # if it's a dir and auto_zip is enabled, zip it
        if self.isDir and self.auto_zip:
            # disable the share button
            self.share_button.config(state="disabled")
            self.logContent(text="Auto zipping...")
            self.resource = self.resource + ".zip"
            self.resource_label.config(text=os.path.basename(self.resource))
            self.text_entry.delete(0, END)
            self.text_entry.insert(0, self.resource)
            op_zip_filename = self.zip_folder(file_or_folder, self.resource)
            self.share_button.config(state="normal")
            self.logContent(text="Auto zipped! " + op_zip_filename)
        # logic to set the resource to the server
        # self.resource is the path to the file or folder
        main.set_file(self.resource)

    def handle_share_button(self):
        if self.is_server_started:
            self.share_button.config(text="Share")
            # logic to stop the server
            main.stop_server()
            self.is_server_started = False
            return
        if self.resource is None:
            print("No resource selected!")
            self.logContent(text="No resource selected!", type="error")
            return
        print("Sharing:", self.resource)
        self.logContent(text="Sharing: " + self.resource)
        self.share_button.config(text="Stop Sharing")
        self.is_server_started = True
        # logic to start the server
        main.start_server()


    def toggle_auto_zip(self):
        self.auto_zip = bool(self.auto_zip_var.get())
        print("Auto Zip:", self.auto_zip)

    def zip_folder(self, folder_path, output_path):
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arcname)

        return output_path

    def logContent(self, text, type="info"):
        self.log.config(text=text, foreground="green" if type == "info" else "red")


root = TkinterDnD.Tk()
drag_drop_window = ShareApp(root)
root.mainloop()
