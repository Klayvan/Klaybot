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
    #game = discord.Game("La programmation... Aie")
    watch = discord.Activity(type=discord.ActivityType.watching, name="programmer... Aie")
    await client.change_presence(activity=watch)
    print('Klaybot est en ligne.')

cmd = Cmds(client)
cmd.ping()
cmd.roll_dice()
cmd.echo()
cmd.clear()

@client.event
async def on_voice_state_update(member, before, after):
    channel = client.get_channel(685038704322281481)
    voicechannel = client.get_channel(547863579039236097)
    if after.channel and after.channel == voicechannel and before.channel != voicechannel:
        await channel.send(f"Bienvenue dans le canal {voicechannel.name}")

client.run(tokendiscord.getToken())