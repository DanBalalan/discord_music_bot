from importlib import import_module

from discord.ext import commands
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from converters import SourceDetector


class MusicPlayer(commands.Cog):
    voice_client = None

    def __init__(self, bot):
        self.bot = bot
        setattr(self, self._playlist_attr_name, dict())  # {<guild_id>: [<song0_link>, <song1_link>]}

    @commands.command(name='play', aliases=('p',))
    async def play(self, ctx, *, arg: SourceDetector):
        source, link = arg

        if not self._playlist.get(ctx.guild.id):
            self._playlist[ctx.guild.id] = [link]
        else:
            self._playlist[ctx.guild.id].append(link)

        if not ctx.author.voice:
            await ctx.send(f'You\'re not in a voice channel')
        else:
            if not self.voice_client or not self.voice_client.is_playing():
                await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_deaf=True)
                self.voice_client = await ctx.author.voice.channel.connect(timeout=10)
                play_config, title = import_module(f'cogs.music_sources.{source}').get_config(self._playlist[ctx.guild.id][0])
                await ctx.send(f'Now playing {title}')
                self.voice_client.play(FFmpegPCMAudio(**play_config))

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
        await ctx.send(f'Queue:\n{self._playlist[ctx.guild.id]}')

    @commands.command(name='jump', aliases=('j',))
    async def jump(self, ctx):
        print('BasePlayer.jump')

    @property
    def _playlist_attr_name(self):
        return f'_{type(self).__name__.lower()}_playlist'

    @property
    def _playlist(self):
        return getattr(self, self._playlist_attr_name)
