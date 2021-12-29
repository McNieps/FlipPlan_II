import pygame

from json import load as json_load


class RessourceHandler:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.load_sounds()
        self.load_images()

    def load_sounds(self):
        sound_json_file = open("../assets/sounds/sound_index.json")
        sound_json_dict = json_load(sound_json_file)
        sound_json_file.close()

        self.extract_sound_dictionary(sound_json_dict, "../assets/sounds/")
        print(self.sounds)

    def extract_sound_dictionary(self, dictionary, path, receiving_dict=None):
        if receiving_dict is None:
            receiving_dict = self.sounds

        for key in dictionary:
            if type(dictionary[key]) == str:
                receiving_dict[key] = pygame.mixer.Sound(path+dictionary[key])

            else:
                new_path = path + key + "/"
                receiving_dict[key] = {}
                self.extract_sound_dictionary(dictionary[key], new_path, receiving_dict[key])

    def load_images(self):
        image_json_file = open("../assets/images/image_index.json")
        image_json_dict = json_load(image_json_file)
        image_json_file.close()

        self.extract_image_dictionary(image_json_dict, "../assets/images/")
        print(self.images)

    def extract_image_dictionary(self, dictionary, path, receiving_dict=None):
        if receiving_dict is None:
            receiving_dict = self.images

        for key in dictionary:
            if type(dictionary[key]) == str:
                print(path+dictionary[key])
                receiving_dict[key] = pygame.image.load(path+dictionary[key]).convert_alpha()

            else:
                new_path = path + key + "/"
                receiving_dict[key] = {}
                self.extract_image_dictionary(dictionary[key], new_path, receiving_dict[key])


if __name__ == '__main__':
    from src.engine.window import window
    x = RessourceHandler()
