import arcade


class SingleHitBlock:
    def __init__(self, sprite):
        self.sprite = sprite
        self.collided_with = False
    
    def collides(self, player):
        if self.sprite.sprite_lists:
            is_colliding = arcade.check_for_collision(self.sprite, player)

            is_below = player.top <= self.sprite.center_y
            is_above = player.bottom >= self.sprite.center_y
            is_left = player.right <= self.sprite.center_x
            is_right = player.left >= self.sprite.center_x

            is_moving_up = player.change_y > 0
            is_moving_down = player.change_y < 0
            is_moving_left = player.change_x < 0
            is_moving_right = player.change_x > 0

            if is_colliding:
                print(is_below, is_moving_up)

                if is_below and is_moving_up:
                    player.change_y = 0
                    player.top = self.sprite.bottom
                    return True
                if is_above and is_moving_down:
                    player.change_y = 0
                    player.bottom = self.sprite.top
                if is_left and is_moving_right:
                    player.right = self.sprite.left
                if is_right and is_moving_left:
                    player.left = self.sprite.right


