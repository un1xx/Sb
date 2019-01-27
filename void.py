import os

import discord
from discord.ext import commands
from pagination import EmbedPagination
import inspect
import helpformatter
from h4cp482s import Int4ctHelpSn as IH 

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
        
        await self.bot.change_presence(activity=discord.Game(name="Void | v!help"))

    async def on_message_edit(self, before, after):
        await self.bot.process_commands(after)
    
    async def on_message(self, msg):
        if  msg.content.lower() in ['help', 'halp', 'report'] and msg.guild ==  self.bot.get_guild(528908686123597835) and not msg.author.bot:
            await msg.channel.send('need help? DM me. <a:BlobbleWobble:529078992943185922>')
        if isinstance(msg.channel, discord.DMChannel) and not msg.author.bot:
            guild = self.bot.get_guild(528908686123597835)
            cat = guild.get_channel(529690110258708480)
            channel_exists = [i for i in guild.channels if i.name == f"{msg.author.name.lower().replace(' ', '-')}{msg.author.discriminator}"]
            if channel_exists:
                chn = channel_exists[0]
                await chn.send(f'**{msg.author.name}** : {msg.clean_content}')
                if msg.attachments:
                    await chn.send(f"attachments with the message: {','.join(i.url for i in msg.attachments)}")
                await msg.add_reaction('\u2611')
            else:
                Ihelp = IH(self.bot)
                await msg.add_reaction('\u2611')
                await Ihelp.start(msg, cat)
        if msg.content.lower() == '=seclose':
            g = self.bot.get_guild(528908686123597835)
            c = g.get_channel(529690110258708480)
            if msg.channel.category == c:
                try:
                    await msg.channel.delete()
                except:
                    pass 
   
@bot.check
def nodmsplz(ctx):
    return not isinstance(ctx.message.channel, discord.DMChannel)

@bot.check
def nobotsplz(ctx):
    return not ctx.message.author.bot

@bot.command(name='help', aliases=['h'])
async def _function(ctx, *args):
    '\n    Get Help on a command.\n    '
    if (not ctx.author.permissions_in(ctx.channel).embed_links) or isinstance(ctx.channel, discord.DMChannel):
        return await commands.bot._default_help_command(ctx, *args)
    if (not len(args)):
        helpclass = helpformatter.HelpFormatter(list(bot.commands), bot, ctx)
        embeds = await helpclass.embedinate()
        paginator = EmbedPagination(embeds, bot, Footer=True, color=ctx.message.author.top_role.color)
        await paginator.paginate(ctx)
    elif len(args) is 1:
        cmd = bot.get_command(args[0])
        if (not cmd):
            cog = bot.get_cog(args[0])
            if (not cog):
                return await ctx.send(f'''command {args[0]} not found.''')
            cog_cmds = []
            for i in inspect.getmembers(cog):
                if isinstance(i[1], commands.core.Command) or isinstance(i[1], commands.core.Group):
                    cog_cmds.append(i[1])
            e = discord.Embed(title=args[0], color=65520, description=f'''commands of command category {args[0]} (total {len(cog_cmds)} commands.)''')
            e.set_footer(text=f'''Do "{ctx.message.content.split('help')[0]}help <command>" for more info on a command.''' if (not ctx.message.mentions) else f'''Do "{ctx.message.content.split()[0]} help <command>" for more info on a command.''')
            if len(cog_cmds) <= 5:
                for i in cog_cmds:
                    e.add_field(name=helpformatter.format_vars(i), value=i.short_doc, inline=False)
                await ctx.send(embed=e)
            elif len(cog_cmds) > 5:
                embeds = []
                for i in cog_cmds[:5]:
                    e.add_field(name=helpformatter.format_vars(i), value=i.short_doc, inline=False)
                embeds.append(e)
                for i in range(5, len(cog_cmds), 5):
                    e = discord.Embed(title=f'''{args[0]} (Continued...)''', description=f'''commands of command category {args[0]} (total {len(cog_cmds)} commands.)''')
                    e.set_footer(text=f'''Do "{ctx.message.content.split('help')[0]}help <command>" for more info on a command.''' if (not ctx.message.mentions) else f'''Do "{ctx.message.content.split()[0]} help <command>" for more info on a command.''')
                    for v in cog_cmds[i:i + 5]:
                        e.add_field(name=helpformatter.format_vars(v), value=v.short_doc, inline=False)
                    embeds.append(e)
                paginator = EmbedPagination(sorted(embeds, key=(lambda e: e.title)), bot, Footer=True, color=1048560)
                await paginator.paginate(ctx)
        is_group = False
        try:
            cmd.commands
            is_group = True
        except:
            pass
        if (not is_group):
            e = discord.Embed(description=f'''{cmd.help}''', color=1048560)
            e.title = helpformatter.format_vars(cmd)
            e.set_footer(text=f'''Do "{ctx.message.content.split('help')[0][:2]}help <command>" for more info on a command.''' if (not ctx.message.mentions) else f'''Do "{ctx.message.content.split()[0]} help <command>" for more info on a command.''')
            return await ctx.send(embed=e)
        if is_group:
            e = discord.Embed(description=cmd.help, color=1048560)
            e.title = helpformatter.format_vars(cmd)
            for v in set(cmd.commands.values()):
                e.add_field(name=helpformatter.format_vars(v), value=v.short_doc, inline=False)
            e.set_footer(text=f'''Do "{ctx.message.content.split('help')[0][:2]}help <command>" for more info on a command.''' if (not ctx.message.mentions) else 'Do f"{ctx.message.content.split()[0]} help <command>" for more info on a command.')
            return await ctx.send(embed=e)
    elif len(args) is 2:
        cmd = bot.get_command(args[0])
        if (not cmd):
            return await ctx.send(f'''command {args[0]} not found''')
        sub_cmd = cmd.get_command(args[1])
        if (not sub_cmd):
            return await ctx.send(f'''command {args[0]} has no subcommand {args[1]}''')
        e = discord.Embed(description=f'''{sub_cmd.help}''', color=1048560)
        e.title = helpformatter.format_vars(sub_cmd)
        e.set_footer(text=f'''Do "{ctx.message.content.split()[0][:2]} <command>" for more info on a command.''' if (not ctx.message.mentions) else f'''Do "{ctx.message.content.split()[0]} help <command>" for more info on a command.''')
        await ctx.send(embed=e)


bot.add_cog(Main(bot))
bot.run(os.getenv('TOKEN'), bot=False)
# test comment

