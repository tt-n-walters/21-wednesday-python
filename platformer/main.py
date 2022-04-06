import arcade
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from platformer import Platformer

Platformer()
arcade.run()
