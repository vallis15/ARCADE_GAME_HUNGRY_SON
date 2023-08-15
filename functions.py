import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 8
COIN_COUNT = 0

class Player(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT


class Coin(arcade.Sprite):
    def __init__(self, filename, scale):
        super().__init__(filename, scale)
        self.visible_timer = 0.0

    def update(self):
        self.visible_timer += 1 / 60

        if self.visible_timer >= 3.0:
            self.remove_from_sprite_lists()


class Broccoli(arcade.Sprite):
    def __init__(self, filename, scale):
        super().__init__(filename, scale)
        self.visible_timer = 0.0

    def update(self):
        self.visible_timer += 1 / 60

        if self.visible_timer >= 3.0:
            self.remove_from_sprite_lists()


class MyGame(arcade.Window):
    def __init__(self, player_image, coin_image, broccoli_image, coin_sound_file, broccoli_hit_sound_file, font_file):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "My son on the hunt")

        self.all_sprites = arcade.SpriteList()
        self.coins = arcade.SpriteList()
        self.player = None
        self.score = 0

        self.coin_spawn_timer = 2.0
        self.coin_spawn_timer_elapsed = 0.0

        self.next_coin_spawn_delay = 1.0

        self.coin_sound = arcade.load_sound(coin_sound_file)
        self.broccoli_hit_sound = arcade.load_sound(broccoli_hit_sound_file)

        self.game_over = False
        self.timer = 60

        self.timer_text = f"Time left: {int(self.timer)}"

        self.player_image = player_image
        self.coin_image = coin_image
        self.broccoli_image = broccoli_image
        self.font_file = font_file

    def setup(self):
        self.player = Player(self.player_image, 0.13)
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.all_sprites.append(self.player)

        for _ in range(COIN_COUNT):
            coin = Coin(self.coin_image, 0.27)
            coin.center_x = random.randint(0, SCREEN_WIDTH)
            coin.center_y = random.randint(0, SCREEN_HEIGHT)
            self.all_sprites.append(coin)
            self.coins.append(coin)

        for _ in range(0):
            broccoli = Broccoli(self.broccoli_image, 0.15)
            broccoli.center_x = random.randint(0, SCREEN_WIDTH)
            broccoli.center_y = random.randint(0, SCREEN_HEIGHT)
            self.all_sprites.append(broccoli)
            self.coins.append(broccoli)

    def on_draw(self):
        arcade.start_render()
        self.all_sprites.draw()
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, SCREEN_HEIGHT - 20, arcade.color.WHITE, 26)

        # Draw the timer text
        arcade.draw_text(self.timer_text, SCREEN_WIDTH - 150, SCREEN_HEIGHT - 30, arcade.color.WHITE, 20)

        if self.game_over:
            game_over_text = f"END OF THE GAME. YOUR SCORE IS {self.score}"
            text_width = len(game_over_text) * 12
            start_x = (SCREEN_WIDTH - text_width) // 2
            start_y = SCREEN_HEIGHT // 2
            font_name = self.font_file
            font_size = 16
            bold = False

            arcade.draw_text(game_over_text, start_x, start_y, arcade.color.WHITE, font_size, font_name=font_name, bold=bold)

    def update(self, delta_time):
        if not self.game_over:
            self.all_sprites.update()

            self.coin_spawn_timer_elapsed += delta_time
            if self.coin_spawn_timer_elapsed >= self.coin_spawn_timer:
                self.spawn_new_coin()
                self.coin_spawn_timer_elapsed = 0.0

            for coin in self.coins:
                coin.update()

            coins_hit = arcade.check_for_collision_with_list(self.player, self.coins)
            for coin in coins_hit:
                if isinstance(coin, Broccoli):
                    self.score -= 1
                    arcade.play_sound(self.broccoli_hit_sound)
                else:
                    self.score += 1
                    arcade.play_sound(self.coin_sound)
                coin.remove_from_sprite_lists()

            self.timer -= delta_time
            if self.timer <= 0:
                self.timer = 0
                self.game_over = True

            self.timer_text = f"Time left: {int(self.timer)}"

    def spawn_new_coin(self):
        coin_type = random.choice(["regular", "broccoli"])

        if coin_type == "regular":
            coin = Coin(self.coin_image, 0.27)
        else:
            coin = Broccoli(self.broccoli_image, 0.15)

        coin.center_x = random.randint(0, SCREEN_WIDTH)
        coin.center_y = random.randint(0, SCREEN_HEIGHT)
        self.all_sprites.append(coin)
        self.coins.append(coin)

        self.next_coin_spawn_delay = random.uniform(1.0, 2.0)

        self.coin_spawn_timer_elapsed = 0.0

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player.change_y = PLAYER_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -PLAYER_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
