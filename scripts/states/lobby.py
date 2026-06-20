import pygame
import random
import numpy

from pygame.locals import *  # type: ignore

from scripts import common, utils, filehandling, color
from scripts.states.basestate import State, StateID, StateSwitch
from scripts.sprites.sprites import *

class Lobby(State):
    is_gamemode = False
    desc = "At the lobby..."

    def prepare_assets(self):
        self.assets_raw = [
            "assets/img/bg/",
            "assets/img/sprites/",
        ]

        self.sounds_raw = {
            "supadood": "assets/music/supadood.wav",
            "explode": "assets/sfx/explode.wav",
            "getTrash": "assets/sfx/getTrash.wav",
            "noTrash": "assets/sfx/noTrash.wav",
        }

    def prepare_next_states(self):
        self.is_reloadable = False
        self.next_states = [
            StateID.SHOP,
            StateID.CATASTROPHE,
            StateID.SCOREBOARD,
        ]

    def prepare_sprites(self):
        lay1 = BackgroundLayer(static_image_path=utils.newPath("assets/img/bg/sky1.png"))
        lay2 = BackgroundLayer(static_image_path=utils.newPath("assets/img/bg/sky2.png"))
        lay3 = BackgroundLayer(static_image_path=utils.newPath("assets/img/bg/sky3.png"))

        self.background = ParallaxBackground(lay3, lay2, lay1)

        self.stat_score = Statistic(pos=(5, 10))
        self.stat_score.set_icon(utils.newPath("assets/img/ui/coin.png"), (0, 0))
        self.stat_score.set_text(str(self.shared_state_data.get('score', 0)), (20, 0))

        self.temp_ground = WorldObject(
            static_image_path=utils.newPath(f"assets/img/bg/sand.png"),
            size=(common.SCREEN_WIDTH*3, int(common.SCREEN_HEIGHT-common.GROUND_HEIGHT)),
            pos=(-common.SCREEN_WIDTH, common.GROUND_HEIGHT)
        )
        self.temp_ground.set_worldobj(
            desc="ground",
            interactable=False,
            collidable=True
        )
        self.temp_ground.image = utils.multiply_image(
            common.ASSET_DICT.get(utils.newPath("assets/img/bg/sand.png")),
            self.temp_ground.image.size,
            self.temp_ground.size
        )
        self.temp_ground.callibrate()

        self.temp_platform = WorldObject(
            static_image_path=utils.newPath(f"assets/img/bg/grass.png"),
            size=(50, 50),
            pos=(common.GROUND_HEIGHT-50, 50)
        )
        self.temp_platform.set_worldobj(
            desc="platform",
            interactable=False,
            collidable=True
        )
        self.temp_platform.image = utils.multiply_image(
            input_image=self.temp_platform.image,
            tile_size=(6, 20),
            target_size=self.temp_platform.size
        )
        self.temp_platform.callibrate()

        self.collidables: RGroup[WorldObject] = RGroup(
            self.temp_ground,
            self.temp_platform
        )

        self.player = Player(
            pos=((common.SCREEN_WIDTH-24)/2, common.GROUND_HEIGHT-50),
        )
        self.player.set_collidables(self.collidables)

        self.interactables_map: dict[str, list] = {
            "Shop": [20, StateID.SHOP, (55, 58), "explode"],
            "Score": [120, StateID.SCOREBOARD, (47, 43), "noTrash"],
            "Play": [220, StateID.CATASTROPHE, (35, 33), "getTrash"]
        }
        self.interactables: RGroup[WorldObject] = RGroup()
        for name, stuff in self.interactables_map.items():
            d = WorldObject(
                static_image_path=utils.newPath(f"assets/img/ui/{name}.png"),
                pos=(stuff[0], (common.GROUND_HEIGHT - stuff[2][1])),
                size=stuff[2],
            )
            d.set_worldobj(
                desc=name,
                interactable=True,
                collidable=True
            )
            self.interactables.add(d)

        self.clouds_group = RGroup()
        self.trees_group = RGroup()

        self.clouds_map = [(random.uniform(-0.5, 0.5)*self.temp_ground.size[0], random.uniform(-10, 10) + common.CLOUD_HEIGHT) for _ in range(25)]
        for pos in self.clouds_map:
            d = WorldObject(
                sheet_path=utils.newPath(f"assets/img/bg/clouds.json"),
                pos=pos,
                size=(15, 15),
            )
            d.set_worldobj(
                desc="cloud",
                interactable=False,
                collidable=False
            )
            d.image = d.sheet.states[d.sheet.current_state][random.randint(0, 2)]
            d.image.set_alpha(random.randint(200, 225))
            self.clouds_group.add(d)

        self.trees_map = [(random.uniform(0, 1)*self.temp_ground.size[0], (common.GROUND_HEIGHT-random.uniform(51, 61))) for _ in range(15)]
        for pos in self.trees_map:
            d = WorldObject(
                static_image_path=utils.newPath(f"assets/img/bg/tree.png"),
                pos=pos,
                size=(23, 61),
            )
            d.set_worldobj(
                desc="tree",
                interactable=False,
                collidable=False
            )
            self.trees_group.add(d)

        self.map_group = RGroup(self.clouds_group, self.trees_group, self.interactables, self.collidables)
        self.map_vel = pygame.Vector2()

    def load_sprites(self):
        self.sprites.add(
            self.background,
            self.map_group,
            self.player,
            self.stat_score,
        )

    def load_assets(self):
        common.SOUND_MANAGER.bgm.play("supadood", -1)

    def logic(self):
        self.stat_score.set_text(str(self.shared_state_data.get('score', 0)))

        for cloud in self.clouds_group:
            if cloud.pos.x >= self.temp_ground.rect.right:
                cloud.move_to((self.temp_ground.rect.left, cloud.pos.y))
            cloud.velocity.x = random.uniform(0, 10)

        if (self.key[K_LEFT] or self.key[K_a]):
            self.map_vel.x -= self.player.acceleration.x if abs(self.map_vel.x) < self.player.max_velocity.x else 0
        elif (self.key[K_RIGHT] or self.key[K_d]):
            self.map_vel.x += self.player.acceleration.x if abs(self.map_vel.x) < self.player.max_velocity.x else 0
        else:
            self.map_vel.x = 0

        if (self.key[K_UP] or self.key[K_w]):
            self.player.jump()

        # crude cam implementation, will change later
        self.map_vel.y = pygame.math.lerp(self.map_vel.y, self.player.velocity.y, 0.5)

        if not self.player.is_colliding:
            self.player.move_to((self.player.old_pos.x, self.player.pos.y))
            self.map_group.move_ip(-self.map_vel*self.dt)
            self.background.move_parallax(self.map_vel*self.dt, 10)

        collided_sprite = pygame.sprite.spritecollideany(self.player, self.interactables, None)

        if isinstance(collided_sprite, WorldObject) and collided_sprite.interactable and self.key[K_RETURN]:
            print("interacted with an interactable worldobject")

            # in each of these checks we could do something special like play a sound effect.
            # it's kinda hardcoded rn but i'll change it later
            common.SOUND_MANAGER.sfx.play(self.interactables_map[collided_sprite.desc][3])

            raise StateSwitch(self.interactables_map[collided_sprite.desc][1], self.shared_state_data)
