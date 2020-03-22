import discord
import json
import os
import random
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix = '?')
client.remove_command('help')

status = cycle(['?help'])


@client.event
async def on_ready():
    change_status.start()
    print('Client On.')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('That command doesnt exist! Try `?help`')

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Cleared `{amount}` messages!')

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        responses = ['10', '42', '1', '9', '7', '100', '20', '78', '90', '21', '52']
        await ctx.send(f'Please specify an amount of messages you want to delete!\nExample: **?clear {random.choice(responses)}**')

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'Sorry `{ctx.message.author}`, You are not admin!')

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked **{member}** for **{reason}**.')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'Sorry `{ctx.message.author}`, You cannot kick members!')

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    memeber_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user=ban_entry.user

        if (user.name, user.discriminator) == (memeber_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned **{user.name}#{user.discriminator}**.')
@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'Sorry `{ctx.message.author}`, You cannot unban members!')

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned **{member}** for **{reason}**.')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'Sorry `{ctx.message.author}`, You cannot ban members!')

@client.command()
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour=discord.Colour.blue()
    )
    embed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
    embed.add_field(name="**Fun**", value="`?8ball <Question>`\n`?say <text>`", inline=True)
    embed.add_field(name="**Moderation**", value="`?kick <@user>`\n`?ban <@user>`\n`?unban <user#usersnumbers>`\n`?clear <number>`", inline=True)
    embed.set_footer(text="© 2020 HappyBat")
    await ctx.send(embed=embed)

@client.command()
async def info(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour=discord.Colour.blue()
    )
    embed.add_field(name="**Developer(s)**", value="HappyBat#1189", inline=True)
    embed.add_field(name="**Python**", value="[3.8.2](https://pypi.org/project/discord.py/)", inline=True)
    embed.add_field(name="**Bot Version**", value="1.9.0", inline=True)
    embed.add_field(name="**Made With**", value="[Visual Studio Code](https://code.visualstudio.com/download)", inline=True)
    embed.add_field(name="****", value="")
    embed.add_field(name="**About This Bot**", value="This bot is an open source bot made by [HappyBat]()")
    embed.set_footer(text="© 2020 HappyBat")
    await ctx.send(embed=embed)
    

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('YOUR TOKEN HERE!')
