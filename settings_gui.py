import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from settings_functions import Settings
import webbrowser


class SettingsGUI:
    def __init__(self, settings, master):
        self.settings = settings

        self.root = tk.Toplevel(master)
        self.root.grab_set()
        self.root.title("Settings")
        self.root.geometry("700x600")

        self.settings_frame = ttk.Frame(self.root)
        self.settings_frame.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.settings_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=5)

        self.canvas = tk.Canvas(self.settings_frame, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.canvas.yview)

        self.settings_canvas = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.settings_canvas, anchor=tk.NW)

        self.populate_settings()

        self.save_button = ttk.Button(
            self.root, text="Save Settings", command=self.save_settings
        )
        self.save_button.pack(side=tk.BOTTOM, pady=10)

        self.load_settings()

    def populate_settings(self):
        self.widgets = {}
        for index, (key, value) in enumerate(self.settings.settings_list.items()):
            label = None
            if value == None and isinstance(key, str):
                fnt = ("Arial", 8, "italic")
                label = ttk.Label(
                    self.settings_canvas,
                    text=key,
                    font=("Arial", 8, "italic"),
                )
                if "https" in key:
                    label.configure(underline=True)
                    label.bind(
                        "<Button-1>",
                        lambda e: webbrowser.open_new_tab(label.cget("text")),
                    )
                label.grid(row=index, column=0, padx=5, pady=1, sticky=tk.W)
            else:
                label = ttk.Label(self.settings_canvas, text=key)
                label.grid(row=index, column=0, padx=5, pady=5, sticky=tk.W)

            if isinstance(value, list):
                combo = ttk.Combobox(self.settings_canvas, values=value)
                combo.set(value[0])
                combo.grid(row=index, column=1, padx=5, pady=5, sticky=tk.W)
                self.widgets[key] = combo
            elif isinstance(value, str):
                entry = None
                if key == "Arguments":
                    entry = tk.Text(
                        self.settings_canvas, font=("Consolas", 9), height=10
                    )
                    entry.insert(tk.END, value)
                    entry.grid(
                        row=index,
                        column=0,
                        columnspan=2,
                        padx=5,
                        pady=5,
                        sticky=tk.NSEW,
                    )
                else:
                    entry = tk.Entry(self.settings_canvas)
                    entry.insert(tk.END, value)
                    entry.grid(row=index, column=1, padx=5, pady=5, sticky=tk.W)
                self.widgets[key] = entry
            elif isinstance(value, bool):
                checkbox_var = tk.BooleanVar(value=value)
                checkbox = ttk.Checkbutton(self.settings_canvas, variable=checkbox_var)
                checkbox_var.set(value)
                checkbox.grid(row=index, column=1, padx=5, pady=5, sticky=tk.W)
                self.widgets[key] = checkbox_var
            elif isinstance(value, int):
                spinbox = ttk.Spinbox(self.settings_canvas, from_=0, to=100)
                spinbox.set(value)
                spinbox.grid(row=index, column=1, padx=5, pady=5, sticky=tk.W)
                self.widgets[key] = spinbox

    def save_settings(self):
        try:
            current_settings = {}
            for key, widget in self.widgets.items():
                if isinstance(widget, tk.Text):
                    current_settings[key] = widget.get("1.0", tk.END)
                else:
                    current_settings[key] = widget.get()
            self.settings.save_settings(current_settings)
            messagebox.showinfo(
                "Notice",
                "Some changes may require a restart to take effect, such as hotkey changes",
            )
            self.root.destroy()
        except:
            messagebox.showerror(
                "Error",
                "An error occured while saving settings\nCheck if a field is invalid or if you have the permissions to make and write to the file",
            )

    def load_settings(self):
        saved_settings = self.settings.load_settings()
        for key, value in saved_settings.items():
            if key in self.widgets:
                widget = self.widgets[key]
                if isinstance(widget, tk.BooleanVar):
                    widget.set(value)
                elif isinstance(widget, tk.Text):
                    widget.delete(1.0, tk.END)
                    widget.insert(tk.END, str(value))
                else:
                    widget.delete(0, tk.END)
                    widget.insert(0, str(value))
