import os

from dataclasses import dataclass
from datetime import timedelta

import youtube_dl as yt

from settings import FFMPEG_EXECUTABLE


YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'False', 'rm_cachedir': True}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


@dataclass
class YtConfig:
    id: str
    config: dict
    title: str
    duration: str


def get_config(link_or_name):
    if link_or_name.startswith('http'):
        try:
            with yt.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(link_or_name, download=False)

            return YtConfig(
                id=link_or_name,
                config=dict(executable=FFMPEG_EXECUTABLE, source=info['formats'][0]['url'], **FFMPEG_OPTIONS),
                title=info['title'],
                duration=str(timedelta(seconds=info['duration']))
            ), True
        except Exception as e:
            print(e)  # TODO: log
            return "Error extracting audio. Try again", False

    else:
        return "Search is not implemented yet", False   # TODO
