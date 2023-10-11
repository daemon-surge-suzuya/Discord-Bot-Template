import discord
from discord.ext import commands
from discord.ext.commands import Context

class Roles(commands.Cog, name="roles"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.error_color = discord.Color.red()
        self.light_color = 0xBEBEFE

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

    @commands.hybrid_command(name="assign", description="Assigns a role to a member")
    async def assign(self, ctx, member: discord.Member, role: discord.Role) -> None:
        if role in member.roles:
            await ctx.send(embed=discord.Embed(title="Role already Assigned!", description=f"{member.name} already has the {role.name} role", color=self.error_color))
        else:
            try:
                await member.add_roles(role)
                await ctx.send(embed=discord.Embed(title="Role Assigned!", description=f"{member.name} has been assigned {role.name} role", color=self.light_color))
            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Error occurred!", description=f"An error occurred: {e}", color=discord.Color.red()))

    @commands.hybrid_command(name="revoke", description="Revokes a member's role")
    async def revoke(self, ctx, member: discord.Member, role: discord.Role) -> None:
        if role not in member.roles:
            await ctx.send(embed=discord.Embed(title="Role Not Found!", description=f"{member.name} does not have {role.name} role", color=self.error_color))
        else:
            try:
                await member.remove_roles(role)
                await ctx.send(embed=discord.Embed(title="Role has been Revoked!", description=f"{role.name} has been revoked from {member.name}", color=self.light_color))
            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Error occurred!", description=f"An error occurred: {e}", color=discord.Color.red()))

async def setup(bot) -> None:
    await bot.add_cog(Roles(bot))
