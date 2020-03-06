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

clone_channel = ''
list_clone = []

@client.event
async def on_voice_state_update(member, before, after):
    guild = member.guild
    global clone_channel
    global list_clone
    channel = client.get_channel(685038704322281481) #On choisit notre salon textuel test2 dont l'ID est connue
    voicechannel = client.get_channel(547863579039236097) #On choisit notre salon vocal qu'on veut dupliquer
    if before.channel in list_clone:
        list_pos = list_clone.index(before.channel)
    if after.channel and after.channel == voicechannel and before.channel != voicechannel:
        clone_channel = await guild.create_voice_channel(f'{voicechannel.name} {member.name}', user_limit=5, category=client.get_channel(547862839369531411), position=4) #On crée un nouveau canal vocal
        list_clone.append(clone_channel)
        await channel.send(f"{member.name} a rejoint le canal {voicechannel.name} et créé le canal {clone_channel}")
        await member.edit(voice_channel=clone_channel) #On déplace le membre qui a rejoint le canal dans le nouveau canal vocal créé
    if before.channel and before.channel == list_clone[list_pos] and after.channel !=list_clone[list_pos] and len(list_clone[list_pos].members)==0:
        await channel.send(f"{member.name} a quitté le canal {list_clone[list_pos]}")
        await list_clone[list_pos].delete()
        del list_clone[list_pos]


client.run(tokendiscord.getToken())