import os
import discord
from dotenv import load_dotenv

from arg_parser import ArgParser
from music_sources.restreamer_dispatcher import RestreamerDispatcher
import settings


load_dotenv('env.py', override=True)
client = discord.Client()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    splitted = message.content.split(settings.SPLIT_CHAR)
    if splitted[0] in settings.COMMANDS_MAP:
        # TODO: прикрутить подключение к войсчату и стриминг через music_sources.restreamers
        func_name, args_schema = settings.COMMANDS_MAP[splitted[0]]
        func_args = ArgParser.parse(splitted[1:], args_schema)
        restreamer_class = RestreamerDispatcher.get_restreamer_class(func_name, func_args)()
        getattr(restreamer_class, func_name)()
        await message.channel.send(f'{splitted[0]}\n{func_name}')

client.run(os.environ['BOT_KEY'])
