import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class About:
    def __init__(self, master):
        self.root = tk.Toplevel(master)
        self.root.grab_set()
        self.root.title("About")
        self.root.geometry("858x358")
        self.root.maxsize(858, 358)
        self.root.minsize(858, 358)
        self.root.iconbitmap("icon.ico")

        header_font = tk.font.nametofont("TkDefaultFont").copy()
        header_font.configure(size=20, weight="bold")

        self.ok_button = ttk.Button(self.root, text="OK", command=self.root.destroy)
        self.ok_button.place(x=760, y=310, width=70, height=25)

        logo_photoimage = ImageTk.PhotoImage(
            Image.open("./icon.png").resize([212, 212], Image.LANCZOS)
        )
        self.logo = tk.Label(self.root, image=logo_photoimage)
        self.logo.image = logo_photoimage
        self.logo.place(x=60, y=60, width=212, height=212)

        self.name_label = tk.Label(
            self.root, text="RecorderApp", font=header_font, justify=tk.CENTER
        )
        self.desc_label1 = tk.Label(
            self.root,
            text="A free and open source FFmpeg screen capturing frontend",
            justify=tk.CENTER,
        )
        self.desc_label2 = tk.Label(
            self.root, text="Made in Python with tkinter", justify=tk.CENTER
        )

        self.name_label.place(x=510, y=130, width=70, height=25)
        self.desc_label1.place(x=360, y=180, width=366, height=30)
        self.desc_label2.place(x=460, y=200, width=163, height=30)
