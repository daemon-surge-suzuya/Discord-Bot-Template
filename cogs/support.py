import discord
from discord.ext import commands
from discord.ext.commands import Context

class support(commands.Cog, name="support"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.error_color = discord.Color.red()
        self.light_color = 0xBEBEFE

    async def cog_check(self, ctx: Context):
        is_owner = ctx.author.id == ctx.guild.owner_id  # Compare author's ID with owner's ID
        is_admin = any(role.permissions.administrator for role in ctx.author.roles)

        if is_owner or is_admin:
            return True
        else:
            error_embed = discord.Embed(
                title="Permission Error",
                description="Only Owners and Administrators can use this command!",
                color=discord.Color.red()
            )
            await ctx.send(embed=error_embed)
            return False
        
    @commands.hybrid_command(name="bug", description="Report a bug!. Note: Using this command unnecessarily may result in you being blacklisted")
    async def bug(self, ctx, bug: str = "None"):
        try: 
            author = ctx.author
            author_name = author.name
            author_id = author.id
            server = ctx.guild
            invite = await ctx.channel.create_invite(max_age = (86400^5), unique=True)
            user = self.bot.get_user(789731850645405766)
            embed = discord.Embed(title="New Feature Report!", description=bug ,color=self.light_color)            
            embed.add_field(name="Username", value=author_name)
            embed.add_field(name="User Id", value=author_id)
            embed.add_field(name="Server", value=server)
            embed.add_field(name="Server Invite", value=invite)
            await user.send(embed=embed)
            await ctx.send(embed=discord.Embed(title="Submitted!", description="Thank you for reporting a bug, We will look into it!", color=self.light_color))
        except Exception as e:
            await ctx.send(embed=discord.Embed(title="An error occurred!", description=f"An error occurred: {e}", color=self.error_color))

    @commands.hybrid_command(name="suggest_feature", description="Suggest a new feature!. Note: Using this command unnecessarily may result in you being blacklisted")
    async def suggest_feature(self, ctx, feature: str = "None"):
        try:
            author = ctx.author
            author_name = author.name
            author_id = author.id
            server = ctx.guild
            invite = await ctx.channel.create_invite(max_age = (86400^5), unique=True)
            user = self.bot.get_user(789731850645405766)
            embed = discord.Embed(title="New Feature Suggestion!", description=feature ,color=self.light_color)
            embed.add_field(name="Username", value=author_name)
            embed.add_field(name="User Id", value=author_id)
            embed.add_field(name="Server", value=server)
            embed.add_field(name="Server Invite", value=invite)
            await user.send(embed=embed)
            await ctx.send(embed=discord.Embed(title="Submitted!", description="Thank you for reporting a bug, We will look into it!", color=self.light_color))
        except Exception as e:
            await ctx.send(embed=discord.Embed(title="An error occurred!", description=f"An error occurred: {e}", color=self.error_color))

async def setup(bot) -> None:
    await bot.add_cog(support(bot))
