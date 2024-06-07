import json
import os


class Settings:
    def __init__(self):
        self.settings_list = {
            "Encoder": [
                "None",
                "h264_nvenc",
                "h264_amf",
                "hevc_nvenc",
                "hevc_amf",
                "h264_mf",
                "hevc_qsv",
                "av1",
                "av1_qsv",
                "av1_nvenc",
                "av1_amf",
                "libx264",
                "libx264rgb",
                "libopenh264",
            ],
            "Framerate": 60,
            "CRF": "23",
            "Show CPU usage": True,
            "Output filename (supports timestamps)": "hello world %Y-%m-%d %H-%M-%S",
            "Output format": ".mp4",
            "Start recording": "home",
            "Stop recording": "end",
            "Custom FFmpeg path (blank to use the ffmpeg on PATH)": "",
            "Arguments": '-f dshow -thread_queue_size 1024 -rtbufsize 256M -audio_buffer_size 80 -framerate 60 -i video="screen-capture-recorder":audio="virtual-audio-capturer" -r 60 -crf 28 -pix_fmt yuv420p -movflags +faststart -c:a aac -ac 2 -b:a 128k -tune hq -preset p1',
            "For a comprehensive list of arguments:": None,
            "https://gist.github.com/tayvano/6e2d456a9897f55025e25035478a3a50": None,
        }
        self.settings_file = "settings.json"

    def save_settings(self, settings):
        with open(self.settings_file, "w") as f:
            json.dump(settings, f, indent=4)

    def load_settings(self):
        settings = {}
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as f:
                settings = json.load(f)
        return settings
