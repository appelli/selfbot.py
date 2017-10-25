'''
MIT License
Copyright (c) 2017 verixx
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import discord
from discord.ext import commands
from discord.ext.commands import TextChannelConverter
from contextlib import redirect_stdout
from ext.utility import load_json
from urllib.parse import quote as uriquote
from mtranslate import translate
from lxml import etree
from ext import fuzzy
from ext import embedtobox
from PIL import Image
import unicodedata
import traceback
import textwrap
import wikipedia
import aiohttp
import inspect
import re
import io
import os
import random

class Utility:
    '''Useful commands to make your life easier'''
    def __init__(self, bot):
        self.bot = bot
        self.lang_conv = load_json('data/langs.json')
        self._last_embed = None
        self._rtfm_cache = None
        self._last_google = None
        self._last_result = None

	@commands.command()
    async def quote(self, ctx, id : int, channel : discord.TextChannel=None):
        """Quote someone's message by ID"""
        await ctx.message.delete()

        msg = await ctx.get_message(channel or ctx.channel, id)

        if not msg:
            return await ctx.send('Could not find that message!', delete_after=3.0)

        em = discord.Embed(color=0x00FFFF, description=msg.clean_content, timestamp=msg.created_at)
        em.set_author(name=str(msg.author), icon_url=msg.author.avatar_url)

        if isinstance(msg.channel, discord.TextChannel):
            em.set_footer(text='#'+str(msg.channel))
        else:
            em.set_footer(text=str(msg.channel))

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Utility(bot))
