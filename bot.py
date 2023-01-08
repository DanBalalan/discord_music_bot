import asyncio
import os

from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

from cogs import all_cogs

load_dotenv('env.py', override=True)

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(os.environ['COMMAND_PREFIX']),
    description=None,
    intents=Intents.all()
)

# for cog in all_cogs:
#     bot.add_cog(cog(bot))

# bot.run(os.environ['BOT_KEY'])

async def main():
    async with bot:
        for cog in all_cogs:
            await bot.add_cog(cog(bot))

        await bot.start(os.environ['BOT_KEY'])


asyncio.run(main())
