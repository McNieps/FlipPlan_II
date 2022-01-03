from flipplan.game_objects.projectiles.missile import Missile


class MissileLauncher:
    def __init__(self, linked_plane, arena_handler):
        self.arena_handler = arena_handler
        self.ressource_handler = self.arena_handler.ressource_handler

        # Weapon metadata
        self.linked_plane = linked_plane

        self.missiles_capacity = self.ressource_handler.fetch_data(["weapons", "missile_launcher", "capacity"])
        self.missiles_quantity = self.missiles_capacity
        self.missiles_recover_time = self.ressource_handler.fetch_data(["weapons", "missile_launcher", "recover_time"])

        # Projectile metadata
        self.projectile = Missile
        self.projectile_handler = self.arena_handler.projectile_handler
        self.speed_absorption_ratio = self.ressource_handler.fetch_data(["weapons", "missile_launcher", "speed_absorption_ratio"])

        # Weapon state
        self.missile_linked = None
        self.has_fired = False
        self.missiles_current_cooldown = 0

    def trigger_down(self):
        if self.missiles_quantity > 0:
            self.missiles_quantity -= 1
            self.shoot()
            self.has_fired = True

    def trigger_pressed(self, delta):
        if self.missile_linked:
            linked_plane_x = self.linked_plane.x
            linked_plane_y = self.linked_plane.y
            dv = self.ressource_handler.fetch_data(["projectiles", "missile", "acceleration"]) * self.speed_absorption_ratio * delta
            self.missile_linked.set_position(linked_plane_x, linked_plane_y, False, False)
            self.linked_plane.set_speed(dv, 0)
            self.missile_linked.a = self.linked_plane.a
            self.missile_linked.vx = self.linked_plane.vx
            self.missile_linked.vy = self.linked_plane.vy

    def trigger_up(self):
        self.missile_linked = None

    def reset(self, delta):
        if not self.has_fired:
            if self.missiles_quantity < self.missiles_capacity:
                self.missiles_current_cooldown += delta
                if self.missiles_current_cooldown > self.missiles_recover_time:
                    self.missiles_quantity += 1
                    if self.missiles_quantity == self.missiles_capacity:
                        self.missiles_current_cooldown = 0
                    else:
                        self.missiles_current_cooldown -= self.missiles_recover_time

        self.has_fired = False

    def shoot(self):
        initial_pos = (self.linked_plane.x, self.linked_plane.y)
        initial_speed = (self.linked_plane.vx, self.linked_plane.vy)
        initial_a = self.linked_plane.a

        projectile = self.projectile(self.arena_handler,
                                     self.linked_plane.player_number,
                                     initial_pos,
                                     initial_speed,
                                     initial_a)

        self.projectile_handler.add_projectile(projectile)
        self.missile_linked = projectile
