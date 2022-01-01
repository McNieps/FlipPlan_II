import pygame

from flipplan.engine.handlers.ressource_handler import RessourceHandler


# Pre_init
ressource_handler = RessourceHandler()
ressource_handler.pre_init()    # load data

pygame.mixer.pre_init(44100, -16, 1, 512)

# Initilisation
pygame.init()
pygame.mixer.set_num_channels(ressource_handler.fetch_data(["system", "audio", "number_of_channels"]))

# Creation de la fenetre
if ressource_handler.fetch_data(["system", "window", "scaled"]):
    window = pygame.display.set_mode(ressource_handler.fetch_data(["system", "window", "size"]), pygame.SCALED)
else:
    window = pygame.display.set_mode(ressource_handler.fetch_data(["system", "window", "size"]))

# Chargement images et sons
ressource_handler.init()

# Cosmetique fenetre
pygame.display.set_caption(ressource_handler.fetch_data(["system", "window", "name"]))
if ressource_handler.fetch_data(["system", "window", "icon"]):
    icon = ressource_handler.images["icon"]
    pygame.display.set_icon(icon)

# Si on veut lancer ce script
if __name__ == "__main__":
    marche = True
    while marche:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                marche = False

    pygame.quit()
