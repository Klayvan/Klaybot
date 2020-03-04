import discord
from discord.ext import commands

class Cmds:
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self,ctx):
        await ctx.send('Pong! :ping_pong:')