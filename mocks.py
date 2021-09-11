from telebot.types import Message


class User:
    def __init__(self,
                 tg_id=None,
                 first_name=None,
                 username=None,
                 last_name=None,
                 language_code=None,
                 supports_inline_queries=None,
                 registration_date=None,
                 api_key=None,
                 message=None,
                 tuple_=None):
        self.attrs = ["tg_id", "first_name", "username", "last_name", "language_code", "supports_inline_queries",
                      "registration_date", "api_key"]
        if message is not None:
            self.create_user_from_message(message=message)
        elif tuple_ is not None:
            self.create_user_from_tuple(tuple_=tuple_)
        else:
            self.tg_id = tg_id
            self.first_name = first_name
            self.username = username
            self.last_name = last_name
            self.language_code = language_code
            self.supports_inline_queries = supports_inline_queries
            self.registration_date = registration_date
            self.api_key = api_key

    def __iter__(self):
        for attr in self.attrs:
            yield self.__getattribute__(attr)

    def __repr__(self):
        return f"{self.tg_id} | {self.first_name} | {self.username} | {self.last_name} | {self.language_code} | " \
               f"{self.supports_inline_queries} | {self.registration_date} | {self.api_key}"

    def create_user_from_message(self, message: Message):
        self.tg_id = message.chat.id
        self.first_name = message.from_user.first_name
        self.username = message.chat.username
        self.last_name = message.chat.last_name
        self.language_code = message.from_user.language_code
        self.supports_inline_queries = message.from_user.supports_inline_queries
        self.registration_date = message.date
        self.api_key = None

    def create_user_from_tuple(self, tuple_: tuple):
        for index in range(len(self.attrs)):
            self.__setattr__(self.attrs[index], tuple_[index])

