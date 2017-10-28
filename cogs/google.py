import discord
from discord.ext import commands
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
from PIL import Image
import unicodedata
import traceback
import textwrap
import wikipedia
import aiohttp
import datetime
import inspect
import random
import re
import io
import os
import asyncio
import psutil
import random
import pip

class Google:

    def __init__(self, bot):
        self.bot = bot
        self.lang_conv = load_json('data/langs.json')
        self._last_embed = None
        self._rtfm_cache = None
        self._last_google = None
        self._last_result = None	


def setup(bot):
    bot.add_cog(Google(bot))