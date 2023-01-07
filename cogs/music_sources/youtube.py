import os

from dataclasses import dataclass

import youtube_dl as yt


YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'False'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


@dataclass
class YtConfig:
    config: dict
    title: str
    id: str


def get_config(link_or_name):
    if link_or_name.startswith('http'):
        try:
            with yt.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(link_or_name, download=False)

            return YtConfig(
                config=dict(executable=os.environ['FFMPEG_EXECUTABLE'], source=info['formats'][0]['url'], **FFMPEG_OPTIONS),
                title=info['title'],
                id=link_or_name
            ), True
        except yt.utils.ExtractorError as e:
            print(e)  # TODO: log
            return "Error extracting audio", False

    else:
        return "Search is not implemented yet", False   # TODO
