import os
import discord
import traceback
from dotenv import load_dotenv
from discord.ext import commands
from cogs.exceptions import FailGearChannelCheck, FailAdminCheck

# Load environment variables
load_dotenv()
owner_id = int(os.getenv('OWNER_ID'))

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_pm(self, error):
        async with self.bot.fetch_user(owner_id) as user:
            error_traceback = traceback.format_exception(type(error), error, error.__traceback__)
            await user.send('```{}```'.format(error_traceback))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Prevent handling errors for commands with local handlers
        if hasattr(ctx.command, 'on_error'):
            await self.send_pm(error)
            return

        # Prevent handling errors for cogs with overridden cog_command_error
        cog = ctx.cog
        if cog and cog._get_overridden_method(cog.cog_command_error) is not None:
            return

        # Ignore specific error types
        ignored = (commands.CommandNotFound,)
        if isinstance(error, ignored):
            return

        # Handle specific error types with custom messages
        if isinstance(error, FailGearChannelCheck):
            await ctx.send(f'{ctx.command} can only be used in the gear channel.')
        elif isinstance(error, FailAdminCheck):
            await ctx.send(f'{ctx.command} can only be used by Admin.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')
        else:
            # Handle other errors with a generic error message
            print(f'Ignoring exception in command {ctx.command}:')
            traceback.print_exception(type(error), error, error.__traceback__)
            await self.send_pm(error)
            await ctx.send("HUH")

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
