import discord
import json
import os
import random
from discord.ext import commands
import asyncio
from cmds import Cmds
from tokendiscord import Tokendiscord



if __name__ == '__main__':
    client = commands.Bot(command_prefix = ".")
    client.remove_command('help')
    tokendiscord = Tokendiscord()
    cmds = Cmds(client)

@client.event
async def on_ready():
    game = discord.Game("La programmation... Aie")
    watch = discord.Activity(type=discord.ActivityType.watching, name="programmer... Aie")
    await client.change_presence(activity=watch)
    print('Klaybot est en ligne.')

cmd = Cmds(client)
cmd.ping()
cmd.roll_dice()

client.run(tokendiscord.getToken())