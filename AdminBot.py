"""
rm -rf /* Discord Admin Bot by Scott 'LittlemanSMG' Goes
5/2/2018

Using Discord.py
  Rewrite info for discord.ext.Commands
    http://discordpy.readthedocs.io/en/rewrite/index.html
  Standard documentation
    http://discordpy.readthedocs.io/en/latest/api.html

Github:
  https://github.com/Littlemansmg/RM-RF-DiscordAdminBot
"""

# ---------------------------Imports------------------------------------
from discord.ext import commands
from datetime import datetime as dt
import discord
import logging
import asyncio
import sqlite3
import os
from help import helps

# ----------------------------LOGS--------------------------------------

def commandInfo(ctx):
    pass

def commandWarning(ctx):
    pass

# ----------------------------BOT---------------------------------------

bot = commands.Bot(command_prefix = '/*')

# Todo: Learn how to format help
# Remove help command for formatting.
# bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(game = discord.Game(name = "Type /*help for help"))
    users = bot.get_all_members()
    for user in users:
        sqlconvert = (user.name,)
        c.execute("INSERT INTO rmusers(userid, last_time_message)VALUES (?,?);",
                  (str(sqlconvert), dt.utcnow().timestamp()))

@bot.event
async def on_command_error(error, ctx):
    bot.say('fuck')

# @bot.event
# async def on_message(message):
#     if message.content.startswith(bot.user.mention + ' noob'):
#             await bot.send_message(message.channel, '/*noob')


# format help first.
# @bot.command(pass_context = True, name = 'help', description = 'Prints help text.', help = helps.commandHelp)
# async def help(self, ctx, ):

@bot.command(pass_context = True, name = 'noob', description = helps.newDesc, help = helps.newHelp,
             alias = helps.newAlias)
async def new(ctx):
    await bot.say('This command works.')

@bot.command(pass_context = True, name = 'mention')
async def mention(ctx, notice : discord.User):
    await bot.say(notice.mention)

if __name__ == '__main__':
    # get Token
    with open('token.txt') as token:
        token = token.readline()

    # Start Logging
    logging.basicConfig(handlers = [logging.FileHandler('discord.log', 'a', 'utf-8')],
                        level = logging.INFO)

    #connect to DB
    rmdb = sqlite3.connect('rm.db')
    c = rmdb.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS rmusers (userid TEXT PRIMARY KEY, last_time_message TEXT)''')

    try:
        # Run bot
        loop = asyncio.get_event_loop()
        loop.run_until_complete(bot.run(token.strip()))
    except RuntimeError as e:
        # If RuntimeError happens, stdout message/log.
        rmdb.commit()
        rmdb.close()
        print('This is probably a Runtime error from turning me off.')
        now = dt.now().strftime('%m/%d %H:%M ')
        logging.error(now + str(e))
