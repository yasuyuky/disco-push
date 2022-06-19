import argparse
import asyncio
from asyncio.tasks import wait_for
import discord
import requests
import toml

loop = asyncio.get_event_loop()
client = discord.Client(loop=loop)
CHANNELS = {}
PUSHOVER_URL = "https://api.pushover.net/1/messages.json"


@client.event
async def on_ready():
    for channel in client.get_all_channels():
        print(f"{channel.name} - {channel.id}")
    for cid, c in CHANNELS.items():
        c["channel"] = client.get_channel(cid)
        c["original_name"] = c["channel"].name
        ch_prefix = c.get("ch_prefix", "(Pushing)")
    await wait_for(c["channel"].edit(name=c["channel"].name + ch_prefix), 5.0)
    print("READY")


@client.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel:
        if after.channel and after.channel.id in CHANNELS:
            channel = CHANNELS[after.channel.id]
            if member.name in channel["ignore_names"]: return
            print(f"{member.name} joined {after.channel.name}")
            requests.post(PUSHOVER_URL,
                          data={
                              "token": channel["pushover_token"],
                              "user": channel["pushover_user"],
                              "message": f"{member.name} joined the channel."
                          })


async def restore_channel():
    for c in CHANNELS.values():
        if c["channel"] and c["original_name"]:
            await wait_for(c["channel"].edit(name=c["original_name"]), 5.0)
            print("CHANNEL NAME RESTORED")


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Config file (toml)")
    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    config = toml.load(args.config)
    CHANNELS = {c["channel_id"]: c for c in config["channel"]}
    try:
        loop.run_until_complete(client.start(config["discord_bot_token"]))
    except KeyboardInterrupt:
        loop.run_until_complete(restore_channel())
        loop.run_until_complete(client.close())
    finally:
        loop.close()
