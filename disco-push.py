import asyncio
import discord
import os
import requests

loop = asyncio.get_event_loop()
client = discord.Client(loop=loop)
CHANNEL_ID = int(os.environ['CHANNEL_ID'])
PUSHOVER_URL = "https://api.pushover.net/1/messages.json"
PUSHOVER_USER = os.environ['PUSHOVER_USER']
PUSHOVER_TOKEN = os.environ['PUSHOVER_TOKEN']


@client.event
async def on_ready():
    for channel in client.get_all_channels():
        print(f"{channel.name} - {channel.id}")


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


if __name__ == '__main__':
    try:
        loop.run_until_complete(client.start(os.environ["DISCORD_BOT_TOKEN"]))
    except KeyboardInterrupt:
        loop.run_until_complete(client.close())
    finally:
        loop.close()
