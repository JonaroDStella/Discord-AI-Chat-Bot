class data_class:
    pass

class User:
    def __init__(self, data: dict) -> None:
        self.data = data_class()
        self.data.__dict__ = data.copy()

    def set_data(self, name, value) -> str:
        try:
            cls = self.data.__dict__[name].__class__
            self.data.__dict__[name] = cls(value)
            return f'{name} now is {self.data.__dict__[name]}'
        except ValueError:
            return f'No valid input. Data should be class: {cls.__name__}'
        except KeyError:
            return f'No data named {name}'
        except:
            return f'Unknown error pls contact with Admin'


class UserDB:
    def __init__(self) -> None:
        self.users: dict[int, User] = {}
        self.data = data_class()

    def set_data(self, name, value) -> str:
        try:
            cls = self.data.__dict__[name].__class__
            self.data.__dict__[name] = cls(value)
            return f'{name} now is {self.data.__dict__[name]}'
        except ValueError:
            return f'No valid input. Data should be class: {cls.__name__}'
        except KeyError:
            return f'No data named {name}'
        except:
            return f'Unknown error pls contact with Admin'

    def get_user(self, id: int) -> User:
        if id not in self.users.keys():
            self.users[id] = User(self.data.__dict__)
        return self.users[id]

    def sync_data(self, user: User) -> None:
        for key in user.data.__dict__.keys():
            if key not in self.data.__dict__.keys():
                user.data.__dict__.pop(key)
        for key in self.data.__dict__.keys():
            if key not in user.data.__dict__.keys():
                user.data.__dict__[key] = self.data.__dict__[key]

    def sync_all_data(self) -> None:
        for user in self.users.values():
            self.sync_data(user)