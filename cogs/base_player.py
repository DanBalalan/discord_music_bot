from discord.ext import commands
from abc import abstractmethod


class BasePlayer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        setattr(self, self._playlist_attr_name, dict())  # {<guild_id>: <playlist>}

    @abstractmethod
    async def play(self, ctx, *, args):
        # TODO:
        pass

    @commands.command(name='stop', aliases=('s',))
    async def stop(self):
        print('BasePlayer.stop')

    @commands.command(name='next', aliases=('n',))
    async def next(self):
        print('BasePlayer.next')

    @commands.command(name='exit', aliases=('e',))
    async def exit(self):
        print('BasePlayer.exit')

    @commands.command(name='queue', aliases=('q',))
    async def queue(self):
        print('BasePlayer.queue')

    @commands.command(name='jump', aliases=('j',))
    async def jump(self):
        print('BasePlayer.jump')

    @property
    def _playlist_attr_name(self):
        return f'_{type(self).__name__.lower()}_playlist'

    @property
    def _playlist(self):
        return getattr(self, self._playlist_attr_name)
