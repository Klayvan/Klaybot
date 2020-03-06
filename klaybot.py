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
    channel = client.get_channel(547539142808961072)
    await channel.send('Klaybot est actuellement en ligne, tapez .help pour avoir la liste des commandes')
    print('Klaybot est en ligne.')

cmd = Cmds(client)
cmd.ping()
cmd.roll_dice()
cmd.echo()
cmd.clear()
cmd.help()

newChannel = ''

@client.event
async def on_voice_state_update(member, before, after):
    guild = member.guild
    global newChannel
    channel = client.get_channel(685038704322281481) #On choisit notre salon textuel test2 dont l'ID est connue
    voicechannel = client.get_channel(547863579039236097) #On choisit notre salon vocal qu'on veut dupliquer
    if after.channel and after.channel == voicechannel and before.channel != voicechannel:
        newChannel = await guild.create_voice_channel(f'{voicechannel.name} {member.name}', user_limit=5, category=client.get_channel(547862839369531411), position=4) #On crée un nouveau canal vocal
        await channel.send(f"{member.name} a rejoint le canal {voicechannel.name} et créé le canal {newChannel}")
        await member.edit(voice_channel=newChannel) #On déplace le membre qui a rejoint le canal dans le nouveau canal vocal créé
    if before.channel == newChannel and after.channel !=newChannel and len(newChannel.members)==0:
        await channel.send(f"{member.name} a quitté le canal {newChannel}")
        await newChannel.delete()


client.run(tokendiscord.getToken())