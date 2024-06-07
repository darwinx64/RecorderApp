import tkinter as tk
from tkinter import ttk
from gui import RecorderGUI
from functions import RecorderFunctions
from os import name
from os import system

class RecorderApp:
    def __init__(self, root):
        if name == "nt":
            _ = system("cls")
        else:
            _ = system("clear")
        self.gui = RecorderGUI(root)


if __name__ == "__main__":
    root = tk.Tk()
    app = RecorderApp(root)
