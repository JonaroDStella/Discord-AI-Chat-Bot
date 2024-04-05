class User:
    def __init__(self, data: dict) -> None:
        self.data = data.copy()

    def set_data(self, name, value) -> str:
        try:
            cls = self.data[name].__class__
            self.data[name] = cls(value)
            return f'{name} now is {self.data[name]}'
        except ValueError:
            return f'No valid input. Data should be class: {cls.__name__}'
        except KeyError:
            return f'No data named {name}'
        except:
            return f'Unknown error pls contact with Admin'


class UserDB:
    def __init__(self) -> None:
        self.users: dict[int, User] = {}
        self.data = {}

    def set_data(self, name, value) -> str:
        try:
            cls = self.data[name].__class__
            self.data[name] = cls(value)
            return f'{name} now is {self.data[name]}'
        except ValueError:
            return f'No valid input. Data should be class: {cls.__name__}'
        except KeyError:
            return f'No data named {name}'
        except:
            return f'Unknown error pls contact with Admin'

    def get_user(self, id: int) -> User:
        if id not in self.users.keys():
            self.users[id] = User(self.data)
        return self.users[id]

    def sync_data(self, user: User) -> None:
        for key in user.data.keys():
            if key not in self.data.keys():
                user.data.pop(key)
        for key in self.data.keys():
            if key not in user.data.keys():
                user.data[key] = self.data[key]

    def sync_all_data(self) -> None:
        for user in self.users.values():
            self.sync_data(user)