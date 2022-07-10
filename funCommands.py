import discord
from discord.ext import commands

from datetime import datetime
import random

class funCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dailypussy", aliases=["dp", "pussy"] , help="List pussy")
    async def dp(self, ctx):
        names = [
            "Derek",
            "Jordan", 
            "Teagle", 
            "Anfony", 
            "Antony",
            "Damon",
            "Dan",
            "Daniel", 
            "Jaimin",
            "James",
            "Jason"
            "Ross",
            "Scott", 
            "Tom", 
            "Zeidan",
            "Zac"  
        ]

        d0 = datetime(2008, 8, 18)  # Pick an arbitrary date in the past
        d1 = datetime.now()
        delta = d1 - d0

        random.seed(delta.days)
        randIndex = random.randint(0,len(names) - 1)

        await ctx.send("Today's pussy is " + names[randIndex] + "! Congratulations")

    @commands.command(name="jordan", help="Jordan's catchphrase")
    async def jordan(self, ctx):
        await ctx.send("***that's cringe***")
