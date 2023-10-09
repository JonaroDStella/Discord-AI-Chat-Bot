from time import time
import openai

from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


class Chat:
    def __init__(self, history: list, prompt: str, limit: int, token: int) -> None:
        self.history = history
        self.prompt = prompt
        self.limit = limit
        self.token = token
        self.reply = ''
        self.starttime = time()
        self.lasttoken = 0
        self.completion = None

    def make_completion(self, msg) -> bool:
        try:
            self.history.append({'role': 'user', 'content': msg})
            self.history = self.history[-self.limit:] if len(
                self.history) > self.limit else self.history
            self.completion = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {'role': 'system', 'content': self.prompt}] + self.history
            )
            self.reply = self.completion.choices[0].message.content
            self.history.append({"role": "assistant", "content": self.reply})
            self.lasttoken = self.completion.usage.total_tokens

            self.token += self.lasttoken
            return True
        except:
            return False


class User:
    def __init__(self, prompt: str, limit: int = 3) -> None:
        self.data = {'prompt': prompt,
                     'limit': limit
                     }
        self.chat = Chat(history=[], prompt=prompt, limit=limit, token=0)

    def get_data(self, data) -> dict:
        data = str(data)
        return str(self.data[data])


class UserDatabase:
    def __init__(self, prompt: str, limit: int = 3) -> None:
        self.db = {}
        self.prompt = prompt
        self.limit = limit

    def get_user(self, id: str, prompt: str, limit: int = 3) -> User:
        if id not in self.db:
            self.db[id] = User(prompt=prompt, limit=limit)
        return self.db[id]
