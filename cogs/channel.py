import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands

class ChannelCog(commands.Cog, name="channel"):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def cog_check(self, ctx: Context):
        author_role = ctx.author.top_role
        bot_role = ctx.me.top_role

        if author_role.position > bot_role.position or ctx.author == ctx.guild.owner:
            return True
        else:
            error_embed = discord.Embed(
                title="Permission Error",
                description="You do not have a higher role than me to use this command!",
                color=discord.Color.red())
            await ctx.send(embed=error_embed)
            return False

    @commands.hybrid_command(name="lock", description="Locks the current channel")
    async def lock(self, ctx) -> None:
        """Locks the current channel"""

        channel = ctx.channel
        overwrites = channel.overwrites_for(ctx.guild.default_role)
        
        if overwrites.send_messages is False:
            await ctx.send(embed=discord.Embed(title="Already Locked!", description=f"Channel {channel.mention} is already locked!", color=discord.Color.red()))
        else:
            try:
                await channel.set_permissions(ctx.guild.default_role, send_messages=False)
                await ctx.send(embed=discord.Embed(title="Channel has been Locked!", description=f"Channel {channel.mention} has been locked!", color=discord.Color.red()))
            except:
                await ctx.send(embed=discord.Embed(title="Error Occurred!", description=f"An error occurred while trying to lock the channel {channel.mention}", color=discord.Color.red()))

    @commands.hybrid_command(name="unlock", description="Unlocks the current channel")
    async def unlock(self, ctx) -> None:
        """Unlocks the current channel"""

        channel = ctx.channel
        overwrites = channel.overwrites_for(ctx.guild.default_role)
        if overwrites.send_messages is True:
            await ctx.send(embed=discord.Embed(title="Already Unlocked!", description=f"Channel {channel.mention} is already unlocked!", color=0xBEBEFE))
        else:
            try:
                await channel.set_permissions(ctx.guild.default_role, send_messages=True)
                await ctx.send(embed=discord.Embed(title="Channel has been Unlocked!", description=f"Channel {channel.mention} has been unlocked!", color=0xBEBEFE))
            except:
                await ctx.send(embed=discord.Embed(title="Error Occurred!", description=f"An error occurred while trying to unlock the channel {channel.mention}", color=0xBEBEFE)) 

    @commands.hybrid_command(name="lockdown", description="Locks all the channels of the server")
    async def lockdown(self, ctx) -> None:
        """Locks all the channels of the server"""
        
        guild = ctx.guild
        try:
            for channel in guild.channels:
                if not isinstance(channel, discord.CategoryChannel):
                    await channel.set_permissions(ctx.guild.default_role, send_messages=False)
                    await channel.send(embed=discord.Embed(title="Server is on Lockdown!", description="All the channels have been locked!", color=discord.Color.red()))
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.hybrid_command(name="end_lockdown", description="Unlocks all the channels of the server")
    async def end_lockdown(self, ctx) -> None:
        """Unlocks all the channels of the server"""

        guild = ctx.guild
        try:
            for channel in guild.channels:
                if not isinstance(channel, discord.CategoryChannel):
                    await channel.set_permissions(ctx.guild.default_role, send_messages=True)
                    await channel.send(embed=discord.Embed(title="Server lockdown has been lifted!", description="All the channels have been Unlocked!", color=0xBEBEFE))
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

async def setup(bot) -> None:
    await bot.add_cog(ChannelCog(bot))
