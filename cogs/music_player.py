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
        self._sources = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Cog `{self.__class__.__name__}` ready')

    @commands.command(name='play', aliases=('p',))
    async def play(self, ctx, *, arg: SourceDetector):
        print(ctx.guild.id)
        print(ctx.guild)
        source, link = arg

        print(source, link)

        if not self._sources.get(source):
            self._sources[source] = import_module(f'cogs.music_sources.{source}')

        voice_client = await self._get_voice_client(ctx)
        if voice_client is None:
            await ctx.send(f'You\'re not in a voice channel')
        
        else:
            playlist = self._playlists.setdefault(ctx.guild.id, OrderedDict())
            
            play_config, valid = self._sources[source].get_config(link)
            
            if not valid:  # play_config is error message
                await ctx.send(play_config)
            
            else:
                if play_config.id in playlist:
                    await ctx.send(f'Track `{play_config.title}` is already in queue')
                else:
                    playlist[play_config.id] = play_config
                    await ctx.send(f'Added to queue: `{play_config.title} ({play_config.duration})`')  # TODO: Красивую плашку

                await self._play_track(ctx, voice_client, playlist)

    async def _get_voice_client(self, ctx):
        if not ctx.author.voice:
            return None
        
        if ctx.voice_client is None:
            await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_deaf=True)
            voice_client = await ctx.author.voice.channel.connect(timeout=10)
        else:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                await ctx.send('You can\'t interact with bot from another voice channel')
                return None

            voice_client = ctx.voice_client

        return voice_client

    async def _play_track(self, ctx, voice_client, playlist):  # TODO
        if not voice_client.is_playing() and playlist:
            _, play_config = playlist.popitem(last=False)

            voice_client.play(PCMVolumeTransformer(FFmpegPCMAudio(**play_config.config), volume=0.1))
            await ctx.send(f'Now playing: `{play_config.title} ({play_config.duration})`')

    @commands.command(name='stop', aliases=('s',))
    async def stop(self, ctx):
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        self._playlists[ctx.guild.id] = OrderedDict()

    @commands.command(name='next', aliases=('n',))
    async def next(self, ctx):
        print('BasePlayer.next')

    @commands.command(name='exit', aliases=('e',))
    async def exit(self, ctx):
        print('BasePlayer.exit')

    @commands.command(name='queue', aliases=('q',))
    async def queue(self, ctx):
        titles = '\n'.join([f'`{n+1}. {cfg.title} ({cfg.duration})`' for n, cfg in enumerate(self._playlists[ctx.guild.id].values())])
        await ctx.send(f'Queue:\n{titles}')

    @commands.command(name='jump', aliases=('j',))
    async def jump(self, ctx):
        print('BasePlayer.jump')
