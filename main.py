import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands

bot = commands.Bot(command_prefix="&", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Monitoring!"))
    try:
        await bot.load_extension("cogs.moderation")
        await bot.load_extension("cogs.roles")
        await bot.load_extension("cogs.channel")
        await bot.load_extension("cogs.general")
        await bot.load_extension("cogs.utilities")
        await bot.load_extension("cogs.support")
    except Exception as e:
        print(e)

@bot.command()
async def sync(context: Context, scope: str) -> None:
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
    embed = discord.Embed(
    description="The scope must be `global` or `guild`.", color=0xE02B2B
    )
    await context.send(embed=embed)

@bot.command()
async def unsync(ctx, scope: str) -> None:
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
    embed = discord.Embed(
        description="The scope must be `global` or `guild`.", color=0xE02B2B
    )
    await ctx.send(embed=embed)

bot.run("TOKEN")
