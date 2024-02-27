# MOE in-game chat to Discord webhook

This script reads data from user-defined chat channels for Myth of Empires in-game chat and outputs their content to discord.



## Recommendations

The intent is to read global chat channels only, but could be used to route other channel data as well.

It is intentionally simple and does not read or write redis, thus should be fairly safe. The chat service is extremely sensitive and reading or writing redis without using the native API would be a bad idea.

The first iteration does not support multiple webhooks tied to different channels, but you can simply run more than one instance of the script to accomplish that.

Restart this script after you've restarted the chat log service, that's when it will rotate to a new file (from what we can tell so far).

## Features

- Sends MOE in-Game Chat to a discord webhook.
- Configurable to support multiple channels.

## Configuration

The script is configured via environment variables that can be set in a `.env` file located in the same directory as the script.

You can find the channel IDs in your chat logs C:\PATH\TO\MOESERVER\MatrixServerTool\chat_logs\, which look like this:

{"addr":"1.2.3.4:28328","conn id":16,"content":"GuildName^^\u0026\u0026Im a little chat log short and stout","content type":1,"conv type":2,"from":"610133034AD89937F996C9BA3AA4859A","from nick":"timex","level":"info","msg":"chat msg","role":"chater","time":"2024-02-23T09:33:16-05:00","to":"f3a3ffec643000"}

{"addr":"1.2.3.4:35237","conn id":23,"content":"Dogs of War^^\u0026\u0026here is my handle here is my spout","content type":1,"conv type":2,"from":"0C0D025C4A38BEAB5CEAE1AA309835D2","from nick":"timex-DOGS","level":"info","msg":"chat msg","role":"chater","time":"2024-02-25T11:09:34-05:00","to":"f3a3fe34324000"}

Add the value of to: here to the .env file under GLOBAL_CHANNELS

You can configure the CHANNEL_FRIENDLY_NAMES in the .env file to display the to: channel as something more readable.

Configure DISCORD_WEBHOOK to your webhook URL.

Configure the chat log path in .env.

Example:
DISCORD_WEBHOOK="https://discord.com/api/webhooks/somewebhook"
GLOBAL_CHANNELS=f3a3ffec543000,f3a3fe34432000
CHANNEL_FRIENDLY_NAMES=f3a3ffec543000=Eastern,f3a3fe34432000=Central
LOG_DIRECTORY=C:\moenew\MatrixServerTool\chat_logs\

### Environment Variables


- `DISCORD_WEBHOOK`: The directory where game states are stored.
- `GLOBAL_CHANNELS`: The directory where backup zip files are placed.
- `CHANNEL_FRIENDLY_NAMES`: The maximum number of game states to include in a backup. The maximum number of Game States folders to add to the archive in a single execution.
- `LOG_DIRECTORY`: Whether to delete older backups after creating a new one (`True` or `False`).

## Windows installation

For this part, I'll do the steps using a windows admin account. You can do things how you want to suit your environment.
Download and install python (https://www.python.org/downloads/windows/), note that there is an option in the installer to install for all users, if preferred. Make sure to select the following options:
- Install pip
- Add python to the environment
- Make python the default program to run .py files

If haven't already, upgrade pip and install setuptools:
- python -m pip install --upgrade pip
- pip install setuptools

Install the module requirements:
- pip install -r requirements.txt

## Usage

You can run the script manually with:
```python moeChatToDiscord.py```

or

`python3 /path/to/moeChatToDiscord.py`

## Getting help

Feel free to submit a PR or issue as needed.

I can be found in the Dogs of War discord.  https://discord.gg/Z3SaqXfVvD

General community support is also available in the MOE Admins United discord. https://discord.gg/7vrFzfAMvG