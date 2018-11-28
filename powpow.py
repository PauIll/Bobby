import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get
from discord.ext import commands
import asyncio
import datetime
import time
import os

client = discord.Client()

channela = '507498647911399434'
channelp1 = '507120862831575040'
channelp2 = '514735595063607308'
channelalert1 = '514748410050641941'
channelalert2 = '513090628075388958'

@client.event
async def on_ready() :
    print("Bot is ready")
    await client.change_presence(status=discord.Status.online, game= discord.Game(name="cache à cache avec Gilbert Montagné", type=0))

@client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, id="507515568400760843")
    await client.add_roles(member, role)

@client.event
async def on_message(message):

    channeltyping = message.channel.id
    oui = message.content
    mtype = message.type

    if channeltyping == channelalert1 :
        await client.send_message(client.get_channel(channelalert2), f"<@223971564570279938> est en live ! Rejoignez nous : https://www.twitch.tv/pollynette")
    
    if channeltyping == channelp1 or channeltyping == channelp2 :
        if oui != "" :
            nick = message.author.nick
            await client.purge_from(client.get_channel(channeltyping), limit=1, check=None, before=None, after=None, around=None)
            await client.send_message(message.author,f"Attention {nick} ce salon n'accepte que les photos ! :sun_with_face:")
            return

    if "Bonne nuit" in message.content or "bonne nuit" in message.content or "Bonne Nuit" in message.content or "Bonne soirée" in message.content or "coucou" in message.content:
        if channeltyping == channela :
            x = "\U0001F4A4"
            await client.add_reaction(message, x)
            return
        return
    
    if "Bonjour" in message.content or "salut" in message.content or "bonjour" in message.content or "Salut" in message.content:
        if channeltyping == channela :
            x = "\U0001F31E"
            await client.add_reaction(message, x)
            return
        return
    
    

    
client.run(os.getenv('TOKEN2'))
