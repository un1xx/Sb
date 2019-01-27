import os

import aiohttp
import discord
import heroku3
from discord.ext.commands import Bot

class Void(Bot):
    '''
    Custom bot class
    '''
    def __init__(self, **kwargs):
        kwargs['command_prefix'] = ['!!!']
        super().__init__(**kwargs)
        self.exts = [i[:-3] for i in os.listdir("exts") if i.endswith('.py')]
        self.heroku = heroku3.from_key(os.getenv('HEROKUAPIKEY'))
        self.session = aiohttp.ClientSession(loop=self.loop)

    def close_session(self):
        '''
        closes aiohttp session.
        '''
        self.session.close()
