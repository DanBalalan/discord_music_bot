import os
import discord
from dotenv import load_dotenv

from arg_checker import ArgChecker
from music_sources.restreamer_dispatcher import RestreamerDispatcher
import settings


load_dotenv('env.py', override=True)
client = discord.Client()
restreamer_dispatcher = RestreamerDispatcher()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    # if message.author == client.user:
    #     return

    splitted = message.content.split(settings.SPLIT_CHAR)
    if splitted[0] in settings.COMMANDS_MAP:
        # TODO: прикрутить подключение к войсчату и стриминг через music_sources.restreamers
        command = splitted[0]
        actual_args = splitted[1:]
        actual_args = [None] if not actual_args else actual_args

        func_name, required_arg_types = settings.COMMANDS_MAP[splitted[0]]
        ArgChecker.check(actual_args, required_arg_types)
        restreamer_class = restreamer_dispatcher.get_restreamer_class(*actual_args)()
        getattr(restreamer_class, func_name)()
        await message.channel.send(f'{command}\n{func_name}')

client.run(os.environ['BOT_KEY'])
