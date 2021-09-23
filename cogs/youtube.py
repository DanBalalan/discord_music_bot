from discord.ext import commands

from converters import GuildLinkSplitter
from .base_player import BasePlayer


class YoutubeCog(BasePlayer):

    @commands.command(name='play', aliases=('p',))
    async def play(self, ctx, *, arg: GuildLinkSplitter):
        guild_id, link = arg
        if not self._playlist.get(guild_id):
            self._playlist[guild_id] = [link]
        else:
            self._playlist[guild_id].append(link)

        await ctx.send(f'{type(self).__name__} play: {arg}')
