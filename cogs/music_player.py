from discord.ext import commands
from converters import SourceDetector


class MusicPlayer(commands.Cog):

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

        await ctx.send(f'{type(self).__name__} source: {source}, link: {link}')

    @commands.command(name='stop', aliases=('s',))
    async def stop(self, ctx):
        print('BasePlayer.stop')

    @commands.command(name='next', aliases=('n',))
    async def next(self, ctx):
        print('BasePlayer.next')

    @commands.command(name='exit', aliases=('e',))
    async def exit(self, ctx):
        print('BasePlayer.exit')

    @commands.command(name='queue', aliases=('q',))
    async def queue(self, ctx):
        print('BasePlayer.queue')

    @commands.command(name='jump', aliases=('j',))
    async def jump(self, ctx):
        print('BasePlayer.jump')

    @property
    def _playlist_attr_name(self):
        return f'_{type(self).__name__.lower()}_playlist'

    @property
    def _playlist(self):
        return getattr(self, self._playlist_attr_name)
