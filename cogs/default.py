from discord.ext import commands

from settings import ALLOWED_GUILD_IDS


class DefaultCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Cog `{self.__class__.__name__}` ready')

    def bot_check(self, ctx):
        return ctx.guild.id in ALLOWED_GUILD_IDS
