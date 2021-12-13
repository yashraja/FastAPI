# Exceptions can be handled like this


class TokenException(Exception):
    def __init__(self, name: str):
        self.name = name