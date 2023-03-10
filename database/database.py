import json

import game


class Database:
    def __init__(self):
        self.__is_loaded = False
        self.__data = {}

    def load(self):
        if self.__is_loaded:
            return
        self.__is_loaded = True
        with open("./database/db.json", 'r') as f:
            self.__data = json.load(f)
        print("Database is loaded!")
        return self

    def save(self):
        game.GameWindow.database.set_data("fx_volume", game.fx_volume)
        game.GameWindow.database.set_data("music_volume", game.music_volume)
        if not self.__is_loaded:
            return
        with open("./database/db.json", 'w') as f:
            f.write(json.dumps(self.__data))
        self.__is_loaded = False
        return self

    def get_data(self, tag):
        return self.__data[tag]

    def set_data_dict(self, tag: str, new_data: dict):
        new_list = []
        for item in self.__data[tag]:
            if list(new_data.keys())[0] != list(item.keys())[0]:
                new_list.append(item)
        self.__data[tag] = [*new_list, new_data]

    def set_data_primitive(self, tag: str, new_data):
        self.__data[tag] = new_data

    def set_data(self, tag: str, new_data):
        if game.GameConstants.DEBUG_MODE:
            return
        if type(new_data) == dict:
            return self.set_data_dict(tag, new_data)
        else:
            return self.set_data_primitive(tag, new_data)
