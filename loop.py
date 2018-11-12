import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import os

client = discord.Client()


channelweb = '502510555618344960'   #Channel du webhook
channel = '502399480176443394'      #Channel timer

@client.event
async def on_ready():
    while True:
        client.send_message(await client.send_message(client.get_channel(channelweb),"!nbj"))
        time.sleep(45)
        client.send_message(await client.send_message(client.get_channel(channelweb),"!nbj"))
        time.sleep(45)
        client.send_message(await client.send_message(client.get_channel(channelweb),"!nbj"))
        time.sleep(45)
        client.send_message(await client.send_message(client.get_channel(channelweb),"!nbj"))
        time.sleep(45)
        client.send_message(await client.send_message(client.get_channel(channel),"!mp"))
        time.sleep(45)
    return

client.run(os.getenv('TOKEN2'))
