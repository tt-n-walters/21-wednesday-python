import arcade
import time

class Player(arcade.Sprite):
    def __init__(self, left, bottom):
        super().__init__("PNG/Characters/platformChar_idle.png")
        self.left = left
        self.bottom = bottom

        self.direction = "right"
        self.last_texture_change = 0        # When animation was last update
        self.texture_change_rate = 0.02        # How quickly to update animation
        self.texture_index = -1             # Which texture is being displayed

        # Standing still textures
        self.stand_right_texture, self.stand_left_texture = arcade.load_texture_pair("PNG/Characters/platformChar_idle.png")

        # Jumping texture
        self.jump_right_texture, self.jump_left_texture = arcade.load_texture_pair("PNG/Characters/platformChar_jump.png")
        
        # Walking textures
        walk_right_1, walk_left_1 = arcade.load_texture_pair("PNG/Characters/platformChar_walk1.png")
        walk_right_2, walk_left_2 = arcade.load_texture_pair("PNG/Characters/platformChar_walk2.png")

        self.walk_right_textures = [
            walk_right_1,
            walk_right_2
        ]
        self.walk_left_textures = [
            walk_left_1,
            walk_left_2
        ]
        
    # Code for updating everything about the player
    def update_animation(self, is_touching_ground):
        if is_touching_ground:      # jumping
            if self.direction == "right":
                self.texture = self.jump_right_texture
            elif self.direction == "left":
                self.texture = self.jump_left_texture

        elif self.change_x > 0:       # walking right
            self.direction = "right"
            if time.time() > self.last_texture_change + self.texture_change_rate:       # Check if enough time has passed
                self.last_texture_change = time.time()                                  # Save the current time
                self.texture_index += 1                                                 # Change to the next texture
                if self.texture_index >= len(self.walk_right_textures):                 # When we run out of textures, reset
                    self.texture_index = 0                                              #   back to the first

            self.texture = self.walk_right_textures[self.texture_index]

        elif self.change_x < 0:       # walking left
            self.direction = "left"
            if time.time() > self.last_texture_change + self.texture_change_rate:       # Check if enough time has passed
                self.last_texture_change = time.time()                                  # Save the current time
                self.texture_index += 1                                                 # Change to the next texture
                if self.texture_index >= len(self.walk_left_textures):                # When we run out of textures, reset
                    self.texture_index = 0                                              #   back to the first

            self.texture = self.walk_left_textures[self.texture_index]

        elif self.change_x == 0:      # stopped
            if self.direction == "right":
                self.texture = self.stand_right_texture
            elif self.direction == "left":
                self.texture = self.stand_left_texture

    
    def key_press(self, key, pressed):
        if pressed:
            if key == arcade.key.D:
                self.change_x += 8
            if key == arcade.key.A:
                self.change_x += -8
            if key == arcade.key.LEFT:
                self.change_angle = 4
            if key == arcade.key.RIGHT:
                self.change_angle = -4
        else:
            if key == arcade.key.D:
                self.change_x -= 8
            if key == arcade.key.A:
                self.change_x -= -8
            if key == arcade.key.LEFT:
                self.change_angle = 0
            if key == arcade.key.RIGHT:
                self.change_angle = 0