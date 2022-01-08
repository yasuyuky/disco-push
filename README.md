# disco-push

[Pushover][pushover] notification when someone enters a [Discord][discord] channel

# Usage

## Setup Discord Bot

### Required Bot Permissions

- [x] Manage Channels

## Prepare a config file

```toml
discord_bot_token = "YOUR_DISCORD_BOT_TOKEN"

[[channel]]
channel_id = YOUR_CHANNEL_ID
pushover_user = "YOUR_PUSHOVER_USER"
pushover_token = "YOUR_PUSHOVER_TOKEN"
```

## Execute

```console
python disco-push.py
```

[pushover]: https://pushover.net
[discord]: https://discord.gg
