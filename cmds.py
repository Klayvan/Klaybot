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