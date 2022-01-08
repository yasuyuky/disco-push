import asyncio
from asyncio.tasks import wait_for
import discord
import os
import requests

loop = asyncio.get_event_loop()
client = discord.Client(loop=loop)
CHANNEL_ID = int(os.environ['CHANNEL_ID'])
PUSHOVER_URL = "https://api.pushover.net/1/messages.json"
PUSHOVER_USER = os.environ['PUSHOVER_USER']
PUSHOVER_TOKEN = os.environ['PUSHOVER_TOKEN']
CH_PREFIX = os.environ.get("CH_PREFIX", "(Pushing)")
target_channel = None
original_name = None


@client.event
async def on_ready():
    global target_channel, original_name
    for channel in client.get_all_channels():
        print(f"{channel.name} - {channel.id}")
    target_channel = client.get_channel(CHANNEL_ID)
    original_name = str(target_channel.name)
    await wait_for(target_channel.edit(name=original_name + CH_PREFIX), 5.0)
    print("READY")


@client.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel:
        if after.channel and after.channel.id == CHANNEL_ID:
            print(f"{member.name} joined {after.channel.name}")
            requests.post(PUSHOVER_URL,
                          data={
                              "token": PUSHOVER_TOKEN,
                              "user": PUSHOVER_USER,
                              "message": f"{member.name} joined the channel."
                          })


async def restore_channel():
    if target_channel and original_name:
        await wait_for(target_channel.edit(name=original_name), 5.0)
        print("CHANNEL NAME RESTORED")


if __name__ == '__main__':
    try:
        loop.run_until_complete(client.start(os.environ["DISCORD_BOT_TOKEN"]))
    except KeyboardInterrupt:
        loop.run_until_complete(restore_channel())
        loop.run_until_complete(client.close())
    finally:
        loop.close()
