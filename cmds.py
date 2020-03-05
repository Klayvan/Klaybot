import discord
import random
from discord.ext import commands

class Cmds:
    def __init__(self, client):
        self.client = client

    def ping(self):
        @self.client.command(name='ping')
        async def ping(ctx):
            message='Pong! :ping_pong:'
            response = message
            await ctx.send(response)

    def roll_dice(self):
        @self.client.command(name='roll_dice', help='Simulates rolling dice.')
        async def roll(ctx, number_of_dice: int, number_of_sides: int):
            dice = [
                str(random.choice(range(1, number_of_sides + 1)))
                for _ in range(number_of_dice)
            ]
            await ctx.send(','.join(dice))

    def echo(self):
        @self.client.command(name='echo')
        async def echo(ctx, * ,content:str):
            await ctx.send(content)

    def clear(self):
        @self.client.command(pass_context=True,name='clear')
        @commands.has_role('Master')
        async def clear(ctx, *,amount:int):
            channel = ctx.channel
            messages = []
            async for message in channel.history(limit=amount+1):
                messages.append(message)
            await channel.delete_messages(messages)
            await ctx.send("Notre chat a été nettoyé")
