import traceback
from datetime import datetime
import discord
from discord.ext import commands
import json


def getConfig(path):
    configFile = open(path, "r")
    return json.loads(configFile.read())


config = getConfig("config.json")


prefix = "!"
bot = commands.Bot(command_prefix=config["prefix"], description="Welcome to PradaBot!\nCommands are below:",
                   case_insensitive=True)

initial_extensions = [
    'Fun',
    'Audio',
    "Basics",
    "Replies",
    "Memevoting"
]


@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.send('This command cannot be used in private messages.')
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send('Sorry. This command is disabled and cannot be used.')


@bot.event
async def on_ready():
    print("Everything's all ready to go~")
    print(f'Logged in as: {bot.user.name} with id: {bot.user.id}')
    print('-' * 50)
    await bot.change_presence(activity=discord.Activity(type=2, name='the birds sing :-]'))
    bot.uptime = datetime.now()


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    time = datetime.now().strftime("%I:%M %p")

    print("\nMESSAGE\n-------\n"
          "Content     : {0.content}\n"
          "Author      : {0.author}\n"
          "Text channel: {0.channel}\n"
          "Guild       : {0.guild}\n"
          "Time        : {1}\n".format(message, time))

    await bot.process_commands(message)


@bot.event
async def on_command(ctx):
    pass


if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            print(f"Loading {extension}...")
            bot.load_extension("cogs." + extension)
        except Exception as e:
            print(traceback.format_exc())


bot.run(config["token"])
