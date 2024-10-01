import twitchio
from twitchio.ext import commands
import discord
from discord.ext import commands as discord_commands
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

discord_bot_token = 'discord_bot_token'
twitch_bot_token = 'twitch_bot_token'
twitch_client_id = 'twitch_client_id'

twitch_nick = 'twitch_nick'
initial_twitch_channels = ['initial_twitch_channels']

discord_channel_id = 1234567890

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
discord_bot = discord_commands.Bot(command_prefix='!', intents=intents)


class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(token=twitch_bot_token, client_id=twitch_client_id, nick=twitch_nick, initial_channels=initial_twitch_channels, prefix='!')

    async def event_ready(self):
        logging.info(f'Bot Twitch connecté en tant que {self.nick}')
        for channel in self.connected_channels:
            logging.info(f'Connecté au canal: {channel.name}')

    async def event_message(self, message):
        if message.author.name.lower() == self.nick.lower():
            return

        print(f"{message.author.name}: {message.content}")

        if discord_channel:
            await discord_channel.send(f"{message.author.name}: {message.content}")


@discord_bot.event
async def on_ready():
    global discord_channel
    logging.info(f'Bot Discord connecté en tant que {discord_bot.user.name}')
    
    discord_channel = discord_bot.get_channel(discord_channel_id)
    if discord_channel:
        logging.info(f'Canal Discord récupéré avec succès: {discord_channel.name}')
    else:
        logging.error(f'Échec de la récupération du canal Discord avec l\'ID {discord_channel_id}')

async def main():
    twitch_bot = TwitchBot()
    await asyncio.gather(
        discord_bot.start(discord_bot_token),
        twitch_bot.start()
    )


if __name__ == '__main__':
    asyncio.run(main()) 