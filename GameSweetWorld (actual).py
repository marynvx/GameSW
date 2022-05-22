import arcade


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Sweet world"

TILE_SCALING = 1
CHARACTER_SCALING = 0.6

COIN_SCALING = 0.5

PLAYER_X_SPEED = 5
PLAYER_Y_SPEED = 6

JUMP_MAX_HEIGHT = 140

PLAYER_SPRITE_IMAGE_CHANGE_SPEED = 30

WINIMAGE_SCALING = 1
GAMEOVER_SCALING = 1

ENEMY_SCALING = 0.5

LEFT_FACING = -1
RIGHT_FACING = 1

ENEMY_SPEED = 4


class gameSW(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.enemy_sprite = None
        self.enemy_list = None
        self.enemy_image_right = []
        self.enemy_image_left = []
        

        self.camera = None

        self.tile_map = None
        self.player_list = None

        self.player_sprite = None

        self.key_right_pressed = False
        self.key_left_pressed = False


        self.player_jump = False
        self.jump_start = None

        self.player_dx = PLAYER_X_SPEED
        self.player_dy = PLAYER_Y_SPEED

        self.collide = False
        self.gameover = False

        self.player_sprite_images = []
        self.player_sprite_images_left = []

        self.gui_camera = None
        self.score = 0


        self.win_text = None

        
       
    def setup(self):

        self.coin_sound = arcade.load_sound("Sound/CollectCoin.mp3")
        self.win_sound = arcade.load_sound("Sound/YouWin.mp3")
        self.gameover_sound = arcade.load_sound("Sound/GameOver.mp3")
        self.music_sound = arcade.load_sound("Sound/BGmusic.mp3")

        arcade.play_sound(self.music_sound)

        self.camera = arcade.Camera(self.width, self.height)

        self.enemy_list = arcade.SpriteList()
        image_enemy = "Pics/fire.png"
        self.enemy_sprite = arcade.Sprite(image_enemy, ENEMY_SCALING)
        self.enemy_sprite.center_x = 128
        self.enemy_sprite.center_y = 92
        self.enemy_list.append(self.enemy_sprite)

        self.enemy_sprite.initial_center_x = self.enemy_sprite.center_x
        self.enemy_sprite.facing_direction = 1



        self.player_list = arcade.SpriteList()
        image_source = "Pics/zefir1.png"

        win_image = "Pics/Win.png"
        self.win_text = arcade.Sprite(win_image, WINIMAGE_SCALING)
        self.win_text.center_x = 512
        self.win_text.center_y = 320

        gameover_image = "Pics/GameOver.png"
        self.gameover_text = arcade.Sprite(gameover_image, GAMEOVER_SCALING)
        self.gameover_text.center_x = 512
        self.gameover_text.center_y = 320

        self.coin_list = arcade.SpriteList(use_spatial_hash=True)

        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 92
        self.player_list.append(self.player_sprite)

        for i in range(1, 3):
            self.player_sprite_images.append(arcade.load_texture(f"Pics/zefir{i}.png"))
        for i in range(2, 0, -1):
            self.player_sprite_images_left.append(arcade.load_texture(f"Pics/zefir{i}.png", flipped_horizontally=True))

        self.player_sprite_image_standing = arcade.load_texture(f"Pics/zefir_standing.png")
        self.player_sprite_image_jump = arcade.load_texture(f"Pics/zefir_jump.png")

        
            
        self.jump_start = self.player_sprite.center_x


        map_name = f"NewSweetMapDay/bigmap.json"

        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,

            "Coins": {
                "use_spatial_hash": True,
            }
            }
        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)


        self.scene = arcade.Scene.from_tilemap(self.tile_map)

       
        self.gui_camera = arcade.Camera(self.width, self.height)
        self.score = 0

        


    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        if screen_center_x > 1024:
            screen_center_x = 1024
        if screen_center_y > 640:
            screen_center_y = 640
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)


    def win(self):
            if self.score == 17:
                self.score = "all"
                arcade.play_sound(self.win_sound)

    def on_draw(self):
        self.clear()
        self.scene["BG"].draw()
        self.scene["Platforms"].draw()
        self.scene["Coins"].draw()


        self.coin_list.draw()
        self.enemy_list.draw()
        self.player_list.draw()
        

        self.gui_camera.use()
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            610,
            arcade.csscolor.WHITE,
            18,
        )

        if self.score == "all":
            self.win_text.draw()

        if self.gameover == True:
            self.gameover_text.draw()
            
        self.camera.use()

        
    

        
    def coin_collision(self):

        for coi in self.scene["Coins"]:
            if (self.player_sprite.center_x + self.player_sprite.width / 2 >= coi.center_x - coi.width / 2 and self.player_sprite.center_x - self.player_sprite.width / 2 <= coi.center_x + coi.width / 2) \
                    and (self.player_sprite.center_y + self.player_sprite.height / 2 >= coi.center_y - coi.height / 2 and self.player_sprite.center_y - self.player_sprite.height / 2 <= coi.center_y + coi.height / 2):
                coi.remove_from_sprite_lists()
                self.score += 1
                arcade.play_sound(self.coin_sound)
               


    def calculate_collision(self):

        for block in self.scene["Platforms"]:
            if (self.player_sprite.center_x + self.player_sprite.width / 2 >= block.center_x - block.width / 2 and self.player_sprite.center_x - self.player_sprite.width / 2 <= block.center_x + block.width / 2) \
                    and (self.player_sprite.center_y + self.player_sprite.height / 2 >= block.center_y - block.height / 2 and self.player_sprite.center_y - self.player_sprite.height / 2 <= block.center_y + block.height / 2):
                self.collide = True    

        
    def enemy_collision(self):

        if (self.player_sprite.center_x + self.player_sprite.width / 2 >= self.enemy_sprite.center_x - self.enemy_sprite.width / 2 and self.player_sprite.center_x - self.player_sprite.width / 2 <= self.enemy_sprite.center_x + self.enemy_sprite.width / 2) \
                    and (self.player_sprite.center_y + self.player_sprite.height / 2 >= self.enemy_sprite.center_y - self.enemy_sprite.height / 2 and self.player_sprite.center_y - self.player_sprite.height / 2 <= self.enemy_sprite.center_y + self.enemy_sprite.height / 2):
                self.player_sprite.remove_from_sprite_lists()
                self.gameover = True
                arcade.play_sound(self.gameover_sound)



    def on_update(self, delta_time: float):

        self.center_camera_to_player()

        self.player_movement()
        if self.player_jump:
            self.collide = False
        else:
            self.calculate_collision()
    
        self.coin_collision()

        self.enemy_movement()
        
        self.enemy_collision()

        self.win()

        

    def player_movement(self):
        if self.collide:
            self.player_dy = 0
        else:
            self.player_dx = PLAYER_X_SPEED
            self.player_dy = PLAYER_Y_SPEED

        if self.key_right_pressed:
            self.player_sprite.center_x += self.player_dx
            self.player_sprite.texture = self.player_sprite_images[int(self.player_sprite.center_x / PLAYER_SPRITE_IMAGE_CHANGE_SPEED) % 2]
            
        if self.key_left_pressed:
            self.player_sprite.center_x -= self.player_dx
            self.player_sprite.texture = self.player_sprite_images_left[int(self.player_sprite.center_x / PLAYER_SPRITE_IMAGE_CHANGE_SPEED) % 2]

        if self.player_jump:
            self.player_sprite.center_y += self.player_dy
            if self.player_sprite.center_y > self.jump_start + JUMP_MAX_HEIGHT:
                self.player_jump = False
        else:
            self.player_sprite.center_y -= self.player_dy


    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.key_right_pressed = True
        elif key == arcade.key.LEFT:
            self.key_left_pressed = True
        elif key == arcade.key.UP:
            self.player_jump = True
            self.jump_start = self.player_sprite.center_y
            self.player_sprite.texture = self.player_sprite_image_jump

    def on_key_release(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.key_right_pressed = False
            self.player_sprite.texture = self.player_sprite_image_standing
        elif key == arcade.key.LEFT:
            self.key_left_pressed = False
            self.player_sprite.texture = self.player_sprite_image_standing
        elif key == arcade.key.UP:
            self.player_sprite.change_y = 0
            self.player_sprite.texture = self.player_sprite_image_standing


    def enemy_movement(self):

        if self.enemy_sprite.center_x > self.enemy_sprite.initial_center_x + 2000:
            self.enemy_sprite.facing_direction = LEFT_FACING
        if self.enemy_sprite.center_x < self.enemy_sprite.initial_center_x - 200:
            self.enemy_sprite.facing_direction = RIGHT_FACING
        self.enemy_sprite.center_x += ENEMY_SPEED * self.enemy_sprite.facing_direction



def main():
    window = gameSW()
    window.setup()
    arcade.run()
    

if __name__ == "__main__":
    main()