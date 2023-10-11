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

bot.run("TOKEN")
