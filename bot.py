import argparse
import asyncio

from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

from cogs import all_cogs
from settings import COMMAND_PREFIX


parser = argparse.ArgumentParser(description='Discord music bot')
parser.add_argument('-t', '--token', nargs='?', action='store', type=str, required=True, dest='token')
args = parser.parse_args()


bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(COMMAND_PREFIX),
    description=None,
    intents=Intents.all()
)

async def main():
    async with bot:
        for cog in all_cogs:
            await bot.add_cog(cog(bot))

        await bot.start(args.token)


asyncio.run(main())
