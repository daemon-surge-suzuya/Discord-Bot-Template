import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Context


class utilities(commands.Cog, name="utilities"):

  def __init__(self, bot) -> None:
    self.bot = bot
    self.error_color = discord.Color.red()
    self.light_color = 0xBEBEFE
    self.allowed_ids = [789731850645405766]
    self.bot_start_time = datetime.datetime.now()

  async def cog_check(self, ctx):
    if ctx.author.id not in self.allowed_ids:
      error_embed = discord.Embed(
          title="Permission Denied!",
          description="This command is restricted to developers only.",
          color=discord.Color.red())
      await ctx.send(embed=error_embed)
      return False
    return True

  @commands.command()
  async def status(self, ctx, online_status):
    if str(online_status).lower() == "dnd":
      await self.bot.change_presence(status=discord.Status.dnd,
                                     activity=discord.Game("Monitoring!"))
    elif str(online_status).lower() == "idle":
      await self.bot.change_presence(status=discord.Status.idle,
                                     activity=discord.Game("Monitoring!"))
    elif str(online_status).lower() == "offline":
      await self.bot.change_presence(status=discord.Status.offline,
                                     activity=discord.Game("Monitoring!"))
    else:
      await self.bot.change_presence(status=discord.Status.online,
                                     activity=discord.Game("Monitoring!"))

    embed = discord.Embed(
        color=self.light_color,
        title="→ Online Status Changed!",
        description=
        f"• My status has been updated to: `{online_status.lower()}`")

    await ctx.send(embed=embed)

  @commands.command()
  async def uptime(self, ctx):
    embed = discord.Embed(
        color=self.light_color,
        title="→ Current Uptime",
        description=f"uptime : {datetime.datetime.now() - self.bot_start_time}"
    )

    await ctx.send(embed=embed)

  @commands.command()
  async def ping(self, context: Context) -> None:
    """
        Check if the bot is alive.

        :param context: The hybrid command context.
        """
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
        color=0xBEBEFE,
    )
    await context.send(embed=embed)

  @commands.command()
  async def sync(self, context: Context, scope: str) -> None:
    if scope == "global":
      await context.bot.tree.sync()
      embed = discord.Embed(
          description="Slash commands have been globally synchronized!",
          color=0xBEBEFE,
      )
      await context.send(embed=embed)
      return
    elif scope == "guild":
      context.bot.tree.copy_global_to(guild=context.guild)
      await context.bot.tree.sync(guild=context.guild)
      embed = discord.Embed(
          description="Slash commands have been synchronized in this guild.",
          color=0xBEBEFE,
      )
      await context.send(embed=embed)
      return
    embed = discord.Embed(description="The scope must be `global` or `guild`.",
                          color=0xE02B2B)
    await context.send(embed=embed)

  @commands.command()
  async def unsync(self, ctx, scope: str) -> None:
    if scope == "global":
      ctx.bot.tree.clear_commands(guild=None)
      await ctx.bot.tree.sync()
      embed = discord.Embed(
          description="Slash commands have been globally unsynchronized.",
          color=0xBEBEFE,
      )
      await ctx.send(embed=embed)
      return
    elif scope == "guild":
      ctx.bot.tree.clear_commands(guild=ctx.guild)
      await ctx.bot.tree.sync(guild=ctx.guild)
      embed = discord.Embed(
          description="Slash commands have been unsynchronized in this guild.",
          color=0xBEBEFE,
      )
      await ctx.send(embed=embed)
      return
    await ctx.send(embed=discord.Embed(
        description="The scope must be `global` or `guild`.", color=0xE02B2B))


async def setup(bot) -> None:
  await bot.add_cog(utilities(bot))

