import discord
import os
import requests

client = discord.Client()
CHANNEL_NAME = os.environ['CHANNEL_NAME']
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
        if after.channel and after.channel.name == CHANNEL_NAME:
            print(f"{member.name} joined {after.channel.name}")
            requests.post(PUSHOVER_URL,
                          data={
                              "token": PUSHOVER_TOKEN,
                              "user": PUSHOVER_USER,
                              "message": f"{member.name} joined the channel."
                          })


if __name__ == '__main__':
    client.run(os.environ["DISCORD_BOT_TOKEN"])
