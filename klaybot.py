import configparser
import random

import discord

from discord import app_commands
from discord.ext import commands

intents = discord.Intents().all()

intents.message_content = True
intents.guilds = True
intents.members = True

INIFILE = 'klaybot.ini'


bot = commands.Bot(command_prefix='.', intents=intents)
bot.remove_command('help')


def get_discord_token(inifile):
    config = configparser.ConfigParser()
    config.read(inifile)
    return config['discord']['token']

# Stocke l'ID du canal vocal temporaire
temporary_channel_id = None
@bot.event
async def on_ready():
    watch = discord.Activity(type=discord.ActivityType.watching,
                             name="Evolution de la machine")
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

@bot.event
async def on_voice_state_update(member, before, after):
    global temporary_channel_id
    
    # Vérifie si le membre s'est connecté au canal vocal spécifié
    if after.channel is not None and after.channel.id == 1130824483905736777:
        guild = member.guild  # Récupère le serveur (guild) où l'événement a eu lieu
        
        # Vérifie si le canal vocal temporaire existe déjà
        if temporary_channel_id is None:
            # Crée un nouveau canal vocal temporaire en dupliquant le canal spécifié
            original_channel = guild.get_channel(1130824483905736777)
            new_channel = await original_channel.clone(name=f"{original_channel.name}-{member.name}")
            
            # Stocke l'ID du canal vocal temporaire
            temporary_channel_id = new_channel.id
        
        # Déplace le membre vers le canal vocal temporaire
        temporary_channel = guild.get_channel(temporary_channel_id)
        await member.move_to(temporary_channel)
        
    # Vérifie si tous les membres sont sortis du canal vocal temporaire
    if after.channel is None and temporary_channel_id is not None:
        guild = member.guild
        temporary_channel = guild.get_channel(temporary_channel_id)
        
        if all(member.voice.channel == 0 for member in temporary_channel.members):
            # Supprime le canal vocal temporaire
            await temporary_channel.delete()
            temporary_channel_id = None


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
