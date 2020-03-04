import discord
import json
import os
from discord.ext import commands
import asyncio
import botsetup
from botsetup import token

TOKEN = token()
client = commands.Bot(command_prefix = ".")
client.remove_command('help')
os.chdir(r'D:\coding\Klaybot')
