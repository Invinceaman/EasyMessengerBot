# EasyMessengerBot

## Requirements

```pip install -r requirements.txt```

## Running

```python bot_client.py```

## Auth

Example auth file format is in `auth_details.example.py`. Rename this to `auth_details.py`

## Config

An example config file is in `config.example.json`. When running the bot, change this to `config.json`. The config file contains information about what groups the bot is active in and information about each command the bot has access to. 

## Making new commands

### Creating the file

To make a new command, create a python file: `modules/command_name/command_name.py` (examples shown for `commands` and `uptime`). The `command_name.py` file must implement `def module(message_object, **kwargs)`.

### Adding it to the config file

Create a new entry in `commands` following the format of `uptime`. The key is the keyword that activates the command, `help` displays info text about the command when `!command !help` is called, and `file_path` is the name of the directory that was created earlier.