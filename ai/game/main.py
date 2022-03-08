from turtle import window_height
import arcade
import random
import os

rootdir = os.path.dirname(os.path.abspath(__file__))

class Game_Window(arcade.Window):
    def __init__(self):
        super().__init__(1280 , 720 , "Autonomous Moving Asteroid")

        Player.texture = arcade.load_texture(rootdir + "/player.png")
        Player.texture.image = Player.texture.image.rotate(-90)

        self.score = 0


        self.player = Player(self.width / 2 , self.height / 2)
        self.food = Food()
        self.food.set_random_position(self.width , self.height)

        self.pressed_keys = set()

    def on_draw(self):
        arcade.start_render()
        self.player.draw()
        self.food.draw()

    def on_key_press(self , symbol , modifiers):
        self.pressed_keys.add(symbol)

    def on_key_release(self , symbol , modifiers):
        self.pressed_keys.remove(symbol)

    def on_update(self, delta_time):
        self.player.update(self.pressed_keys)
        self.player.wrap_screen(self.width , self.height)
        if (self.player.collides_with_sprite(self.food)):
            self.food.set_random_position(self.width , self.height)
            self.score += 1
            print("score:" , self.score)
        

class Player(arcade.Sprite):
    def __init__(self , x , y ):
        super().__init__(texture=Player.texture)
        self.center_x = x
        self.center_y = y


    def update(self , pressed_keys):
        super().update()
        self.change_x = 0           # reset player speed
        self.change_y = 0

        if arcade.key.UP in pressed_keys or arcade.key.W in pressed_keys:
            self.forward(10)

        if arcade.key.DOWN in pressed_keys or arcade.key.S in pressed_keys:
            self.reverse(2)

        if arcade.key.LEFT in pressed_keys or arcade.key.D in pressed_keys:
            self.turn_left(4)

        if arcade.key.RIGHT in pressed_keys or arcade.key.A in pressed_keys:
            self.turn_right(4)

#the keys that work

    def wrap_screen(self , s_width , s_height):
        if self.left > s_width:
            self.right = 0
        elif self.right < 0:
            self.left = s_width

        if self.bottom > s_height:
            self.top = 0
        elif self.top < 0:
            self.bottom = s_height
#if go past the screen boundaries, appear again when the center has gone past the barrier

class Food(arcade.Sprite):
    def __init__(self):
        super().__init__(os.path.join(rootdir , "food.png"))

    def set_random_position(self , window_width , window_height):
        margin = 32
        self.center_x = random.randint(margin , window_width)
        self.center_y = random.randint(margin , window_height)




Game_Window()
arcade.run()