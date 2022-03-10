from importlib import import_module

from asyncio import sleep as as_sleep
from discord.ext import commands
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from converters import SourceDetector


class MusicPlayer(commands.Cog):
    voice_client = None

    def __init__(self, bot):
        self.bot = bot
        self._playlists = {}  # {<guild_id>: [(<play_config>, <title>)]}
        self.__sources = {}

    @commands.command(name='play', aliases=('p',))
    async def play(self, ctx, *, arg: SourceDetector):
        source, link = arg

        if not self.__sources.get(source):
            self.__sources[source] = import_module(f'cogs.music_sources.{source}')

        if not ctx.author.voice:
            await ctx.send(f'You\'re not in a voice channel')
        else:
            vc = self.__get_vc(ctx)

            playlist = self._playlists.setdefault(ctx.guild.guild_id, [])
            play_config, title = self.__sources[source].get_config(link)

            if title in (p[1] for p in playlist):
                await ctx.send(f'This song is already in queue')  # Могут быть коллизии
            else:
                playlist.append((play_config, title))
                await ctx.send(f'Added to queue: {title}')  # TODO: Красивую плашку

                await self.__play_loop(vc)
            # vc.play(FFmpegPCMAudio(**play_config))

    async def __get_vc(self, ctx):
        if not ctx.voice_client:
            await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_deaf=True)
            vc = await ctx.author.voice.channel.connect(timeout=10)
        else:
            vc = ctx.voice_client

        return vc

    def __get_source(self):  # TODO
        pass

    async def __play_loop(self, vc):  # TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # session_id
        while True:
            if not vc.is_playing():
                pass
            else:
                await as_sleep(1)

    @commands.command(name='stop', aliases=('s',))
    async def stop(self, ctx):
        self.voice_client.stop()

    @commands.command(name='next', aliases=('n',))
    async def next(self, ctx):
        print('BasePlayer.next')

    @commands.command(name='exit', aliases=('e',))
    async def exit(self, ctx):
        print('BasePlayer.exit')

    @commands.command(name='queue', aliases=('q',))
    async def queue(self, ctx):
        await ctx.send(f'Queue:\n{self._playlists[ctx.guild.id]}')

    @commands.command(name='jump', aliases=('j',))
    async def jump(self, ctx):
        print('BasePlayer.jump')
