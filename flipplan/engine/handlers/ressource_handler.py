import pygame

from json import load as json_load
from random import choice


class RessourceHandler:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.data = {}

    def pre_init(self):
        self.load_data()

    def init(self):
        self.load_sounds()
        self.load_images()

    def load_data(self):
        data_index_file = open("../assets/data/data_index.json")
        data_index_dict = json_load(data_index_file)
        data_index_file.close()

        self.extract_data_dictionary(data_index_dict, "../assets/data/")

    def load_sounds(self):
        sound_json_file = open("../assets/sounds/sound_index.json")
        sound_json_dict = json_load(sound_json_file)
        sound_json_file.close()

        self.extract_sound_dictionary(sound_json_dict, "../assets/sounds/")

    def load_images(self):
        image_json_file = open("../assets/images/image_index.json")
        image_json_dict = json_load(image_json_file)
        image_json_file.close()

        self.extract_image_dictionary(image_json_dict, "../assets/images/")

    def extract_data_dictionary(self, dictionary, path, receiving_dict=None):
        if receiving_dict is None:
            receiving_dict = self.data

        for key in dictionary:
            if type(dictionary[key]) == str:
                data_file = open(path+dictionary[key])
                receiving_dict[key] = json_load(data_file)
                data_file.close()
            else:
                new_path = path + key + "/"
                receiving_dict[key] = {}
                self.extract_data_dictionary(dictionary[key], new_path, receiving_dict[key])

    def extract_sound_dictionary(self, dictionary, path, receiving_dict=None):
        if receiving_dict is None:
            receiving_dict = self.sounds

        for key in dictionary:
            if type(dictionary[key]) == str:
                receiving_dict[key] = pygame.mixer.Sound(path+dictionary[key])
                receiving_dict[key].set_volume(0.05)
            else:
                new_path = path + key + "/"
                receiving_dict[key] = {}
                self.extract_sound_dictionary(dictionary[key], new_path, receiving_dict[key])

    def extract_image_dictionary(self, dictionary, path, receiving_dict=None):
        if receiving_dict is None:
            receiving_dict = self.images

        for key in dictionary:
            if type(dictionary[key]) == str:
                receiving_dict[key] = pygame.image.load(path+dictionary[key]).convert_alpha()

            else:
                new_path = path + key + "/"
                receiving_dict[key] = {}
                self.extract_image_dictionary(dictionary[key], new_path, receiving_dict[key])

    def play_sound(self, keys=(), channel=None):
        if channel:
            channel.play(self.fetch_sound(keys))
            return None
        return self.fetch_sound(keys).play()

    def fetch_sound(self, keys=()):
        sub_dict = self.sounds
        for key in keys:
            if type(sub_dict[key]) == dict:
                sub_dict = sub_dict[key]
            else:
                return sub_dict[key]

        while True:
            keys = list(sub_dict.keys())
            key = choice(keys)
            if type(sub_dict[key]) == dict:
                sub_dict = sub_dict[key]
            else:
                return sub_dict[key]

    def fetch_data(self, keys=()):
        sub_dict = self.data
        for key in keys:
            sub_dict = sub_dict[key]
        return sub_dict


if __name__ == '__main__':
    from flipplan.engine.handlers.loop_handler import LoopHandler

    loop_handler = LoopHandler(120)
    ressources_handler = RessourceHandler()

    while loop_handler.is_running():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop_handler.stop_loop()
            if event.type == pygame.KEYDOWN:
                ressources_handler.play_sound(["misc", "misc_2"])

        if pygame.key.get_pressed()[pygame.K_RETURN]:
            ressources_handler.play_sound(["misc", "misc_2"])
            pass

        pygame.display.flip()
    pygame.quit()
