# -*- coding: utf-8 -*-

import typing

import pygame.surface

from asset.AssetObjectFactory import AssetObjectFactory
from config.ConfigManager import ConfigManager
from core.object_model.Atlas import Atlas
from core.object_model.Camera import Camera
from core.object_model.Layer import Layer
from core.object_model.Map import Map
from core.object_model.Scene import Scene
from core.object_model.Sprite import Sprite
from event.CustomEventTypes import CustomEventTypes
from game.atlas.MapAtlas import MapAtlas
from game.atlas.PickleAtlasGravity import PickleAtlasGravity
from game.scene.GameLost import GameLost
from game.scene.GameWin import GameWin
from game.atlas.BacteriaAtlasGravity import BacteriaAtlasGravity
from game.atlas.BossAtlas import BossAtlas
from util.PatrolNavigator import PatrolNavigator
from game.atlas.BulletAtlas import BulletAtlas


class Level2(Scene):
    def __init__(self, size: typing.Tuple[int, int]):
        super().__init__(size)

        config_manager = ConfigManager()
        self.__is_show_collide_body = config_manager.get("config.debug")

        ao = AssetObjectFactory()
        texture_dict = {
            Map.TileType.WALL: ao.new_asset_object("asset.sprite.level.1.tile.grass"),
            Map.TileType.DEAD: ao.new_asset_object("asset.sprite.level.1.tile.water")
        }

        heart = ao.new_asset_object("asset.sprite.heart")
        heart = pygame.transform.scale(heart.surface, (50, 50))

        self.__scene_assets = {
            "heart": heart
        }

        self.__ui_atlases = []
        self.__entity_layer = Layer()

        # setting dynamically spawned entities' layer
        self.__enemy_layer = Layer()
        self.__bullets_layer = Layer()
        self.__enemy_bullets_layer = Layer()

        self.__spawned_store = {"enemies": [], "bullets": [], "enemy_bullets": []}
        self.__enemy_layer.set_atlas_list(self.__spawned_store["enemies"])
        self.__bullets_layer.set_atlas_list(self.__spawned_store["bullets"])
        self.__enemy_bullets_layer.set_atlas_list(self.__spawned_store["enemy_bullets"])

        self.background = Atlas(ao.new_asset_object("asset.sprite.level.1.background"))
        self.background.scale_to(size)

        self.__map_atlas = MapAtlas(AssetObjectFactory().new_asset_object("asset.map.level.2"),
                                    texture_dict, 60)
        self.__map_atlas.position = (0, 0)
        self.__map_atlas.SHOW_COLLIDE_BODY = self.__is_show_collide_body
        map_layer = Layer(self.__map_atlas)

        self.__pickle_atlas = PickleAtlasGravity(self.__spawned_store["bullets"])
        self.__pickle_atlas.scale = (0.05, 0.05)
        self.__pickle_atlas.position = self.__map_atlas.grid_to_screen_position(
            pygame.Vector2(8, 10), self.__pickle_atlas.surface.get_size()
        )
        self.__pickle_atlas.RECT_MASK = True
        self.__pickle_atlas.SHOW_COLLIDE_BODY = self.__is_show_collide_body

        self.__camera = Camera((1280, 720), self.__pickle_atlas,
                               self.__map_atlas.surface.get_size())
        self.__collide_mask_surface = None

        self.__level_boss = BossAtlas(self.__spawned_store["enemies"],
                                      self.__spawned_store["enemy_bullets"], self.__map_atlas)
        self.__level_boss.position = (1100, 100)
        self.__level_boss.spawn_new_enemy()

        self.__entity_layer.add_atlas(self.__pickle_atlas)
        self.__entity_layer.add_atlas(self.__level_boss)

        self.layer_manager["map"] = map_layer
        self.layer_manager["scenery"] = self.init_scenery_layer()
        self.layer_manager["entity"] = self.__entity_layer
        self.layer_manager["enemy"] = self.__enemy_layer
        self.layer_manager["bullet"] = self.__bullets_layer
        self.layer_manager["enemy_bullet"] = self.__enemy_bullets_layer

        self.__scene_canvas = pygame.Surface(self.__map_atlas.surface.get_size(),
                                             pygame.SRCALPHA).convert_alpha()

        self.__sent_floor_collision_event = False

    def init_scenery_layer(self):
        ao = AssetObjectFactory()
        tree_sp: Sprite = ao.new_asset_object("asset.sprite.level.1.tree")
        tree_sp.image = pygame.transform.scale(tree_sp.surface, (60, 120))

        tree1 = Atlas(tree_sp)
        tree1.position = self.__map_atlas.grid_to_screen_position(pygame.Vector2(9, 10),
                                                                  tree1.surface.get_size())

        tree2 = Atlas(tree_sp)
        tree2.position = self.__map_atlas.grid_to_screen_position(pygame.Vector2(9, 15),
                                                                  tree2.surface.get_size())
        return Layer(tree1, tree2)

    def garbage_collect(self):
        map_size = self.__map_atlas.surface.get_size()
        for bullet in self.__spawned_store["bullets"]:
            bullet: BulletAtlas
            if bullet.position_x > map_size[0] or \
                    bullet.position_x < 0 or \
                    bullet.position_y > map_size[1] or \
                    bullet.position_y < 0:
                self.__spawned_store["bullets"].remove(bullet)

        for bc in self.__spawned_store["enemies"]:
            bc: BacteriaAtlasGravity
            if bc.hp <= 0:
                self.__spawned_store["enemies"].remove(bc)

    def bullet_collide(self):
        for bullet in self.__spawned_store["bullets"]:
            bullet: BulletAtlas

            # collide with bacteria
            for bc in self.__spawned_store["enemies"]:
                bc: BacteriaAtlasGravity

                is_collide = bc.mask.overlap(
                    bullet.mask, pygame.Vector2(bullet.position) - pygame.Vector2(bc.position))
                if is_collide:
                    bc.hp -= bullet.damage
                    self.__spawned_store["bullets"].remove(bullet)
                    break

            # collide with level boss
            is_collide = bullet.mask.overlap(self.__level_boss.mask,
                                             pygame.Vector2(
                                                 self.__level_boss.position) - pygame.Vector2(
                                                 bullet.position))
            if is_collide:
                self.__level_boss.hp -= bullet.damage
                self.__spawned_store["bullets"].remove(bullet)

    def enemy_bullet_collide(self):
        for bullet in self.__spawned_store["enemy_bullets"]:
            bullet: BulletAtlas

            is_collide = bullet.mask.overlap(
                self.__pickle_atlas.mask,
                pygame.Vector2(self.__pickle_atlas.position) - pygame.Vector2(
                    bullet.position)
            )

            if is_collide:
                self.__pickle_atlas.hit(bullet.damage)
                self.__spawned_store["enemy_bullets"].remove(bullet)

    def enemy_collide(self):
        for bc in self.__spawned_store["enemies"]:
            bc: BacteriaAtlasGravity

            if not bc.first_touch_ground:
                backup_pos = bc.position
                backup_pos_x, backup_pos_y = backup_pos

                bc.update()

                is_collide_wall = bc.mask.overlap(
                    self.__map_atlas.wall_mask,
                    pygame.Vector2(self.__map_atlas.position) - pygame.Vector2(
                        bc.position)
                )

                if is_collide_wall:
                    bc.first_touch_ground = True
                    bc.acceleration = (0, 0)
                    bc.speed = (0, 0)
                    bc.position_x = backup_pos_x
                    bc.position_y = backup_pos_y

    def pickle_collide(self):
        backup_pos = self.__pickle_atlas.position
        backup_pos_x, backup_pos_y = backup_pos

        super().update()
        self.__pickle_atlas.update()

        # collide with wall
        collide_mask = self.__pickle_atlas.mask.overlap_mask(
            self.__map_atlas.wall_mask,
            pygame.Vector2(self.__map_atlas.position) - pygame.Vector2(self.__pickle_atlas.position)
        )
        if collide_mask.count():
            x, y = collide_mask.centroid()

            pickle_size_x, pickle_size_y = self.__pickle_atlas.surface.get_size()

            # colliding left
            if self.__pickle_atlas.speed_x < 0 and x < (pickle_size_x / 2) - 1:
                self.__pickle_atlas.speed_x = 0
                self.__pickle_atlas.position_x = backup_pos_x

            # colliding right
            if self.__pickle_atlas.speed_x > 0 and x > (pickle_size_x / 2) + 1:
                self.__pickle_atlas.speed_x = 0
                self.__pickle_atlas.position_x = backup_pos_x

            # colliding floor wall
            if self.__pickle_atlas.speed_y >= 0 and y > (pickle_size_y / 2):
                self.__pickle_atlas.speed_y = 0
                self.__pickle_atlas.position_y = backup_pos_y
                if not self.__sent_floor_collision_event:
                    self.__pickle_atlas.accept_event(
                        pygame.event.Event(CustomEventTypes.EVENT_LEVEL_1_COLLIDE_FLOOR))
                    self.__sent_floor_collision_event = True
        else:
            self.__sent_floor_collision_event = False

        collide_dead = self.__pickle_atlas.collides_mask(
            self.__map_atlas.dead_mask,
            pygame.Vector2(self.__map_atlas.position) - pygame.Vector2(
                self.__pickle_atlas.position)
        )
        if collide_dead:
            event = pygame.event.Event(CustomEventTypes.EVENT_STAGE_CHANGE_SCENE_REQUEST)
            event.scene = GameLost(self.size, self.__class__)
            pygame.event.post(event)

        # collide with enemy
        for bc in self.__spawned_store["enemies"]:
            bc: BacteriaAtlasGravity

            is_collide = self.__pickle_atlas.mask.overlap(
                bc.mask,
                pygame.Vector2(bc.position) - pygame.Vector2(
                    self.__pickle_atlas.position)
            )

            if is_collide:
                self.__pickle_atlas.hit(bc.damage)

    def update(self):
        self.pickle_collide()
        self.enemy_collide()
        self.bullet_collide()
        self.enemy_bullet_collide()
        self.garbage_collect()

        if self.__level_boss.hp <= 0:
            event = pygame.event.Event(CustomEventTypes.EVENT_STAGE_CHANGE_SCENE_REQUEST)
            event.scene = GameWin(self.size, None)
            pygame.event.post(event)

        if self.__pickle_atlas.hp <= 0:
            event = pygame.event.Event(CustomEventTypes.EVENT_STAGE_CHANGE_SCENE_REQUEST)
            event.scene = GameLost(self.size, self.__class__)
            pygame.event.post(event)

    def render_ui(self, surface: pygame.surface.Surface):
        hp = self.__pickle_atlas.hp
        heart_img = self.__scene_assets["heart"]
        offset = heart_img.get_size()[0]
        for i in range(hp):
            surface.blit(heart_img, (offset * i, 0))

    def render(self, surface: pygame.surface.Surface):
        surface.blit(self.background.surface, (0, 0))
        render_params = self.__camera.get_render_params()
        self.__scene_canvas.fill((0, 0, 0, 0))
        self.layer_manager.render(self.__scene_canvas)
        surface.blit(self.__scene_canvas, (0, 0), render_params)
        self.render_ui(surface)
