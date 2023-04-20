import discord
from discord.ext import commands
from discord import guild
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext import tasks
import asyncio
from datetime import datetime
from discord import Option
from datetime import timedelta
from discord import Permissions, channel, guild, utils
from discord import ui
from discord.utils import get

bot = commands.Bot()

servers = [1093168046404800682]

warn_counts = {}

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online ,activity=discord.Game('ur mom'))
    print("the bot is ready")

@bot.slash_command(name='kick', description='kicks users')
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason == None:
        reason = "no reason provided"
    await ctx.guild.kick(member)
    await ctx.send(f'User {member} has kicked.')

@bot.slash_command(name='ban', description='ban users')
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'banned {member}')

@bot.slash_command(name='warn', description='warn users')
async def warn(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.administrator:
        
        if ctx.guild.id not in warn_counts:
            warn_counts[ctx.guild.id] = {}
        if member.id not in warn_counts[ctx.guild.id]:
            warn_counts[ctx.guild.id][member.id] = 0
        warn_counts[ctx.guild.id][member.id] += 1

        if reason is None:
            embed = discord.Embed(title="User Warning", description=f"{member.mention} has been warned by {ctx.author.display_name}.", color=discord.Color.red())
            await ctx.send(embed=embed)
            await member.send(f"You have been warned in {ctx.guild.name} by {ctx.author.display_name}.")
        else:
            embed = discord.Embed(title="User Warning", description=f"{member.mention} has been warned by {ctx.author.display_name} for {reason}.", color=discord.Color.red())
            await ctx.send(embed=embed)
            await member.send(f"You have been warned in {ctx.guild.name} by {ctx.author.display_name} for {reason}.")
    else:
        await ctx.send("You do not have the required permissions to use this command.")

@bot.slash_command(name='warnlist', description='Show the warn list for a user.')
async def warnlist(ctx, member: discord.Member):
    if ctx.author.guild_permissions.administrator:
        if ctx.guild.id not in warn_counts or member.id not in warn_counts[ctx.guild.id]:
            warn_count = 0
        else:
            warn_count = warn_counts[ctx.guild.id][member.id]
        embed = discord.Embed(title="Warn List", description=f"{member.mention} has {warn_count} warns in {ctx.guild.name}.", color=discord.Color.orange())
        await ctx.send(embed=embed)
    else:
        await ctx.send("You do not have the required permissions to use this command.")

@bot.slash_command(name='remove_warn', description='Remove a certain number of warns from a user.')
async def remove_warn(ctx, member: discord.Member, amount: int):
    if ctx.author.guild_permissions.administrator:
        # Get the member's warn count and decrement it by the specified amount
        if ctx.guild.id not in warn_counts or member.id not in warn_counts[ctx.guild.id]:
            warn_count = 0
        else:
            warn_count = warn_counts[ctx.guild.id][member.id]
        warn_count -= amount
        if warn_count < 0:
            warn_count = 0
        if ctx.guild.id not in warn_counts:
            warn_counts[ctx.guild.id] = {}
        warn_counts[ctx.guild.id][member.id] = warn_count
        
        embed = discord.Embed(title="Warn Removal", description=f"{amount} warns have been removed from {member.mention}'s warn list by {ctx.author.display_name}.", color=discord.Color.green())
        await ctx.send(embed=embed)
    else:
        await ctx.send("You do not have the required permissions to use this command.")

    

@bot.slash_command(guild_ids = servers, name = 'timeout', description = "mutes/timeouts a member")
@commands.has_permissions(moderate_members = True)
async def timeout(ctx, member: Option(discord.Member, required = True), reason: Option(str, required = False), days: Option(int, max_value = 27, default = 0, required = False), hours: Option(int, default = 0, required = False), minutes: Option(int, default = 0, required = False), seconds: Option(int, default = 0, required = False)): #setting each value with a default value of 0 reduces a lot of the code
    if member.id == ctx.author.id:
        await ctx.respond("You can't timeout yourself!")
        return
    if member.guild_permissions.moderate_members:
        await ctx.respond("You can't do this, this person is a moderator!")
        return
    duration = timedelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
    if duration >= timedelta(days = 28): #added to check if time exceeds 28 days
        await ctx.respond("I can't mute someone for more than 28 days!", ephemeral = True) #responds, but only the author can see the response
        return
    if reason == None:
        await member.timeout_for(duration)
        await ctx.respond(f"<@{member.id}> has been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}>.")
    else:
        await member.timeout_for(duration, reason = reason)
        await ctx.respond(f"<@{member.id}> has been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}> for '{reason}'.")

@bot.slash_command(guild_ids = servers, name = 'remove_timeout', description = "unmutes/untimeouts a member")
@commands.has_permissions(moderate_members = True)
async def remove_timeout(ctx, member: Option(discord.Member, required = True), reason: Option(str, required = False)):
    if reason == None:
        await member.remove_timeout()
        await ctx.respond(f"<@{member.id}> has been untimed out by <@{ctx.author.id}>.")
    else:
        await member.remove_timeout(reason = reason)
        await ctx.respond(f"<@{member.id}> has been untimed out by <@{ctx.author.id}> for '{reason}'.")

@bot.slash_command(guild_ids=servers, name="giverole", description="Give a role to a member")
@commands.has_permissions(manage_roles=True)
async def giverole(ctx, member: Option(discord.Member, required=True), role: discord.Role):
    try:
        await member.add_roles(role)
        await ctx.send(f"Added role {role.name} to {member.display_name}")
    except discord.Forbidden:
        await ctx.send("I don't have permission to add that role.")
    except discord.HTTPException:
        await ctx.send("Failed to add role due to an error.")
#if the role is adminstrator it will error

@bot.slash_command(guild_ids=servers, name="removerole", description="Remove a role from a member")
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member: Option(discord.Member, required=True), role: discord.Role):
    try:
        await member.remove_roles(role)
        await ctx.send(f"Removed role {role.name} from {member.display_name}")
    except discord.Forbidden:
        await ctx.send("I don't have permission to remove that role.")
    except discord.HTTPException:
        await ctx.send("Failed to remove role due to an error.")

@bot.slash_command(name="help", description="Show help message about the available commands.")
async def help(ctx):
    embed = discord.Embed(title="Available Commands", color=discord.Color.blue())
    embed.add_field(name="/kick", value="Kicks a member from the server.", inline=False)
    embed.add_field(name="/ban", value="Bans a member from the server.", inline=False)
    embed.add_field(name="/warn", value="Warns a member in the server.", inline=False)
    embed.add_field(name="/warnlist", value="Shows the warn list for a member in the server.", inline=False)
    embed.add_field(name="/remove_warn", value="Removes a certain number of warns from a member in the server.", inline=False)
    embed.add_field(name="/timeout", value="Mutes/Timeouts a member in the server.", inline=False)
    embed.add_field(name="/remove_timeout", value="removes Mutes/Timeouts a member in the server.", inline=False)
    embed.add_field(name="/giverole", value="give roles a member in the server.", inline=False)
    embed.add_field(name="/removerole", value="removes a role to a member in the server.", inline=False)
    await ctx.send(embed=embed)

@bot.slash_command(name='purge', description='delete the message above')
async def clear(ctx, amount= 2):
    await ctx.channel.purge(limit=amount)

@bot.slash_command(name="create_poll", description="creates a poll")
async def poll(ctx, question, option1=None, option2=None):
  if option1==None and option2==None:
    await ctx.channel.purge(limit=1)
    message = await ctx.send(f"```New poll: \n{question}```\n**✅ = Yes**\n**❎ = No**")
    await message.add_reaction('❎')
    await message.add_reaction('✅')
  elif option1==None:
    await ctx.channel.purge(limit=1)
    message = await ctx.send(f"```New poll: \n{question}```\n**✅ = {option1}**\n**❎ = No**")
    await message.add_reaction('❎')
    await message.add_reaction('✅')
  elif option2==None:
    await ctx.channel.purge(limit=1)
    message = await ctx.send(f"```New poll: \n{question}```\n**✅ = Yes**\n**❎ = {option2}**")
    await message.add_reaction('❎')
    await message.add_reaction('✅')
  else:
    await ctx.channel.purge(limit=1)
    message = await ctx.send(f"```New poll: \n{question}```\n**✅ = {option1}**\n**❎ = {option2}**")
    await message.add_reaction('❎')
    await message.add_reaction('✅')

bot.run('add token')