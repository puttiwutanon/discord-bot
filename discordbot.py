import discord
from discord.ext import commands
from discord import guild
import random

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print("the bot is ready")

@client.command()
async def hello(ctx):
    await ctx.send("hello, welcome")

@client.event
async def on_member_join(member):
    channel = client.get_channel(1093168046404800685)
    await channel.send(f'{member} has joined')
#this function would say that a member have entered the server

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1093168046404800685)
    await channel.send(f'{member} has left')
#this function would say that a member have left the server

@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        ctx.send("you are not in a voice channel, to use this command you must be in a voice channel")

@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("i have left the voice channel")
    else:
        await ctx.send("you are not in a voice channel")

@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
#this command is for kicking members out of your discord server

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'banned {member}')
#this command is for banning users

@client.event
async def on_message(message):
    if message.content == "fuck": #in this line if you want to add more words just type ,"your words" after "fuck"
        await message.delete()
        await message.channel.send("don't say that again")

@client.command()
async def warn(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.administrator:
        if reason is None:
            await member.send(f"You have been warned in {ctx.guild.name} by {ctx.author.display_name}.")
            await ctx.send(f"{member.mention} has been warned.")
        else:
            await member.send(f"You have been warned in {ctx.guild.name} by {ctx.author.display_name} for {reason}.")
            await ctx.send(f"{member.mention} has been warned for {reason}.")
    else:
        await ctx.send("You do not have the required permissions to use this command.")



client.run('MTA5MzcwMjQ1NjQ5NzY4NDU2Mg.GnZgF-.Pmzb6c8dUNnsLbKWOJdeoTkoQ9VLdEjFr7FKVE')
#in the line above put in your token
