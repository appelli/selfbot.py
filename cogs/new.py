import discord
from discord.ext import commands
from ext.utility import parse_equation
from ext.colours import ColorNames
from urllib.request import urlopen
from sympy import solve
from PIL import Image
import asyncio
import random
import emoji
import copy
import io
import aiohttp
import json
import os
from discord.ext.commands import TextChannelConverter
from contextlib import redirect_stdout
from ext import embedtobox
from ext.utility import load_json
from urllib.parse import quote as uriquote
from urllib.parse import urlparse
from mtranslate import translate
from lxml import etree
from ext import fuzzy
from ext import embedtobox
import unicodedata
import traceback
import textwrap
import wikipedia
import datetime
import inspect
import re
import psutil
import pip

class New:
    def __init__(self, bot):
        self.bot = bot
		
    @commands.group(pass_context=True, invoke_without_command=True)
    async def ascii(self, ctx, *, msg):
        """Convert text to ascii art. Ex: ascii stuff help ascii for more info."""
        if ctx.invoked_subcommand is None:
            if msg:
                font = get_config_value("optional_config", "ascii_font")
                msg = str(figlet_format(msg.strip(), font=font))
                if len(msg) > 2000:
                    await ctx.send(self.bot.bot_prefix + 'Message too long, RIP.')
                else:
                    await ctx.message.delete()
                    await ctx.send(self.bot.bot_prefix + '```\n{}\n```'.format(msg))
            else:
                await ctx.send(
                               self.bot.bot_prefix + 'Please input text to convert to ascii art. Ex: ``>ascii stuff``')

    @commands.command(pass_context=True)
    async def textflip(self, ctx, *, msg):
        """Flip given text."""
        result = ""
        for char in msg:
            if char in self.text_flip:
                result += self.text_flip[char]
            else:
                result += char
        await ctx.message.edit(content=result[::-1])  # slice reverses the string

    @commands.command(pass_context=True)
    async def regional(self, ctx, *, msg):
        """Replace letters with regional indicator emojis"""
        await ctx.message.delete()
        msg = list(msg)
        regional_list = [self.regionals[x.lower()] if x.isalnum() or x in ["!", "?"] else x for x in msg]
        regional_output = '\u200b'.join(regional_list)
        await ctx.send(regional_output)
		
    @commands.command()
    async def embedsay(self, ctx, *, message):
        '''Quick command to embed messages quickly.'''
        await ctx.message.delete()
        em = discord.Embed(color=random.randint(0, 0xFFFFFF))
        em.description = message
        await ctx.send(embed=em)
	
def setup(bot):
    bot.add_cog(New(bot))