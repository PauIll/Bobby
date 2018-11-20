import discord
from discord.ext.commands import Bot
from discord.ext import commands
import random
import asyncio
import time
import os

client = discord.Client()

classlist = ["Cra", "Ecaflip", "Eliotrope", "Eniripsa", "Enutrof", "Feca", "Steamer", "Huppermage", "Iop", "Roublard", "Osamodas", "Zobal", "Ouginak", "Pandawa", "Sram", "Sacrieur", "Sadida", "Xelor"]
elementlist = ["Air", "Eau", "Feu","Terre"]

@client.event
async def on_ready():
    print("The bot is ready!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if "!dofus" in message.content:

        elementlist = ["Air", "Eau", "Feu","Terre"]
        if message.author.name == "Jamie":
            print("test")
        dclass = random.choice(classlist)
        delement = random.choice(elementlist)
        elementlist.remove(delement)
        delement1 = random.choice(elementlist)
        elementlist.remove(delement1)
        delement2 = random.choice(elementlist)
        await client.send_message(message.channel,f"```markdown\n #{dclass} {delement} \n - 100: {delement1} \n - 150: {delement2}```")


client.run(os.getenv('TOKEN2'))

