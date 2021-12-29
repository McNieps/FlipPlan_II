class ProjectileHandler:
    def __init__(self):
        self.projectile_list = []

    def add_projectile(self, projectile):
        self.projectile_list.append(projectile)

    def handle_movements(self, delta):
        for projectile in self.projectile_list:
            projectile.update(delta)

    def check_and_remove_projectile(self):
        index_to_remove = []
        for i in range(len(self.projectile_list)):
            if self.projectile_list[i].number_of_hit_left <= 0:
                index_to_remove.append(i)
        index_to_remove.reverse()
        for i in index_to_remove:
            self.projectile_list.pop(i).death_function()
