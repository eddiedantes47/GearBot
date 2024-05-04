import discord
from discord.ext import commands

class PingPongCog(commands.Cog, name="PingPong"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Responds with 'Pong!'"""
        await ctx.send('Pong!')

    @commands.command(name='pong')
    async def pong(self, ctx):
        """Responds with 'Ping!'"""
        await ctx.send('Ping!')

async def setup(bot):
    await bot.add_cog(PingPongCog(bot))
