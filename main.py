import discord
from discord.ext import commands
import os

from helpCommands import helpCommands
from playMusic import playMusic
from funCommands import funCommands


bot = commands.Bot(command_prefix="!")

bot.remove_command("help")

bot.add_cog(helpCommands(bot))
bot.add_cog(playMusic(bot))
bot.add_cog(funCommands(bot))

bot.run(os.getenv("TOKEN"))