import asyncio

from collections import OrderedDict
from importlib import import_module

from discord.ext import commands
from discord import FFmpegPCMAudio, PCMVolumeTransformer

from converters import SourceDetector
from settings import VOLUME


class MusicPlayer(commands.Cog):
    voice_client = None

    def __init__(self, bot):
        self.bot = bot
        self._playlists = {}  # {<guild_id>: OrderedDict{<id>: <play_config>}}
        self._sources = {}

    async def _get_voice_client(self, ctx):
        if not ctx.author.voice:
            return None

        if ctx.voice_client is None:
            await ctx.guild.change_voice_state(
                channel=ctx.author.voice.channel, self_deaf=True
            )
            voice_client = await ctx.author.voice.channel.connect(timeout=10)
        else:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                await ctx.send("You can't interact with bot from another voice channel")
                return None

            voice_client = ctx.voice_client

        return voice_client

    async def _play_track(self, ctx, voice_client, play_config):
        playlist = self._playlists[ctx.guild.id]

        if play_config.id not in playlist:
            playlist[play_config.id] = play_config
            await ctx.send(f"Track `{play_config.title}` added to queue")
        else:
            await ctx.send(f"Track `{play_config.title}` is already in queue")
            return

        if not voice_client.is_playing():
            _, play_config = playlist.popitem(last=False)
            voice_client.play(PCMVolumeTransformer(FFmpegPCMAudio(**play_config.config), volume=VOLUME), after=lambda err: self._play_next_track(ctx))
            await ctx.send(f"Now playing: `{play_config.title} ({play_config.duration})`")

    @staticmethod
    def _get_voice_client_by_guild(bot, guild):
        for voice_client in bot.voice_clients:
            if voice_client.guild == guild:
                return voice_client

        raise RuntimeError(f"Can't find voice client for guild `{guild}`")

    def _play_next_track(self, ctx):
        voice_client = self._get_voice_client_by_guild(self.bot, ctx.guild)
        playlist = self._playlists[ctx.guild.id]

        if playlist:
            _, play_config = playlist.popitem(last=False)

            voice_client.play(PCMVolumeTransformer(FFmpegPCMAudio(**play_config.config), volume=VOLUME), after=lambda err: self._play_next_track(ctx))
            asyncio.run_coroutine_threadsafe(ctx.send(f"Now playing: `{play_config.title} ({play_config.duration})`"), self.bot.loop)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog `{self.__class__.__name__}` ready")

    @commands.command(name="play", aliases=("p",))
    async def play(self, ctx, *, arg: SourceDetector):
        source, link = arg
        self._playlists.setdefault(ctx.guild.id, OrderedDict())

        if not self._sources.get(source):
            self._sources[source] = import_module(f"cogs.music_sources.{source}")

        voice_client = await self._get_voice_client(ctx)
        if voice_client is None:
            await ctx.send(f"You're not in a voice channel")

        else:
            play_config, valid = self._sources[source].get_config(link)
            if not valid:  # play_config is error message
                await ctx.send(play_config)

            else:
                await self._play_track(ctx, voice_client, play_config)

    @commands.command(name="stop", aliases=("s",))
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()
        self._playlists[ctx.guild.id] = OrderedDict()

    @commands.command(name="next", aliases=("n",))
    async def next(self, ctx):
        await ctx.send(f"Skipping track")
        await self._play_next_track(ctx)

    @commands.command(name="queue", aliases=("q",))
    async def queue(self, ctx):
        titles = "\n".join(
            [
                f"`{n+1}. {cfg.title} ({cfg.duration})`"
                for n, cfg in enumerate(self._playlists[ctx.guild.id].values())
            ]
        )

        if titles:
            msg = f"Queue:\n{titles}"
        else:
            msg = "Queue is empty"

        await ctx.send(msg)

    @commands.command(name="jump", aliases=("j",))
    async def jump(self, ctx):
        ctx.send("Not implemented yet. Contact bot maintainer for more info")
        print("BasePlayer.jump")
