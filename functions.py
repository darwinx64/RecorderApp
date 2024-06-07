import tkinter as tk
from tkinter import messagebox
import subprocess
from datetime import datetime
import re
import psutil
from time import sleep
from settings_functions import Settings
import os
from os import system, name
import shlex
import keyboard


class RecorderFunctions:
    def __init__(self, root, duration_label, record_button, stop_button, usage_label):
        self.root = root
        self.duration_label = duration_label
        self.record_button = record_button
        self.stop_button = stop_button
        self.usage_label = usage_label
        self.process = None
        self.start_time = None
        self.do_usage = True
        self.recording = False
        self.settings = Settings()
        self.update_duration()
        loaded = self.settings.load_settings()
        try:
            keyboard.add_hotkey(loaded.get("Start recording"), self.record_action)
            keyboard.add_hotkey(loaded.get("Stop recording"), self.stop_action)
        except:
            messagebox.showwarning(
                "Warning",
                "Hotkeys initialization failed.\nLikely due to deleted settings.json.\nGo to Edit > Settings, save settings, and restart.",
            )
        try:
            path = loaded.get("Custom FFmpeg path (blank to use the ffmpeg on PATH)")
            subprocess.run(["ffmpeg" if path == "" else path])
            print("FFmpeg was found!")
        except:
            messagebox.showwarning(
                "Warning",
                "FFmpeg wasn't found or the path is invalid.\nDownload FFmpeg from the README.md or set the path in Edit > Settings.",
            )

    def remove_parentheses(self, input_string):
        return re.sub(r"\s*\([^)]*\)", "", input_string)

    def record_action(self):
        if self.recording:
            return
        self.recording = True
        loaded = self.settings.load_settings()
        encoder = self.remove_parentheses(loaded.get("Encoder"))
        print(encoder)
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        self.start_time = datetime.now()
        self.record_timestamp = self.start_time.strftime(
            loaded.get("Output filename (supports timestamps)")
        )
        self.process_args = "ffmpeg" + " -framerate " + loaded.get("Framerate") + " -y "
        self.process_args += loaded.get("Arguments")
        self.process_args += (
            " -c:v "
            + encoder
            + " -crf "
            + loaded.get("CRF")
            + ' "'
            + self.record_timestamp
            + loaded.get("Output format")
            + '"'
        )
        print(self.process_args)
        self.process = subprocess.Popen(
            self.process_args,
            stdin=subprocess.PIPE,
        )
        self.update_duration()
        self.stop_button.config(state=tk.NORMAL)

    def convert_to_mp4(self, input_file, output_file):
        cmd = ["ffmpeg", "-i", input_file, "-c:v", "copy", "-c:a", "copy", output_file]
        subprocess.run(cmd, check=False)
        print("removing input")
        try:
            os.remove(input_file)
        except OSError:
            pass

    def stop_action(self):
        if not self.recording:
            return
        self.recording = False
        self.stop_button.config(state=tk.DISABLED)
        self.record_button.config(state=tk.DISABLED)
        if self.process:
            self.process.communicate(input=b"q")
            self.process.wait()
        self.start_time = None
        self.update_duration()
        self.record_button.config(state=tk.NORMAL)

    def update_duration(self):
        if self.start_time:
            elapsed_time = datetime.now() - self.start_time
            hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            self.duration_label.config(
                text="{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
            )
            self.root.after(1000, self.update_duration)
        else:
            self.duration_label.config(text="00:00:00")

    def usage_loop(self):
        while True and self.usage_label and self.do_usage:
            if self.settings.load_settings().get("Show CPU usage"):
                self.usage_label.config(
                    text="CPU usage: " + str(psutil.cpu_percent()) + "%"
                )
            else:
                self.usage_label.config(text=" ")
            sleep(0.5)

    def on_closing(self):
        if self.start_time:
            if messagebox.askokcancel("Exit", "Are you sure?"):
                self.stop_action()
            else:
                return

        self.do_usage = False
        self.root.destroy()
