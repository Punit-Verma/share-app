import os
import zipfile
from tkinter import *
from tkinterdnd2 import *
from tkinter import filedialog
from tkinter import ttk


class DragDropWindow(Frame):
    def __init__(self, master):
        super().__init__(master)

        # theme
        self.tk.call("source", "theme/forest-dark.tcl")
        # self.tk.call("source", "theme/forest-light.tcl")
        ttk.Style().theme_use("forest-dark")

        self.resource = None

        self.master = master
        self.master.title("Share")
        self.master.geometry("450x300")

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
        self.resource_label.config(text=file_or_folder.split("/")[-1])
        self.text_entry.delete(0, END)
        self.text_entry.insert(0, file_or_folder)
        if os.path.isfile(file_or_folder):
            self.isDir = False
        elif os.path.isdir(file_or_folder):
            self.isDir = True
        # if it's a dir and auto_zip is enabled, zip it
        if self.isDir and self.auto_zip:
            # disable the share button
            self.share_button.config(state="disabled")
            self.logContent(text="Auto zipping...")
            self.resource = self.resource + ".zip"
            self.resource_label.config(text=self.resource.split("/")[-1])
            self.text_entry.delete(0, END)
            self.text_entry.insert(0, self.resource)
            op_zip_filename = self.zip_folder(file_or_folder, self.resource)
            self.share_button.config(state="normal")
            self.logContent(text="Auto zipped! " + op_zip_filename)

    def handle_share_button(self):
        if self.resource is None:
            print("No resource selected!")
            self.logContent(text="No resource selected!", type="error")
            return
        print("Sharing:", self.resource)
        self.logContent(text="Sharing: " + self.resource)

    def share(self):
        file_or_folder = self.resource_label["text"]
        if os.path.exists(file_or_folder):
            self.resource_label.config(state="normal")  # Disable the button
            self.isDir = os.path.isdir(file_or_folder)
            print("Sharing:", file_or_folder)
            print("Is Directory:", self.isDir)
            print("Auto Zip:", self.auto_zip)
        else:
            self.resource_label.config(state="disabled")  # Disable the button
            print("File or folder does not exist!")

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
drag_drop_window = DragDropWindow(root)
root.mainloop()
