from discord.ext import commands


class DefaultCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user}')

    def bot_check(self, ctx):
        return ctx.guild is not None
