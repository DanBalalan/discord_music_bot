from discord.ext import commands


class GuildLinkSplitter(commands.Converter):
    async def convert(self, ctx, argument):
        if argument.startswith('http'):
            pass
        else:
            pass
        return ctx.guild.id, argument  # сервер, ссылка
