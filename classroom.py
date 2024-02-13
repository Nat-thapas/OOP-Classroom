import logging

class Classroom():
    def __init__(self, name: str, section: str, subject: str, room: str):
        self.__name: str = name
        self.__section: str = section
        self.__subject: str = subject
        self.__room: str = room
