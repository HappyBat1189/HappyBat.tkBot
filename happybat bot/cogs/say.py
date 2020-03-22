import discord
from discord.ext import commands

class Say(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Commands loaded')
        print('Ready to use!')
        print('Enjoy! Made by HappyBat.')

    @commands.command()
    async def say(self, ctx):
        await ctx.send('No')

def setup(client):
    client.add_cog(Say(client))