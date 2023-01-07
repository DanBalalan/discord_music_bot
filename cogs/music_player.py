from collections import OrderedDict
from importlib import import_module

from asyncio import sleep as as_sleep
from discord.ext import commands
from discord import FFmpegPCMAudio, PCMVolumeTransformer

from converters import SourceDetector


class MusicPlayer(commands.Cog):
    voice_client = None

    def __init__(self, bot):
        self.bot = bot
        self._playlists = {}  # {<guild_id>: OrderedDict{<id>: <play_config>}}
        self.__sources = {}

    @commands.command(name='play', aliases=('p',))
    async def play(self, ctx, *, arg: SourceDetector):
        source, link = arg

        if not self.__sources.get(source):
            self.__sources[source] = import_module(f'cogs.music_sources.{source}')

        if not ctx.author.voice:
            await ctx.send(f'You\'re not in a voice channel')
        else:
            playlist = self._playlists.setdefault(ctx.guild.id, OrderedDict())
            
            play_config, valid = self.__sources[source].get_config(link)
            if not valid:
                await ctx.send(play_config)
            
            else:
                if play_config.id in playlist:
                    await ctx.send(f'Track `{play_config.title}` is already in queue')
                else:
                    playlist[play_config.id] = play_config
                    await ctx.send(f'Added to queue: `{play_config.title}`')  # TODO: Красивую плашку

                vc = await self.__get_vc(ctx)
                await self.__play_loop(ctx, vc, playlist)

    async def __get_vc(self, ctx):
        if not ctx.voice_client:
            await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_deaf=True)
            vc = await ctx.author.voice.channel.connect(timeout=10)
        else:
            vc = ctx.voice_client

        return vc

    async def __play_loop(self, ctx, vc, playlist):  # TODO
        while True:
            if not vc.is_playing() and playlist:
                _, play_config = playlist.popitem(last=False)
                await ctx.send(f'Now playing: `{play_config.title}`')
                vc.play(FFmpegPCMAudio(**play_config.config))
            else:
                await as_sleep(3)

    @commands.command(name='stop', aliases=('s',))
    async def stop(self, ctx):
        ctx.voice_client.stop()

    @commands.command(name='next', aliases=('n',))
    async def next(self, ctx):
        print('BasePlayer.next')

    @commands.command(name='exit', aliases=('e',))
    async def exit(self, ctx):
        print('BasePlayer.exit')

    @commands.command(name='queue', aliases=('q',))
    async def queue(self, ctx):
        titles = '\n'.join([f'`{n+1}. {cfg.title}`' for n, cfg in enumerate(self._playlists[ctx.guild.id].values())])
        await ctx.send(f'Queue:\n{titles}')

    @commands.command(name='jump', aliases=('j',))
    async def jump(self, ctx):
        print('BasePlayer.jump')
