import discord
import json
import os
from discord.ext import commands
import asyncio
from cmds import Cmds

def read_token():
    with open ("token.ini","r") as f:
        lines = f.readlines()
        return lines[0].strip()

TOKEN = read_token()
client = commands.Bot(command_prefix = ".")
client.remove_command('help')
os.chdir(r'D:\coding\Klaybot')

@client.event
async def on_ready():
    print('Klaybot est en ligne.')

@client.command()
async def ping(ctx):
    await ctx.send('Pong! :ping_pong:')

client.run(TOKEN)
