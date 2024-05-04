import asyncio
import os
import typing
import discord
from datetime import date
from math import ceil
from discord.ext import commands
from bin.get import (GearData, get_gear, get_average, remove_gear, get_all)
from database import (update_gear, update_ap, update_aap, update_dp, table_check)  # Assuming table_check function creates the necessary table
from cogs.admin import check_admin

class GearCog(commands.Cog, name='gear'):
    def __init__(self, bot):
        self.bot = bot
        self.pending_gear_data = {}

    @commands.command(name='gear')
    async def gear(self, ctx, *args):
        """View or update your gear."""
        if args:
            try:
                ap, aap, dp = map(int, args[:3])
                # Calculate gear score
                gs = ((ap + aap) / 2) + dp
                gear_data = GearData(ctx.author.id, '', ap, aap, dp, gs, ctx.author.display_name, ctx.guild.id, date.today()) 
                result = update_gear(gear_data)
                if result:
                    await ctx.send("Gear updated successfully!")
                else:
                    await ctx.send("Failed to update gear.")
            except ValueError:
                await ctx.send("Invalid input format. Please provide AP AAP DP.")
        else:
            # Check if the user already has gear data in the database
            existing_gear_data = get_gear(ctx.author.id)
            if existing_gear_data.status:
                # User already has gear data, send it to them
                gear_data = existing_gear_data.gear_data
                if gear_data:
                    formatted_response = (
                        f"{ctx.author.display_name}:\n"
                        f"AP: {gear_data[2]}\n"
                        f"AAP: {gear_data[3]}\n"
                        f"DP: {gear_data[4]}"
                    )
                    await ctx.send(formatted_response)
                else:
                    await ctx.send("No gear data found.")
            else:
                await ctx.send("No gear data found or incomplete data.")

    @commands.command(name='ap')
    async def ap(self, ctx, value: int):
        """Set your AP."""
        result = update_ap(ctx.author.id, value)
        if result:
            await ctx.send(f'AP updated to {value}.')
        else:
            await ctx.send("Failed to update AP.")

    @commands.command(name='aap')
    async def aap(self, ctx, value: int):
        """Set your Awakening AP."""
        result = update_aap(ctx.author.id, value)
        if result:
            await ctx.send(f'Awakening AP updated to {value}.')
        else:
            await ctx.send("Failed to update Awakening AP.")

    @commands.command(name='dp')
    async def dp(self, ctx, value: int):
        """Set your DP."""
        result = update_dp(ctx.author.id, value)
        if result:
            await ctx.send(f'DP updated to {value}.')
        else:
            await ctx.send("Failed to update DP.")

    @commands.command(name='remove')
    async def remove_member_gear(self, ctx, user_id: int):
        """Remove gear of a member who left using their discord id."""
        # Check if the user is an admin
        if not check_admin(ctx):
            return await ctx.send("You are not an admin!")
        
        # Remove the gear of the specified member directly
        result = remove_gear(user_id)
        
        # Send the result of gear removal
        await ctx.send(result)


    @commands.command(name='gearaverage')
    async def guild_average(self, ctx):
        """Get the average GS of the guild."""
        result = get_average(ctx.guild.id)
        print(result)
        if result.status:
            average_gs = result.message  # Extract the numerical value
            response = f'Guild GS Average is: {average_gs:.1f}'  # Format the numerical value
        else:
            response = result
        await ctx.send(response)

    @commands.command(name='allgear')
    async def display_all_gear(self, ctx, page: int = 1):
        """Display all members' gear."""
        result = get_all(ctx.guild.id, page)

        if not result.status:
            return await ctx.send(result.message)

        gear_data = result.obj
        pages = result.code

        # Prepare the header row for the table
        header_row = "| Family Name | AP | AAP | DP | Gear Score |\n"
        header_row += "|:-----------:|:--:|:---:|:--:|:----------:|\n"

        # Prepare the data rows for the table
        data_rows = ""
        for gear in gear_data:
            data_rows += f"| {gear.family_name} | {gear.ap} | {gear.aap} | {gear.dp} | {gear.gs} |\n"

        # Combine the header row and data rows
        table = f"**Gear Data (Page {page}/{pages}):**\n\n"
        table += f"{header_row}{data_rows}"

        await ctx.send(f"```markdown\n{table}```")



async def setup(bot):
    await bot.add_cog(GearCog(bot))
