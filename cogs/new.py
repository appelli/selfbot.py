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


class New:
    def __init__(self, bot):
        self.bot = bot
        self.regionals = {'a': '\N{REGIONAL INDICATOR SYMBOL LETTER A}', 'b': '\N{REGIONAL INDICATOR SYMBOL LETTER B}',
                          'c': '\N{REGIONAL INDICATOR SYMBOL LETTER C}',
                          'd': '\N{REGIONAL INDICATOR SYMBOL LETTER D}', 'e': '\N{REGIONAL INDICATOR SYMBOL LETTER E}',
                          'f': '\N{REGIONAL INDICATOR SYMBOL LETTER F}',
                          'g': '\N{REGIONAL INDICATOR SYMBOL LETTER G}', 'h': '\N{REGIONAL INDICATOR SYMBOL LETTER H}',
                          'i': '\N{REGIONAL INDICATOR SYMBOL LETTER I}',
                          'j': '\N{REGIONAL INDICATOR SYMBOL LETTER J}', 'k': '\N{REGIONAL INDICATOR SYMBOL LETTER K}',
                          'l': '\N{REGIONAL INDICATOR SYMBOL LETTER L}',
                          'm': '\N{REGIONAL INDICATOR SYMBOL LETTER M}', 'n': '\N{REGIONAL INDICATOR SYMBOL LETTER N}',
                          'o': '\N{REGIONAL INDICATOR SYMBOL LETTER O}',
                          'p': '\N{REGIONAL INDICATOR SYMBOL LETTER P}', 'q': '\N{REGIONAL INDICATOR SYMBOL LETTER Q}',
                          'r': '\N{REGIONAL INDICATOR SYMBOL LETTER R}',
                          's': '\N{REGIONAL INDICATOR SYMBOL LETTER S}', 't': '\N{REGIONAL INDICATOR SYMBOL LETTER T}',
                          'u': '\N{REGIONAL INDICATOR SYMBOL LETTER U}',
                          'v': '\N{REGIONAL INDICATOR SYMBOL LETTER V}', 'w': '\N{REGIONAL INDICATOR SYMBOL LETTER W}',
                          'x': '\N{REGIONAL INDICATOR SYMBOL LETTER X}',
                          'y': '\N{REGIONAL INDICATOR SYMBOL LETTER Y}', 'z': '\N{REGIONAL INDICATOR SYMBOL LETTER Z}',
                          '0': '0?', '1': '1?', '2': '2?', '3': '3?',
                          '4': '4?', '5': '5?', '6': '6?', '7': '7?', '8': '8?', '9': '9?', '!': '\u2757',
                          '?': '\u2753'}
        self.emoji_reg = re.compile(r'<:.+?:([0-9]{15,21})>')
        self.ball = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes definitely', 'You may rely on it',
                     'As I see it, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes',
                     'Reply hazy try again',
                     'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again',
                     'Don\'t count on it', 'My reply is no', 'My sources say no', 'Outlook not so good',
                     'Very doubtful']

    emoji_dict = {
    # these arrays are in order of "most desirable". Put emojis that most convincingly correspond to their letter near the front of each array.
        'a': ['??', '??', '??', '??', '4?'],
        'b': ['??', '??', '8?'],
        'c': ['??', '©', '??'],
        'd': ['??', '?'],
        'e': ['??', '3?', '??', '??'],
        'f': ['??', '??'],
        'g': ['??', '??', '6?', '9?', '?'],
        'h': ['??', '?'],
        'i': ['??', '?', '??', '1?'],
        'j': ['??', '??'],
        'k': ['??', '??'],
        'l': ['??', '1?', '??', '??', '??'],
        'm': ['??', '?', '??'],
        'n': ['??', '?', '??'],
        'o': ['??', '??', '0?', '?', '??', '?', '?', '?', '??', '??', '??'],
        'p': ['??', '??'],
        'q': ['??', '?'],
        'r': ['??', '®'],
        's': ['??', '??', '5?', '?', '??', '??'],
        't': ['??', '?', '?', '??', '??', '7?'],
        'u': ['??', '?', '??'],
        'v': ['??', '?', '?'],
        'w': ['??', '?', '??'],
        'x': ['??', '?', '?', '?', '?'],
        'y': ['??', '?', '??'],
        'z': ['??', '2?'],
        '0': ['0?', '??', '0?', '?', '??', '?', '?', '?', '??', '??', '??'],
        '1': ['1?', '??'],
        '2': ['2?', '??'],
        '3': ['3?'],
        '4': ['4?'],
        '5': ['5?', '??', '??', '?'],
        '6': ['6?'],
        '7': ['7?'],
        '8': ['8?', '??', '??', '??'],
        '9': ['9?'],
        '?': ['?'],
        '!': ['?', '?', '?', '?'],

        # emojis that contain more than one letter can also help us react
        # letters that we are trying to replace go in front, emoji to use second
        #
        # if there is any overlap between characters that could be replaced,
        # e.g. ?? vs ??, both could replace "10",
        # the longest ones & most desirable ones should go at the top
        # else you'll have "100" -> "??0" instead of "100" -> "??".
        'combination': [['cool', '??'],
                        ['back', '??'],
                        ['soon', '??'],
                        ['free', '??'],
                        ['end', '??'],
                        ['top', '??'],
                        ['abc', '??'],
                        ['atm', '??'],
                        ['new', '??'],
                        ['sos', '??'],
                        ['100', '??'],
                        ['loo', '??'],
                        ['zzz', '??'],
                        ['...', '??'],
                        ['ng', '??'],
                        ['id', '??'],
                        ['vs', '??'],
                        ['wc', '??'],
                        ['ab', '??'],
                        ['cl', '??'],
                        ['ok', '??'],
                        ['up', '??'],
                        ['10', '??'],
                        ['11', '?'],
                        ['ll', '?'],
                        ['ii', '?'],
                        ['tm', '™'],
                        ['on', '??'],
                        ['oo', '??'],
                        ['!?', '?'],
                        ['!!', '?'],
                        ['21', '??'],
                        ]
    }

    # used in textflip
    text_flip = {}
    char_list = "!#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}"
    alt_char_list = "{|}z?x??n?s?bdou?l???????p?q?,?^[\]Z?XM?n-S?Q?ONW???IH???p?q?@¿<=>;:68?9?????0/?-'+*(),?%$#¡"[::-1]
    for idx, char in enumerate(char_list):
        text_flip[char] = alt_char_list[idx]
        text_flip[alt_char_list[idx]] = char

    # used in [p]react, checks if it's possible to react with the duper string or not
    def has_dupe(duper):
        collect_my_duper = list(filter(lambda x: x != '<' and x != '?',
                                       duper))  # remove < because those are used to denote a written out emoji, and there might be more than one of those requested that are not necessarily the same one.  ? appears twice in the number unicode thing, so that must be stripped too...
        return len(set(collect_my_duper)) != len(collect_my_duper)

    # used in [p]react, replaces e.g. 'ng' with '??'
    def replace_combos(react_me):
        for combo in Fun.emoji_dict['combination']:
            if combo[0] in react_me:
                react_me = react_me.replace(combo[0], combo[1], 1)
        return react_me

    # used in [p]react, replaces e.g. 'aaaa' with '????????'
    def replace_letters(react_me):
        for char in "abcdefghijklmnopqrstuvwxyz0123456789!?":
            char_count = react_me.count(char)
            if char_count > 1:  # there's a duplicate of this letter:
                if len(Fun.emoji_dict[
                           char]) >= char_count:  # if we have enough different ways to say the letter to complete the emoji chain
                    i = 0
                    while i < char_count:  # moving goal post necessitates while loop instead of for
                        if Fun.emoji_dict[char][i] not in react_me:
                            react_me = react_me.replace(char, Fun.emoji_dict[char][i], 1)
                        else:
                            char_count += 1  # skip this one because it's already been used by another replacement (e.g. circle emoji used to replace O already, then want to replace 0)
                        i += 1
            else:
                if char_count == 1:
                    react_me = react_me.replace(char, Fun.emoji_dict[char][0])
        return react_me


    @commands.command(pass_context=True, aliases=['pick'])
    async def choose(self, ctx, *, choices: str):
        """Choose randomly from the options you give. [p]choose this | that"""
        await ctx.send(
                       self.bot.bot_prefix + 'I choose: ``{}``'.format(random.choice(choices.split("|"))))
		
    @commands.group(pass_context=True, invoke_without_command=True)
    async def ascii(self, ctx, *, msg):
        """Convert text to ascii art. Ex: [p]ascii stuff [p]help ascii for more info."""
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
		
def setup(bot):
    bot.add_cog(New(bot))