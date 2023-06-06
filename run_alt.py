#!/usr/bin/python3.8

import main
import tkinter as tk
from tkinter import filedialog

start_server_dir = lambda: start_server(dir=True)

def stop_server():
    main.stop_server()
    label.config(text='Server Stopped')
    button.config(text='Start Server', command=start_server)
    root.protocol("WM_DELETE_WINDOW", root.quit)


def start_server(dir=False):
    if dir:
        selected_file = filedialog.askdirectory(
            initialdir='/home/cedcoss/Downloads')
    else:
        selected_file = filedialog.askopenfilename(
            initialdir='/home/cedcoss/Downloads')
    if selected_file:
        main.set_file(selected_file)
        ip = main.start_server()
        label.config(text=f'{ip}\nSharing: '+selected_file.split('/')[-1])
        button.config(text='Stop Server', command=stop_server)
        root.protocol("WM_DELETE_WINDOW", quit)


def quit():
    stop_server()
    root.quit()


# Create the Tkinter root window
root = tk.Tk()
root.title("Server Control Panel")
window_width = 400
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width // 4) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
root.configure(bg="#F5F5F5")

# Create a label
label = tk.Label(root, text="Not Sharing", font=("Arial", 18), bg="#F5F5F5")
label.pack(pady=20)

# Create a button to choose a file
choose_file_button = tk.Button(root, text="Choose File", font=("Arial", 12), command=start_server,
                               bg="#5D5FEF", fg="white", relief="flat", activebackground="#4F4FEF", activeforeground="white")
choose_file_button.pack(pady=10)
choose_file_button = tk.Button(root, text="Choose Dir", font=("Arial", 12), command=start_server_dir,
                               bg="#5D5FEF", fg="white", relief="flat", activebackground="#4F4FEF", activeforeground="white")
choose_file_button.pack(pady=10)

# Create a button to start/stop the server
button = tk.Button(root, text="Start Server", font=("Arial", 12), command=start_server,
                   bg="#5D5FEF", fg="white", relief="flat", activebackground="#4F4FEF", activeforeground="white")
button.pack(pady=10)
# Run the Tkinter event loop
root.mainloop()
