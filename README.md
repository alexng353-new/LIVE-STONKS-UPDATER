# LIVE STONKS UPDATER
A python bot using discord.py to update and quote stonks with data from the Yahoo Finance API

### Requires the 'members' privileged intents
[Enable privileged intents here](#enable-privileged-intents)

## Guide on use and installation:
Download the latest release [here](https://github.com/alexng353-new/LIVE-STONKS-UPDATER/releases/latest) and, after unzipping the zip, edit the config file.
Rename the config file to config.ini and change `your token` to your bot's token. 
```
[config]
token=your token
```
If you don't have a developer application yet you can create one [here](https://discord.com/developers/applications).

![devportal](https://github.com/alexng353-new/LIVE-STONKS-UPDATER/blob/master/assets/devportal.png)
After creating your application, add a bot user
![addbot](https://github.com/alexng353-new/LIVE-STONKS-UPDATER/blob/master/assets/addbot.png)
Copy the token and paste it in your config folder.
![copytoken](https://github.com/alexng353-new/LIVE-STONKS-UPDATER/blob/master/assets/copytoken.png)

### Enable Privileged Intents
Turn these two toggles on and Privileged Intents will be enabled
![privilegedintents](https://github.com/alexng353-new/LIVE-STONKS-UPDATER/blob/master/assets/privilegedintents.png)

### Install libraries with pip:
Use pip to install your libraries.
`pip install "library"`
The libraries you need are
- discord
- time
- datetime
- configparser
- asyncio
- yahoo_fin