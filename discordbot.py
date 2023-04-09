import discord
from discord.ext import commands

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
    await channel.send("hello")

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1093168046404800685)
    await channel.send("goodbye")

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

client.run('MTA5MzcwMjQ1NjQ5NzY4NDU2Mg.GlJ-nM.y5JNB6ex8vNpk69KXwkE3iwawy04KMxQaEf8X4')
