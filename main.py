import discord
from discord import member
from discord import guild
from discord import emoji
from discord.ext import commands
from config import *
import datetime
from datetime import datetime
from game import *


bot = commands.Bot(command_prefix=PREFIX,description="Tic-Tac-Toe Bot")

@bot.event

async def on_ready():
    print("I am alive vro !")

@bot.event

async def on_raw_reaction_add(payload):
    ourMessageID = 914884325621788712

    if payload.message_id == ourMessageID:
        member = payload.member
        guild = member.guild
        emoji = payload.emoji.name
        
        if emoji == '🟦':
            role = discord.utils.get(guild.roles,name="Blue")
        
        elif emoji == '🟥':
            role = discord.utils.get(guild.roles,name="Red")
        
        elif emoji == '🎮':
            role = discord.utils.get(guild.roles,name="Game")
        
        await member.add_roles(role)
        
@bot.event

async def on_raw_reaction_remove(payload):
    ourMessageID = 914884325621788712

    if payload.message_id == ourMessageID:
        guild = await(bot.fetch_guild(payload.guild_id))
        emoji = payload.emoji.name
        if emoji == '🟦':
            role = discord.utils.get(guild.roles,name="Blue")
        elif emoji == '🟥':
            role = discord.utils.get(guild.roles,name="Red")
        elif emoji == '🎮':
            role = discord.utils.get(guild.roles,name="Game")
        
        member = await(guild.fetch_member(payload.user_id))
        
        if member is not None:
            await member.remove_roles(role)
        
        else:
            print("Member Not found")


@bot.command(pass_context=True)

async def hello(ctx, name: str):
    await ctx.send(f'Hello {name} vmro!')

@bot.command(pass_context=True)

async def bye(ctx):
    embed =  discord.Embed(
        title="Welcome to Tic-Tac-Toe Game",
        description = "I am a Game Bot you can use to play Tic-Tac-Toe ",
        timestamp = datetime.now(),
         )
    
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('🟥')
    await msg.add_reaction('🟦')
   
    await msg.add_reaction('🎮')

@bot.command(pass_context=True)

async def clear(ctx,amount:str):
    if amount == 'all':
        await ctx.channel.purge()
    else:
        await ctx.channel.purge(limit=(int(amount) +1))

@bot.command(pass_context=True)
@commands.has_role("Game")
async def game(ctx):
    await LoadGame(ctx,bot)




bot.run(TOKEN,bot=True,reconnect=True)



