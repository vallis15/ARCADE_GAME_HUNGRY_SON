import arcade
from functions import MyGame, Player, Coin, Broccoli
from media import player_image, coin_image, broccoli_image, coin_sound_file, broccoli_hit_sound_file, font_file

def main():
    game = MyGame(player_image, coin_image, broccoli_image, coin_sound_file, broccoli_hit_sound_file, font_file)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
