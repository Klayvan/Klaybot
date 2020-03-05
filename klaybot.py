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
    guild = member.guild
    voicechannel = client.get_channel(547863579039236097)
    if after.channel and after.channel == voicechannel and before.channel != voicechannel:
        await guild.create_voice_channel(f'{voicechannel.name} {member.name}')
        #await member.edit(voice_channel=f'{voicechannel.name} {member.name}')


client.run(tokendiscord.getToken())