import discord
from discord.ext import commands
from discord.ext.commands import Context
import datetime
import requests

class general(commands.Cog, name="general"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.error_color = discord.Color.red()
        self.light_color = 0xBEBEFE
        self.bot_start_time = datetime.datetime.now()

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
    
    @commands.hybrid_command(name="serverinfo", description="Get some information about the server.")
    async def serverinfo_command(self, context: commands.Context) -> None:
        """Get some information about the server."""
        roles = [role.name for role in context.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying [50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = discord.Embed(title=f"**Server Name:** {context.guild}", color=0xBEBEFE)
        if context.guild.icon:
            embed.set_thumbnail(url=context.guild.icon.url)
        embed.add_field(name="Server ID", value=context.guild.id)
        embed.add_field(name="Member Count", value=context.guild.member_count)
        embed.add_field(name="Text/Voice Channels", value=f"{len(context.guild.channels)}")
        embed.add_field(name=f"Roles ({len(context.guild.roles)})", value=roles)
        embed.set_footer(text=f"Created at: {context.guild.created_at}")
        await context.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(general(bot))
