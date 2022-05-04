import arcade
from player import Player
from camera import Camera


class Platformer(arcade.Window):
    def __init__(self):
        super().__init__(600, 400, "Platformer", resizable=True, fullscreen=True, vsync=True)
        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.spawn_left = 88
        self.spawn_bottom = 600
        self.player = Player(self.spawn_left, self.spawn_bottom)
        self.camera = Camera(self.player.center_x, self.player.center_y, self.width, self.height)

        self.map = arcade.load_tilemap("map.tmj")
        self.ground = self.map.sprite_lists["Ground"]
        self.gems = self.map.sprite_lists["Gems"]
        self.spikes = self.map.sprite_lists["Spikes"]

        self.physics = arcade.PhysicsEnginePlatformer(self.player, self.ground)
        self.physics.gravity_constant = 0.8
        self.physics.jump_force = 14

        self.physics.enable_multi_jump(2)

        self.draw_annoying_text = False
        self.score = 0


    def on_draw(self):
        arcade.set_viewport(*self.camera.get_coordinates())
        arcade.start_render()
        self.ground.draw()
        self.player.draw()
        self.gems.draw()
        self.spikes.draw()

        arcade.draw_text(str(self.score), self.width - 100, self.height - 100, anchor_x="right", anchor_y="top")

        if self.draw_annoying_text == True:
            arcade.draw_text(
                "CONGRATS YOU WON", self.camera.x, self.camera.y,
                arcade.color.RED, 100, self.camera.width, align="center", anchor_x="center")
        

    

    def on_update(self, delta_time):
        self.physics.update()
        self.physics.can_jump()

        # check fall off map
        if self.player.center_y < -400:
            self.player.left = self.spawn_left
            self.player.bottom = self.spawn_bottom
        
        # invisible wall at start
        if self.player.left < 0:
            self.player.left = 0
        
        # check end of level
        # if self.player.center_x >= 1960:
        #     self.player.left = self.spawn_left
        #     self.draw_annoying_text = True

        spike_collisions = arcade.check_for_collision_with_list(self.player, self.spikes)
        if spike_collisions:
            self.player.left = self.spawn_left
            self.player.bottom = self.spawn_bottom
        
        gem_collisions = arcade.check_for_collision_with_list(self.player, self.gems)
        for gem in gem_collisions:
            gem.kill()


        self.player.update_animation(self.physics.jumps_since_ground)
        # move the camera
        self.camera.x = self.player.center_x
        self.camera.y = self.player.center_y


    def on_key_press(self, symbol, modifiers):
        self.player.key_press(symbol, True)
        if symbol == arcade.key.SPACE and self.physics.can_jump():
            self.physics.jump(self.physics.jump_force)
            
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()
        if symbol == arcade.key.C:
            print(self.player.left, self.player.bottom)



    def on_key_release(self, symbol, modifiers):
        self.player.key_press(symbol, False)


    def on_mouse_press(self, x, y, button, modifers):
        self.player.center_x = x / self.width  * self.camera.width  + self.camera.x - self.camera.width  / 2
        self.player.center_y = y / self.height * self.camera.height + self.camera.y - self.camera.height / 2
        self.player.change_y = 0


    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y > 0:
            self.camera.width *= 0.8
            self.camera.height *= 0.8
        if scroll_y < 0:
            self.camera.width *= 1.2
            self.camera.height *= 1.2