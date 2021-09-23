import os
import youtube_dl as yt


YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'False'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


def get_config(link_or_name):
    if link_or_name.startswith('http'):
        with yt.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(link_or_name, download=False)
        return (
            dict(executable=os.environ['FFMPEG_EXECUTABLE'], source=info['formats'][0]['url'], **FFMPEG_OPTIONS),
            info['title']
        )
    else:
        pass
