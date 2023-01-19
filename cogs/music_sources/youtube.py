import re
from dataclasses import dataclass
from datetime import timedelta
from typing import Optional, Tuple

import youtube_dl as yt

from settings import FFMPEG_EXECUTABLE


DEFAULT_OFFSET = "00:00"
OFFSET_PATTERN = re.compile(pattern=r"\?t=(?P<offset_seconds>\d+)")

YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'False', 'rm_cachedir': True}

FFMPEG_BEFORE_OPTIONS = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
FFMPEG_OPTIONS = '-vn'


@dataclass
class YtConfig:
    id: str
    config: dict
    title: str
    duration: str
    author_name: str

    @property
    def track_repr(self):
        return f'{self.title} ({self.duration}) added by {self.author_name}'


def get_offset(link: str) -> str:
    try:
        seconds = int(OFFSET_PATTERN.search(link).group("offset_seconds"))
    except Exception:
        return DEFAULT_OFFSET
    
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    hours = int(hours)
    minutes = int(minutes)
    seconds = int(seconds)

    if minutes < 10:
        minutes = '0{}'.format(minutes)

    if seconds < 10:
        seconds = '0{}'.format(seconds)

    return f'{hours}:{minutes}:{seconds}'


def get_config(link_or_name: str, author_name: str) -> Tuple[Optional[YtConfig], str]:
    if link_or_name.startswith('http'):
        try:
            with yt.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(link_or_name, download=False)

            ffmpeg_options = {
                'before_options': f'{FFMPEG_BEFORE_OPTIONS} -ss {get_offset(link_or_name)}',
                'options': FFMPEG_OPTIONS,
            }

            return YtConfig(
                id=link_or_name,
                config=dict(executable=FFMPEG_EXECUTABLE, source=info['formats'][0]['url'], **ffmpeg_options),
                title=info['title'],
                duration=str(timedelta(seconds=info['duration'])),
                author_name=author_name
            ), ""
        except Exception as e:
            print(e)  # TODO: log
            return None, "Error extracting audio. Try again"

    else:
        return None, "Search is not implemented yet"
