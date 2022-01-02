from flipplan.game_objects.projectiles.abstract_bullet import AbstractBullet


class RayBullet(AbstractBullet):
    def __init__(self, arena_handler, player_number, initial_pos, initial_speed, initial_a):
        super().__init__(arena_handler, player_number, initial_pos, initial_speed, initial_a)

        # Projectile image
        self.original_image = self.ressource_handler.images["projectiles"]["ray_bullet"]
        self.update_image_rect_mask()
