import arcade
from player import Player
from camera import Camera


class Platformer(arcade.Window):
    def __init__(self):
        super().__init__(600, 400, "Platformer", resizable=True, fullscreen=True)
        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.spawn_left = 88
        self.spawn_bottom = 600
        self.player = Player(self.spawn_left, self.spawn_bottom)
        self.camera = Camera(self.player.center_x, self.player.center_y, self.width, self.height)

        self.map = arcade.load_tilemap("map.tmj")
        self.ground = self.map.sprite_lists["Tile Layer 1"]
        self.objects = self.map.sprite_lists["Tile Layer 2"]

        self.physics = arcade.PhysicsEnginePlatformer(self.player, self.ground)
        self.draw_annoying_text = False

    def on_draw(self):
        arcade.set_viewport(*self.camera.get_coordinates())
        arcade.start_render()
        self.ground.draw()
        self.player.draw()
        self.objects.draw()
        if self.draw_annoying_text == True:
            arcade.draw_text(
                "CONGRATS YOU WON", self.camera.x, self.camera.y,
                arcade.color.RED, 100, self.camera.width, align="center", anchor_x="center")
    

    def on_update(self, delta_time):
        self.physics.update()
        # check fall off map
        if self.player.center_y < -400:
            self.player.left = self.spawn_left
            self.player.bottom = self.spawn_bottom
        
        if self.player.left < 0:
            self.player.left = 0
        
        # check end of level
        # if self.player.center_x >= 1960:
        #     self.player.left = self.spawn_left
        #     self.draw_annoying_text = True

        self.player.update_animation(self.physics.can_jump())
        # move the camera
        self.camera.x = self.player.center_x
        self.camera.y = self.player.center_y


    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.D:
            self.player.change_x = 6
        if symbol == arcade.key.A:
            self.player.change_x = -6
        if symbol == arcade.key.LEFT:
            self.player.change_angle = 4
        if symbol == arcade.key.RIGHT:
            self.player.change_angle = -4
        if symbol == arcade.key.SPACE:
            self.physics.jump(12)
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()
        if symbol == arcade.key.C:
            print(self.player.left, self.player.bottom)

        if symbol == arcade.key.K:
            self.camera.width *= 0.8
            self.camera.height *= 0.8
        if symbol == arcade.key.L:
            self.camera.width *= 1.2
            self.camera.height *= 1.2

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.D:
            self.player.change_x = 0
        if symbol == arcade.key.A:
            self.player.change_x = 0
        if symbol == arcade.key.LEFT:
            self.player.change_angle = 0
        if symbol == arcade.key.RIGHT:
            self.player.change_angle = 0
