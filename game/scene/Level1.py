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
from game.scene.Level2 import Level2


class Level1(Scene):
    def __init__(self, size: typing.Tuple[int, int]):
        super().__init__(size)

        config_manager = ConfigManager()
        self.__is_show_collide_body = config_manager.get("config.debug")

        ao = AssetObjectFactory()
        texture_dict = {
            Map.TileType.WALL: ao.new_asset_object("asset.sprite.level.1.tile.grass"),
            Map.TileType.DEAD: ao.new_asset_object("asset.sprite.level.1.tile.water")
        }

        self.background = Atlas(ao.new_asset_object("asset.sprite.level.1.background"))
        self.background.scale_to(size)

        self.__map_atlas = MapAtlas(AssetObjectFactory().new_asset_object("asset.map.level.1"), texture_dict, 60)
        self.__map_atlas.position = (0, 0)
        self.__map_atlas.SHOW_COLLIDE_BODY = self.__is_show_collide_body
        map_layer = Layer(self.__map_atlas)

        self.__pickle_atlas = PickleAtlasGravity()
        self.__pickle_atlas.scale = (0.05, 0.05)
        self.__pickle_atlas.position = self.__map_atlas.grid_to_screen_position(
            pygame.Vector2(8, 10), self.__pickle_atlas.surface.get_size()
        )
        self.__pickle_atlas.RECT_MASK = True
        self.__pickle_atlas.SHOW_COLLIDE_BODY = self.__is_show_collide_body

        self.__camera = Camera((1280, 720), self.__pickle_atlas,
                               self.__map_atlas.surface.get_size())
        self.__collide_mask_surface = None

        entity_layer = Layer(self.__pickle_atlas)
        self.layer_manager["map"] = map_layer
        self.layer_manager["scenery"] = self.init_scenery_layer()
        self.layer_manager["entity"] = entity_layer

        self.__scene_canvas = pygame.Surface(self.__map_atlas.surface.get_size(),
                                             pygame.SRCALPHA).convert_alpha()

        self.__sent_floor_collision_event = False

    def init_scenery_layer(self):
        ao = AssetObjectFactory()
        tower_sp: Sprite = ao.new_asset_object("asset.sprite.level.1.tower")
        tower_sp.image = pygame.transform.scale(tower_sp.surface, (220, 220))

        tree_sp: Sprite = ao.new_asset_object("asset.sprite.level.1.tree")
        tree_sp.image = pygame.transform.scale(tree_sp.surface, (60, 120))

        tower = Atlas(tower_sp)
        tower.position = self.__map_atlas.grid_to_screen_position(pygame.Vector2(9, 48),
                                                                  tower.surface.get_size())

        tree1 = Atlas(tree_sp)
        tree1.position = self.__map_atlas.grid_to_screen_position(pygame.Vector2(9, 10),
                                                                  tree1.surface.get_size())

        tree2 = Atlas(tree_sp)
        tree2.position = self.__map_atlas.grid_to_screen_position(pygame.Vector2(9, 21),
                                                                  tree2.surface.get_size())
        return Layer(tower, tree1, tree2)

    def update(self):
        backup_pos = self.__pickle_atlas.position
        backup_pos_x, backup_pos_y = backup_pos

        super().update()
        self.__pickle_atlas.update()

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
                    self.__pickle_atlas.accept_event(pygame.event.Event(CustomEventTypes.EVENT_LEVEL_1_COLLIDE_FLOOR))
                    self.__sent_floor_collision_event = True
        else:
            self.__sent_floor_collision_event = False

        collide_exit = self.__pickle_atlas.collides_mask(
            self.__map_atlas.exit_mask,
            pygame.Vector2(self.__map_atlas.position) - pygame.Vector2(self.__pickle_atlas.position)
        )
        if collide_exit:
            event = pygame.event.Event(CustomEventTypes.EVENT_STAGE_CHANGE_SCENE_REQUEST)
            event.scene = GameWin(self.size, Level2)
            pygame.event.post(event)

        collide_dead = self.__pickle_atlas.collides_mask(
            self.__map_atlas.dead_mask,
            pygame.Vector2(self.__map_atlas.position) - pygame.Vector2(self.__pickle_atlas.position)
        )
        if collide_dead:
            event = pygame.event.Event(CustomEventTypes.EVENT_STAGE_CHANGE_SCENE_REQUEST)
            event.scene = GameLost(self.size, self.__class__)
            pygame.event.post(event)

    def render(self, surface: pygame.surface.Surface):
        surface.blit(self.background.surface, (0, 0))
        render_params = self.__camera.get_render_params()
        self.__scene_canvas.fill((0, 0, 0, 0))
        self.layer_manager.render(self.__scene_canvas)
        surface.blit(self.__scene_canvas, (0, 0), render_params)
