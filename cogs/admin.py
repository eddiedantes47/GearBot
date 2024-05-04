import os
import shutil

import discord
from database import table_check
from bin.models import ServerInfo
from discord.ext import commands

from cogs.error_handler import CommandErrorHandler
from cogs.exceptions import FailAdminCheck, FailGearChannelCheck
from bin.models import GearData, Result

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='init', hidden=True)
    @commands.is_owner()
    async def init_function(self, ctx):
        table_check()
        await ctx.send('Bot initialized')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send('Hello there...\nPlease tell a manager to set me up by running ?setup')
                break

    @commands.command(name='senderror', hidden=True)
    @commands.is_owner()
    async def send_error(self, ctx, message: str = 'testing'):  
        try:
            raise Exception(message)
        except Exception as error:
            print(error.__traceback__)
            error_handler = self.bot.get_cog('CommandErrorHandler')
            await error_handler.send_pm(error)

def setup(bot):
    bot.add_cog(AdminCog(bot))


def check_admin(ctx):
    for role in ctx.author.roles:
        if 'admin' in role.name.lower():
            return True
    raise FailAdminCheck

def check_gear_channel(ctx):
    if ctx.channel.id == #TODO:Gear channel id:
        return True
    else:
        raise FailGearChannelCheck
