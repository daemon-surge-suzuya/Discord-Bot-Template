# from discord import app_commands
import discord
from discord.ext import commands
from discord.ext.commands import Context
import time

class moderation(commands.Cog, name="moderation"):
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

    @commands.hybrid_command(name="purge", description="Purges messages")
    async def purge(self, ctx: Context, amount=2) -> None:
        """Purges messages"""

        embed = discord.Embed(title="Purging Messages!", description=f"Purging Messages {amount}", color=self.light_color)
        await ctx.send(embed=embed)
        time.sleep(1)
        await ctx.channel.purge(limit=(amount+1))

    @commands.hybrid_command(name="hard_ban", description="Hardban a member")
    async def hard_ban(self, context: Context, member: discord.Member, reason: str = "Banned by the server authorities!") -> None:
        """Hardban a member"""

        try:
            if member.guild_permissions.administrator:
                embed = discord.Embed(
                    description="User has administrator permissions.", color=self.error_color
                )
                await context.send(embed=embed)
            else:
                embed = discord.Embed(
                    description=f"**{member}** was banned by **{context.author}**!",
                    color=self.light_color,
                )
                embed.add_field(name="Reason:", value=reason)
                await context.send(embed=embed)
                try:
                    await member.ban(reason=reason)
                    await member.send(
                        embed=discord.Embed(
                        title="You have been banned!", description=f"You were banned by **{context.author}** from **{context.guild.name}**!\nReason: {reason}", color=self.light_color))
                except:
                    # Couldn't send a message in the private messages of the user
                    pass
        except:
            embed = discord.Embed(
                title="Error!",
                description="An error occurred while trying to ban the user. Make sure my role is above the role of the user you want to ban.",
                color=self.error_color,
            )
            await context.send(embed=embed)

    @commands.hybrid_command(name="kick", description="Kicks a member")
    async def kick(
        self, context: Context, user: discord.User, *, reason: str = "Kicked by the server authorities"
    ) -> None:
        """Kicks a member"""

        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                description="User has administrator permissions.", color=self.error_color
            )
            await context.send(embed=embed)
        else:
            try:
                embed = discord.Embed(
                    description=f"**{member}** was kicked by **{context.author}**!",
                    color=self.light_color,
                )
                embed.add_field(name="Reason:", value=reason)
                await context.send(embed=embed)
                try:
                    await member.kick(reason=reason)
                    await member.send(embed=discord.Embed(title="You have been kicked!", description=f"You were kicked by **{context.author}** from **{context.guild.name}**!\nReason: {reason}", color=self.error_color))
                except:
                    # Couldn't send a message in the private messages of the user
                    pass
            except:
                embed = discord.Embed(
                    description="An error occurred while trying to kick the user. Make sure my role is above the role of the user you want to kick.", color=self.error_color)
                await context.send(embed=embed)
    
    @commands.hybrid_command(name="nick", description="Changes the nickname of a user on a server")
    async def nick(
        self, context: Context, user: discord.User, *, nickname: str = None) -> None:
        """Changes the nickname of a user on a server"""

        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        try:
            await member.edit(nick=nickname)
            embed = discord.Embed(
                description=f"**{member}'s** new nickname is **{nickname}**!",
                color=self.light_color,
            )
            await context.send(embed=embed)
        except:
            embed = discord.Embed(
                description="An error occurred while trying to change the nickname of the user. Make sure my role is above the role of the user you want to change the nickname.",
                color=self.error_color,
            )
            await context.send(embed=embed)

    @commands.hybrid_command(name="hack_ban", description="Bans a user without having him in the server")
    async def hackban(
        self, context: Context, user_id: str, *, reason: str = "Not specified") -> None:
        """Bans a user without having him in the server"""

        try:
            await self.bot.http.ban(user_id, context.guild.id, reason=reason)
            user = self.bot.get_user(int(user_id)) or await self.bot.fetch_user(
                int(user_id)
            )
            embed = discord.Embed(
                description=f"**{user}** (ID: {user_id}) was banned by **{context.author}**!",
                color=self.light_color,
            )
            embed.add_field(name="Reason:", value=reason)
            await context.send(embed=embed)
        except Exception:
            embed = discord.Embed(
                description="An error occurred while trying to ban the user. Make sure ID is an existing ID that belongs to a user.",
                color=self.error_color,
            )
            await context.send(embed=embed)

    @commands.hybrid_command(name="soft_ban", description="Softban a member")
    async def soft_ban(self, context: Context, member: discord.Member, reason: str = "Soft banned by the server authorities!") -> None:
        """Softban a member"""
        try:
            if member.guild_permissions.administrator:
                embed = discord.Embed(
                    description="User has administrator permissions.", color=self.error_color
                )
                await context.send(embed=embed)
            else:
                embed = discord.Embed(
                    description=f"**{member}** was soft banned by **{context.author}**!",
                    color=self.light_color,
                )
                embed.add_field(name="Reason:", value=reason)
                await context.send(embed=embed)
                try:
                    await member.ban(reason=reason)
                    await member.send(
                        embed=discord.Embed(
                        title="You have been soft banned!", description=f"You were soft banned by **{context.author}** from **{context.guild.name}**!\nReason: {reason}", color=self.light_color))
                except:
                    pass
        except:
            embed = discord.Embed(
                title="Error!",
                description="An error occurred while trying to ban the user. Make sure my role is above the role of the user you want to ban.",
                color=self.error_color,
            )
            await context.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(moderation(bot))
