#!/usr/bin/python3
import time
import json
import requests
from dotenv import load_dotenv
import os
import glob

# Load .env vars
load_dotenv()

# Assign vars to .env values
log_directory = os.getenv('LOG_DIRECTORY', 'C:\\moenew\\MatrixServerTool\\chat_logs\\')
global_channels = os.getenv('GLOBAL_CHANNELS', '').split(',')
channel_names = {channel.split('=')[0]: channel.split('=')[1] for channel in os.getenv('CHANNEL_FRIENDLY_NAMES', '').split(',') if '=' in channel}
webhook_url = os.getenv('DISCORD_WEBHOOK')


# Send message to discord
def send_to_discord(channel_friendly_name, from_nick, content):
    # Escape markdown characters so we don't break things
    def escape_markdown(text):
        markdown_chars = ['\\', '*', '_', '~', '`', '>', '|']
        for char in markdown_chars:
            text = text.replace(char, '\\' + char)
        return text

    # The input box shouldn't allow too large of messages
    # We'll have truncate func just incase...
    def truncate_message(text, max_length=2000):
        return text if len(text) <= max_length else text[:max_length-3] + '...'

    from_nick = escape_markdown(from_nick)
    content = escape_markdown(content)
    content = truncate_message(content)

    message = f"{channel_friendly_name}: {from_nick}: {content}"
    data = {"content": message}
    response = requests.post(webhook_url, json=data)
    if response.status_code != 204:
        print(f"Error sending message to Discord: {response.status_code} - {response.text}")


# Finds the last written file in the chat log dir
def find_latest_file(directory):
    list_of_files = glob.glob(f'{directory}*')
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file


# Main log file watcher
def watch_log_file(directory):
    current_file = find_latest_file(directory)
    file_position = os.path.getsize(current_file)

    while True:
        try:
            # Check for new file
            new_file = find_latest_file(directory)
            if new_file != current_file:
                current_file = new_file
                file_position = 0

            with open(current_file, 'r') as file:
                file.seek(file_position)
                lines = file.readlines()
                file_position = file.tell()

            for line in lines:
                process_line(line)

        except Exception as e:
            print(f"Error encountered: {e}")
            time.sleep(5)
            continue

        time.sleep(1)


# Function to process a line from the log file
def process_line(line):
    try:
        log_entry = json.loads(line)
        to_channel = log_entry.get("to")
        if to_channel in global_channels:
            channel_friendly_name = channel_names.get(to_channel, "Unknown Channel")
            from_nick = log_entry.get("from nick", "Unknown")
            content = log_entry.get("content", "")

            # Check for guild name and sanitize content
            if "^^&&" in content:
                guild_name, message_content = content.split("^^&&", 1)
                # Append guild name in brackets to the nick
                from_nick = f"<{guild_name}>{from_nick}"
            else:
                # If no guild name, use content as is
                message_content = content

            send_to_discord(channel_friendly_name, from_nick, message_content)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")


# Start watching the log file
watch_log_file(log_directory)
