import random
import discord
import urllib
import secrets
import asyncio
import aiohttp
import re

from io import BytesIO
from discord.ext import commands
from utils import lists, permissions, http, default, argparser


class Random_Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    async def randomimageapi(self, ctx, url, endpoint):
        try:
            r = await http.get(url, res_method="json", no_cache=True)
        except aiohttp.ClientConnectorError:
            return await ctx.send("The API seems to be down...")
        except aiohttp.ContentTypeError:
            return await ctx.send("The API returned an error or didn't return JSON...")

        await ctx.send(r[endpoint])

    async def api_img_creator(self, ctx, url, filename, content=None):
        async with ctx.channel.typing():
            req = await http.get(url, res_method="read")

            if req is None:
                return await ctx.send("I couldn't create the image ;-;")

            bio = BytesIO(req)
            bio.seek(0)
            await ctx.send(content=content, file=discord.File(bio, filename=filename))

    @commands.command()
    async def supreme(self, ctx, *, text: commands.clean_content(fix_channel_mentions=True)):
        """ Make a fake Supreme logo
        Arguments:
            --dark | Make the background to dark colour
            --light | Make background to light and text to dark colour
        """
        parser = argparser.Arguments()
        parser.add_argument('input', nargs="+", default=None)
        parser.add_argument('-d', '--dark', action='store_true')
        parser.add_argument('-l', '--light', action='store_true')

        args, valid_check = parser.parse_args(text)
        if not valid_check:
            return await ctx.send(args)

        inputText = urllib.parse.quote(' '.join(args.input))
        if len(inputText) > 500:
            return await ctx.send(f"**{ctx.author.name}**, the Supreme API is limited to 500 characters, sorry.")

        darkorlight = ""
        if args.dark:
            darkorlight = "dark=true"
        if args.light:
            darkorlight = "light=true"
        if args.dark and args.light:
            return await ctx.send(f"**{ctx.author.name}**, you can't define both --dark and --light, sorry..")

        await self.api_img_creator(
            ctx, f"https://api.alexflipnote.dev/supreme?text={inputText}&{darkorlight}", "supreme.png")

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def cat(self, ctx):
        """ Posts a random cat """
        await self.randomimageapi(ctx, 'https://api.alexflipnote.dev/cats', 'file')

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def dog(self, ctx):
        """ Posts a random dog """
        await self.randomimageapi(ctx, 'https://api.alexflipnote.dev/dogs', 'file')

    @commands.command(aliases=["bird"])
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def birb(self, ctx):
        """ Posts a random birb """
        await self.randomimageapi(ctx, 'https://api.alexflipnote.dev/birb', 'file')

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def duck(self, ctx):
        """ Posts a random duck """
        await self.randomimageapi(ctx, 'https://random-d.uk/api/v1/random', 'url')


def setup(bot):
    bot.add_cog(Random_Images(bot))
