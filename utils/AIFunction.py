import discord
import openai
from utils.UserDB import User
from utils.VoiceVox import Voicevox
from config import *

openai.api_key = OPENAI_API_KEY


async def make_completion(user: User, message) -> tuple[bool, str]:
    try:
        history: list = user.data['history']
        history.append({'role': 'user', 'content': message})
        if len(history) > user.data['limit']:
            history = history[-user.data['limit']:]

        completion = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {'role': 'system', 'content': user.data['prompt']}] + user.data['history']
        )
        reply: str = completion.choices[0].message.content
        history.append({"role": "assistant", "content": reply})
        user.data['history'] = history
        return True, reply

    except Exception as error:
        return False, error

async def translation(message: str, lang: str):
    completion = openai.ChatCompletion.create(
            model=MODEL,
            messages=[{'role': 'system', 'content': f'translate to {lang}'}, {'role': 'user', 'content': message}]
            )
    return completion.choices[0].message.content

async def Voice(voice: discord.VoiceClient, voice_id: int, jp: str):
    VOICE = Voicevox()
    stream = VOICE.speak(jp, voice_id)
    if voice.is_playing():
        voice.stop()
    voice.play(discord.FFmpegPCMAudio(
        source=stream, executable=FFMPEG_PATH),
        after=lambda x: print('finished audio')
    )

def split_message(message: str) -> list[str]:
    messages = []
    while len(message) > 2000:
        index = message[:2000].rfind('\n')
        if index == -1:
            index = message[:2000].rfind(' ')
            if index == -1:
                index = 1999
        messages.append(message[:index])
        message = message[index+1:]
    messages.append(message)
    return messages