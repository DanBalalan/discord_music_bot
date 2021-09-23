import os
from discord.ext import commands
from dotenv import load_dotenv

from cogs import all_cogs

load_dotenv('env.py', override=True)

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(os.environ['COMMAND_PREFIX']),
    description=None
)

for cog in all_cogs:
    bot.add_cog(cog(bot))


bot.run(os.environ['BOT_KEY'])
