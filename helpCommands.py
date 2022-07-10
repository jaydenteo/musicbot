import discord
from discord.ext import commands

class helpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.help_message = """
        ```
!help           - show help menu
!p <songName>
!s              - skip song
!q              - show queue
!c              - clear queue
!pause          - pause
!resume         - resume
!dc             - disconnect bot from channel
!dailypussy     - today's special feature! ```
        """

        self.text_channel_list = []    

    @commands.command(name="help", aliases=["h"] , help="Display all available commands")
    async def help(self, ctx):
        await ctx.send(self.help_message)
