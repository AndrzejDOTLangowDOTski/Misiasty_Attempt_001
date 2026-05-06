from typing import Final
import os
import logging
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger(__name__)

# Szuka .env w tym samym katalogu co main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    raise ValueError("DISCORD_TOKEN nie znaleziony w pliku .env!")

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)


async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        return

    is_private: bool = user_message.startswith('?')
    if is_private:
        user_message = user_message[1:]

    try:
        response = get_response(user_message)
        if response is None:
            return  # Bot milczy gdy nie rozpoznaje komendy
        full_response: str = f'@{message.author.name} {response}'
        if is_private:
            await message.author.send(full_response)
        else:
            await message.channel.send(full_response)
    except Exception as e:
        log.error(f'Blad wysylania wiadomosci: {e}')


@client.event
async def on_ready() -> None:
    log.info(f'{client.user} is now running!')


@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    log.info(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)


def main() -> None:
    client.run(token=TOKEN, reconnect=True)


if __name__ == '__main__':
    main()
