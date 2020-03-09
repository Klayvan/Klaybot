import configparser
import random

import discord

from discord.ext import commands


INIFILE = 'klaybot.ini'


bot = commands.Bot(command_prefix='.')
bot.remove_command('help')


def get_discord_token(inifile):
    config = configparser.ConfigParser()
    config.read(inifile)
    return config['discord']['token']


@bot.event
async def on_ready():
    watch = discord.Activity(type=discord.ActivityType.watching,
                             name="programmer... Aie")
    await bot.change_presence(activity=watch)
    print('Klaybot est en ligne.')


@bot.command(name='ping')
async def ping(ctx):
    message = 'Pong! :ping_pong:'
    response = message
    await ctx.send(response)


@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll_dice(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(','.join(dice))


@bot.command(name='echo')
async def echo(ctx, *, content: str):
    await ctx.send(content)


@bot.command(pass_context=True, name='clear')
@commands.has_role('Master')
async def clear(ctx, *, amount: int):
    channel = ctx.channel
    messages = []
    async for message in channel.history(limit=amount+1):
        messages.append(message)
    await channel.delete_messages(messages)
    await ctx.send("Notre chat a été nettoyé")

@bot.command(pass_context=True, name='help')
async def help(ctx):
    author = ctx.message.author


    em = discord.Embed(
        title = "Fenêtre d'aide de Klaybot",
        colour = discord.Colour.orange()
    )

    em.set_author(name='Help')
    em.add_field(name='.ping', value='Renvoie Pong! :ping_pong:', inline=False)
    em.add_field(name='.echo', value='Renvoi la phrase dites', inline = False)
    em.add_field(name='.clear x', value='Permet de nettoyer les x dernières lignes du chat', inline = False)
    em.add_field(name='.roll_dice x y', value='Effectue un lancer de x dés dont le chiffre est comprit de 1 à y ', inline = False)

    await author.send(embed=em)

if __name__ == '__main__':
    bot.run(get_discord_token(INIFILE))
