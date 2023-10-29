import json

import discord
from discord.ext import commands as cmd, tasks
from file_input import file_input
from discord import app_commands
from help import Help
from display_nft import display_nft

from dotenv import load_dotenv
import os

load_dotenv()
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
bot = cmd.Bot(intents=intents, command_prefix="!")
bot.remove_command('help')



@tasks.loop(seconds=5)
async def update_custom_status():
    minted_NFTs = None
    with open("NFTs_minted.json", "r+") as json_file:
        minted_NFTs = json.load(json_file)['minted']
    custom_status = f"Minted {minted_NFTs} NFTs so far"
    await bot.change_presence(activity=discord.Game(name=custom_status))

@bot.event
async def on_ready():
    print('bot is up')
    await bot.add_cog(file_input(bot))
    await bot.add_cog(Help(bot))
    await bot.add_cog(display_nft(bot))
    await bot.tree.sync()
    update_custom_status.start()

bot.run(os.getenv("token"))
