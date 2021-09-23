from discord.ext import commands
from settings import sources_detector


# Default source for search-and-play
DEFAULT_SOURCE = 'youtube'


class SourceDetector(commands.Converter):
    async def convert(self, ctx, argument):
        if argument.startswith('http'):
            for source in sources_detector:
                if source in argument:
                    return sources_detector[source], argument
            return None, argument
        else:
            return DEFAULT_SOURCE, argument
