import os

import discord
from discord.ext import commands
import inspect

from botclass import Void

bot = Void(case_insensitive=True, self_bot=True)

bot.remove_command('help')

class Main():
    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        print('Logged in as')
        print(self.bot.user.name)
        for i in bot.exts:
            self.bot.load_extension(f'exts.{i}')
        
        await self.bot.change_presence(status=discord.status.offline)

    async def on_message_edit(self, before, after):
        await self.bot.process_commands(after)
 
   
@bot.check
def nodmsplz(ctx):
    return not isinstance(ctx.message.channel, discord.DMChannel)

@bot.check
def nobotsplz(ctx):
    return not ctx.message.author.bot and ctx.message.author.id == 407135783678640128


bot.add_cog(Main(bot))
bot.run(os.getenv('TOKEN'), bot=False)
# test comment

