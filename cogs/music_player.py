import asyncio

from collections import OrderedDict
from importlib import import_module

from discord.ext import commands
from discord import Colour, Embed, FFmpegPCMAudio, PCMVolumeTransformer

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
            await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_deaf=True)
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
            await ctx.send(embed=Embed(
                type='rich',
                color=Colour.brand_green(),
                title='Added to queue',
                description=play_config.track_repr
            ))
        else:
            await ctx.send(embed=Embed(
                type='rich',
                color=Colour.brand_green(),
                title='Already in queue',
                description=play_config.track_repr
            ))
            return

        if not voice_client.is_playing():
            _, play_config = playlist.popitem(last=False)
            voice_client.play(PCMVolumeTransformer(FFmpegPCMAudio(**play_config.config), volume=VOLUME), after=lambda err: self._play_next_track(ctx))
            await ctx.send(embed=Embed(
                type='rich',
                color=Colour.brand_green(),
                title='Now playing',
                description=play_config.track_repr
            ))

    def _play_next_track(self, ctx):
        voice_client = self._get_voice_client_by_guild(self.bot, ctx.guild)
        playlist = self._playlists[ctx.guild.id]

        if playlist:
            _, play_config = playlist.popitem(last=False)

            voice_client.play(PCMVolumeTransformer(FFmpegPCMAudio(**play_config.config), volume=VOLUME), after=lambda err: self._play_next_track(ctx))
            asyncio.run_coroutine_threadsafe(
                ctx.send(embed=Embed(
                    type='rich',
                    color=Colour.brand_green(),
                    title='Now playing',
                    description=play_config.track_repr
                )),
                self.bot.loop
            )

    @staticmethod
    def _get_voice_client_by_guild(bot, guild):
        for voice_client in bot.voice_clients:
            if voice_client.guild == guild:
                return voice_client

        raise RuntimeError(f"Can't find voice client for guild `{guild}`")

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
            await ctx.send(embed=Embed(
                type='rich',
                color=Colour.brand_green(),
                title='Error',
                description='You\'re not in a voice channel'
            ))

        else:
            play_config, err_msg = self._sources[source].get_config(link, ctx.author.name)
            if err_msg:
                await ctx.send(embed=Embed(
                type='rich',
                color=Colour.brand_green(),
                title='Error',
                description=err_msg
            ))

            else:
                await self._play_track(ctx, voice_client, play_config)

    @commands.command(name="stop", aliases=("s",))
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()
        self._playlists[ctx.guild.id] = OrderedDict()

    @commands.command(name="next", aliases=("n",))
    async def next(self, ctx):
        await ctx.send(embed=Embed(
                type='rich',
                color=Colour.brand_green(),
                title='Info',
                description='Skipping track'
            ))
        await ctx.voice_client.stop()
        await self._play_next_track(ctx)

    @commands.command(name="queue", aliases=("q",))
    async def queue(self, ctx):
        msg = "\n".join([f"{n+1}. {cfg.track_repr}" for n, cfg in enumerate(self._playlists[ctx.guild.id].values())]) or 'Queue is empty'

        await ctx.send(embed=Embed(
                type='rich',
                color=Colour.brand_green(),
                title='Queue',
                description=msg
            ))

    @commands.command(name="jump", aliases=("j",))
    async def jump(self, ctx):
        ctx.send("Not implemented yet. Contact bot maintainer for more info")
        print("BasePlayer.jump")

    @commands.command(name="help", aliases=("h",))
    async def help(self, ctx):
        ctx.send(embed=Embed(
                type='rich',
                color=Colour.brand_green(),
                title='Usage',
                description='\n'.join([
                    '-p (-play) <youtube link>   play song',
                    '-q (-queue)                 show queue',
                    '-n (-next)                  skip current song',
                    '-s (-stop)                  exit voice',
                    '-h (-help)                  show this message',
                ])
            ))
