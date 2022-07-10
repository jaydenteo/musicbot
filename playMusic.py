import discord
from discord.ext import commands

from youtube_dl import YoutubeDL

import asyncio

class playMusic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.isPlaying = False
        self.isPaused = False

        self.musicQueue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

    def searchYT(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    async def playSong(self, ctx):
        if len(self.musicQueue) > 0:
            self.isPlaying = True
            self.isPaused = False

            m_url = self.musicQueue[0][0]['source']
            
            #try to connect to voice channel if you are not already connected
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.musicQueue[0][1].connect()
                #in case we fail to connect
                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.musicQueue[0][1])
            
            #remove the first element as you are currently playing it
            self.musicQueue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: asyncio.run(self.playSong(ctx)))
        else:
            self.isPlaying = False
            self.isPaused = False
    
    @commands.command(name="play", aliases=["p","playing"], help="Play song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("You need to connect to a voice channel first")
        elif self.isPaused:
            self.vc.resume()
        else:
            song = self.searchYT(query)
            if type(song) == type(True):
                await ctx.send("Could not find song")
            else:
                await ctx.send("Song added to queue")
                self.musicQueue.append([song, voice_channel])
                
                if not self.isPlaying:
                    await self.playSong(ctx)

    @commands.command(name="pause", help="Pause the music")
    async def pause(self, ctx, *args):
        if self.isPlaying:
            self.isPlaying = False
            self.isPaused = True
            self.vc.pause()
        elif self.isPaused:
            self.isPlaying = True
            self.isPaused = False
            self.vc.resume()

    @commands.command(name = "resume", aliases=["r"], help="Resume the music")
    async def resume(self, ctx, *args):
        if self.isPaused:
            self.isPlaying = True
            self.isPaused = False
            self.vc.resume()

    @commands.command(name="skip", aliases=["s"], help="Skip song")
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()

    @commands.command(name="queue", aliases=["q"], help="Show queue")
    async def queue(self, ctx):
        retval = ""

        for i in range(0, len(self.musicQueue)):
            # display a max of 5 songs in the current queue
            if (i > 4): break
            retval += self.musicQueue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    @commands.command(name="clear", aliases=["c", "bin"], help="Clear queue")
    async def clear(self, ctx):
        self.musicQueue = []
        await ctx.send("Music queue cleared")

    @commands.command(name="disconnect", aliases=["dc", "d"], help="Kick the bot from VC")
    async def dc(self, ctx):
        self.isPlaying = False
        self.isPaused = False
        self.musicQueue = []
        await self.vc.disconnect()