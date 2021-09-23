from discord.ext import commands

from converters import GuildLinkSplitter


@commands.command(name='play', aliases=('p', ))
async def play(ctx, *, link_or_name: GuildLinkSplitter):
    if not link_or_name:
        return

    await ctx.send(link_or_name)


all_commands = [play]
