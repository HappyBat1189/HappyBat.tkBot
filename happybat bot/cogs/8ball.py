import discord
import random
from discord.ext import commands

class _8ball(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['8ball', '8b'])
    async def _8ball(self, ctx, *, question):
       responses = ['`Yes`',
                    '`Without a doubt`',
                    '`No`',
                    '`Maybe`',
                    '`Why even ask?!`',
                    '`I guess so...`',
                    '`Sure :P`',
                    '`Hell yeah!`',
                    '`Cannot predict now`']
       await ctx.send(f'**Question:** `{question}`\n**Answer:** `{random.choice(responses)}`')
        

def setup(client):
    client.add_cog(_8ball(client))