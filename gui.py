import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from functions import RecorderFunctions
from settings_gui import SettingsGUI
from help_guis import About
from settings_functions import Settings
import threading


class RecorderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Recorder App")
        self.root.geometry("354x88")
        self.root.maxsize(354, 88)
        self.root.minsize(354, 88)
        self.root.iconbitmap("icon.ico")

        settings = Settings()

        self.record_button = ttk.Button(self.root, text="Record")
        self.record_button.grid(row=0, column=0, rowspan=2, sticky=tk.W, pady=5, padx=5)

        self.stop_button = ttk.Button(self.root, text="Stop")
        self.stop_button.grid(row=0, column=1, rowspan=2, sticky=tk.W, pady=5, padx=5)
        self.stop_button.config(state=tk.DISABLED)

        self.toolbar = tk.Menu(self.root)
        self.root.config(menu=self.toolbar)
        self.file_menu = tk.Menu(self.toolbar, tearoff=0)
        self.toolbar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Exit")

        self.settings_menu = tk.Menu(self.toolbar, tearoff=0)
        self.toolbar.add_cascade(label="Edit", menu=self.settings_menu)

        self.help_menu = tk.Menu(self.toolbar, tearoff=0)
        self.toolbar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=lambda: About(self.root))

        self.duration_label = ttk.Label(self.root, text="00:00:00")
        self.duration_label.grid(row=1, column=2, sticky=tk.W, pady=20, padx=5)

        self.usage_label = ttk.Label(self.root, text="CPU usage: 0%")
        self.usage_label.grid(row=0, column=2, sticky=tk.W, pady=0, padx=5)

        self.recorder = RecorderFunctions(
            self.root,
            self.duration_label,
            self.record_button,
            self.stop_button,
            self.usage_label,
        )

        self.record_button.config(command=self.recorder.record_action)
        self.stop_button.config(command=self.recorder.stop_action)
        self.settings_menu.add_command(
            label="Settings", command=lambda: SettingsGUI(settings, root)
        )

        self.root.grid_rowconfigure(0, weight=1)

        self.usage_thread = threading.Thread(target=self.recorder.usage_loop)
        self.usage_thread.start()

        self.root.protocol("WM_DELETE_WINDOW", self.recorder.on_closing)
        self.root.mainloop()
