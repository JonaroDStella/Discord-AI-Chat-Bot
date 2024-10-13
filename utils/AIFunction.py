import discord
<<<<<<< HEAD
import openai
from utils.UserDB import User
from utils.VoiceVox import Voicevox
from config import *

openai.api_key = OPENAI_API_KEY

=======
from openai import AsyncOpenAI, OpenAIError
from utils.UserDB import User
from utils.VoiceVox import Voicevox
from saucenao_api import AIOSauceNao
from config import *

client = AsyncOpenAI(api_key=OPENAI_API_KEY)
>>>>>>> 89908d9 (fixed to adapt new openai api)

async def make_completion(user: User, message) -> tuple[bool, str]:
    try:
        history: list = user.data['history']
        history.append({'role': 'user', 'content': message})
        if len(history) > user.data['limit']:
            history = history[-user.data['limit']:]

<<<<<<< HEAD
        completion = openai.ChatCompletion.create(
=======
        completion = await client.chat.completions.create(
>>>>>>> 89908d9 (fixed to adapt new openai api)
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
<<<<<<< HEAD
    completion = openai.ChatCompletion.create(
=======
    completion = await client.chat.completions.create(
>>>>>>> 89908d9 (fixed to adapt new openai api)
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
<<<<<<< HEAD
    return messages
=======
    return messages

async def generate_image(model:str, prompt: str, size: str):
    try:
        response = await client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        quality="standard",
        n=1,
        )

        return response.data[0].url
    except OpenAIError as e:
        return f'Error happened while generating image:```\n{e}\n```'
    
async def find_source(image: discord.Attachment):
    try:
        async with AIOSauceNao('d5a4eb4b6a60ea766bf5a66e053ed50640e3320d') as aio:
            results = await aio.from_url(image.proxy_url)
        output = []
        for result in results:
            if result.similarity > 90:
                for url in result.urls:
                    output.append(url)
        if output:
            return True, output
        else:
            return False, "Found no sauce uwq."
    except Exception as e:
        return False, f"Unknown error: ```\n{e}\n```"
>>>>>>> 89908d9 (fixed to adapt new openai api)
