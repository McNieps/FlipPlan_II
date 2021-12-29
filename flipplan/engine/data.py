from json import load as json_load

json_file = open("../assets/data/data.json", "r")
game_dict = json_load(json_file)
json_file.close()

SCREEN_SIZE = game_dict["window"]["size"]
MAX_FPS = game_dict["system"]["fps"]
IFI = game_dict["system"]["IFI"]        # Nombre de calculs interframe
