from random import randint, choice
import logging

log = logging.getLogger(__name__)

MAGIC_8BALL = [
    "It is certain.", "Without a doubt.", "Yes, definitely.", "You may rely on it.",
    "As I see it, yes.", "Most likely.", "Outlook good.", "Signs point to yes.",
    "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
    "Cannot predict now.", "Concentrate and ask again.",
    "Don't count on it.", "My reply is no.", "My sources say no.",
    "Outlook not so good.", "Very doubtful.",
]


def get_response(user_input: str) -> str | None:
    try:
        lowered: str = user_input.strip().lower()

        if not lowered:
            return None

        # Commands with ! prefix
        if lowered.startswith('!'):
            parts = lowered.split()
            cmd = parts[0]

            if cmd == '!ping':
                return 'Pong!'

            elif cmd in ('!url', '!link'):
                return 'https://andrzej.langow.ski'

            elif cmd == '!help':
                return (
                    'Available commands: !ping, !help, !url, !link, !roll [sides], !choose <opt1> <opt2> ..., !8ball <question>\n'
                    'Or just say: hello, hi, bye, how are you, good morning, good night, thank you, roll dice, coin toss / flip a coin, url / link'
                )

            elif cmd == '!roll':
                if len(parts) > 1 and parts[1].isdigit():
                    sides = int(parts[1])
                    if sides < 2:
                        return 'Dice must have at least 2 sides!'
                    if sides > 1000:
                        return 'That\'s a big dice... max 1000 sides!'
                    return f'You rolled a d{sides}: {randint(1, sides)}'
                return f'You rolled: {randint(1, 6)}'

            elif cmd == '!choose':
                options = parts[1:]
                if len(options) < 2:
                    return 'Give me at least 2 options! e.g. !choose pizza burger sushi'
                return f'I choose: **{choice(options)}**'

            elif cmd == '!8ball':
                question = ' '.join(parts[1:])
                if not question:
                    return 'Ask me a question! e.g. !8ball Will I win today?'
                return f'🎱 {choice(MAGIC_8BALL)}'

            else:
                return 'Unknown command. Type !help for a list of commands.'

        # Natural responses without prefix
        if 'good morning' in lowered:
            return 'Good morning! ☀️'
        if 'good night' in lowered:
            return 'Good night! 🌙'
        if 'hello' in lowered or 'hi' in lowered:
            return 'Hello there!'
        if 'how are you' in lowered:
            return 'Good, thanks!'
        if 'thank you' in lowered or 'thanks' in lowered:
            return 'You\'re welcome!'
        if 'bye' in lowered:
            return 'See you!'
        if 'roll dice' in lowered:
            return f'You rolled: {randint(1, 6)}'
        if 'coin toss' in lowered or 'flip a coin' in lowered:
            return choice(['Heads!', 'Tails!'])
        if 'url' in lowered or 'link' in lowered:
            return 'https://andrzej.langow.ski'

        return None

    except Exception as e:
        log.error(f'get_response error: {e}')
        return None
