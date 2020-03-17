import configparser
import random

import discord

from discord.ext import commands


INIFILE = 'klaybot.ini'
CHAN_ID = 547539142808961072
TEXT_CHAN_ID = 685038704322281481  # test2 text chan
VOICE_CHAN_ID = 547863579039236097


bot = commands.Bot(command_prefix='.')
bot.remove_command('help')


def get_discord_token(inifile):
    config = configparser.ConfigParser()
    config.read(inifile)
    return config['discord']['token']


@bot.event
async def on_ready():
    #game = discord.Game("La programmation... Aie")
    watch = discord.Activity(type=discord.ActivityType.watching, name="programmer... Aie")
    await bot.change_presence(activity=watch)
    channel = bot.get_channel(CHAN_ID)
    await channel.send('Klaybot est actuellement en ligne, tapez .help pour avoir la liste des commandes')
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

@bot.command(pass_context=True, name='help')
async def help(ctx):
    author = ctx.message.author
    em = discord.Embed(
        title="Fenêtre d'aide de Klaybot",
        colour=discord.Colour.orange()
    )

    em.set_author(name='Help')
    em.add_field(name='.ping',
                 value='Renvoie Pong! :ping_pong:',
                 inline=False)
    em.add_field(name='.echo',
                 value='Renvoi la phrase dites',
                 inline=False)
    em.add_field(name='.clear x',
                 value='Permet de nettoyer les x dernières lignes du chat',
                 inline=False)
    em.add_field(name='.roll_dice x y',
                 value='Effectue un lancer de x dés dont le chiffre est comprit de 1 à y ',
                 inline=False)


@bot.event
async def on_voice_state_update(member, before, after):
    guild = member.guild
    clone_channel = ''
    list_clone = []
    list_pos = 0
    channel = bot.get_channel(TEXT_CHAN_ID)  # On choisit notre salon textuel test2 dont l'ID est connue
    voicechannel = bot.get_channel(VOICE_CHAN_ID)  # On choisit notre salon vocal qu'on veut dupliquer
    if before.channel in list_clone:
        list_pos = list_clone.index(before.channel)
    if after.channel and after.channel == voicechannel and before.channel != voicechannel:
        # On crée un nouveau canal vocal
        clone_channel = await guild.create_voice_channel(f'{voicechannel.name} {member.name}',
                                                         user_limit=5, position=4,
                                                         category=bot.get_channel(547862839369531411))
        list_clone.append(clone_channel)
        await channel.send(f"{member.name} a rejoint le canal {voicechannel.name} et créé le canal {clone_channel}")
        await member.edit(voice_channel=clone_channel)  # On déplace le membre qui a rejoint le canal dans le nouveau canal vocal créé
    if before.channel and before.channel == list_clone[list_pos] and after.channel !=list_clone[list_pos] and len(list_clone[list_pos].members)==0:
        await channel.send(f"{member.name} a quitté le canal {list_clone[list_pos]}")
        await list_clone[list_pos].delete()
        del list_clone[list_pos]


if __name__ == '__main__':
    bot.run(get_discord_token(INIFILE))
