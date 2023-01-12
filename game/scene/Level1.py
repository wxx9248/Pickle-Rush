# -*- coding: utf-8 -*-

import typing
import pygame.surface
from asset.AssetObjectFactory import AssetObjectFactory
from config.JSONConfigManager import JSONConfigManager
from core.object_model.Layer import Layer
from core.object_model.Scene import Scene
from core.object_model.Sprite import Sprite
from event.CustomEventTypes import CustomEventTypes
from game.atlas.MapAtlas import MapAtlas
from game.atlas.PlatformerPickleAtlas import PlatformerPickleAtlas, MotionControlEvents
from game.scene.GameLost import GameLost
from game.scene.GameWin import GameWin
from util import util
from core.object_model.Camera import Camera


class Level1(Scene):
    def __init__(self, size: typing.Tuple[int, int]):
        super().__init__(size)

        config_manager = JSONConfigManager("config.json", JSONConfigManager.BindingMode.DOUBLE)
        self.__is_show_collide_body = config_manager.get("config.show_collide_body")

        background_surface = pygame.Surface(self.size).convert_alpha()
        background_surface.fill(pygame.Color("white"))
        self.background["background"] = Sprite(background_surface)

        self.__map_atlas = MapAtlas(AssetObjectFactory().new_asset_object("asset.map.level.1"), 60)
        self.__map_atlas.position = (0, 0)
        self.__map_atlas.SHOW_COLLIDE_BODY = self.__is_show_collide_body
        map_layer = Layer(self.__map_atlas)

        self.__pickle_atlas = PlatformerPickleAtlas()
        self.__pickle_atlas.scale = (0.05, 0.05)
        self.__pickle_atlas.position = self.__map_atlas.grid_to_screen_position(
            pygame.Vector2(8, 10), self.__pickle_atlas.surface.get_size()
        )
        self.__pickle_atlas.acceleration_y = 0.1
        self.__pickle_atlas.RECT_MASK = True
        self.__pickle_atlas.SHOW_COLLIDE_BODY = self.__is_show_collide_body

        self.__camera = Camera((1280, 720), self.__pickle_atlas)
        self.__collide_mask_surface = None

        entity_layer = Layer(self.__pickle_atlas)
        self.layer_manager["map"] = map_layer
        self.layer_manager["entity"] = entity_layer

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
                self.__pickle_atlas.state_machine.next(pygame.event.Event(MotionControlEvents.EVENT_TOUCH_GROUND))
                self.__pickle_atlas.speed_y = 0
                self.__pickle_atlas.position_y = backup_pos_y

        collide_exit = self.__pickle_atlas.collides_mask(
            self.__map_atlas.exit_mask,
            pygame.Vector2(self.__map_atlas.position) - pygame.Vector2(self.__pickle_atlas.position)
        )

        if collide_exit:
            event = pygame.event.Event(CustomEventTypes.EVENT_STAGE_CHANGE_SCENE_REQUEST)
            event.scene = GameWin(self.size)
            pygame.event.post(event)

        collide_dead = self.__pickle_atlas.collides_mask(
            self.__map_atlas.dead_mask,
            pygame.Vector2(self.__map_atlas.position) - pygame.Vector2(self.__pickle_atlas.position)
        )

        if collide_dead:
            event = pygame.event.Event(CustomEventTypes.EVENT_STAGE_CHANGE_SCENE_REQUEST)
            event.scene = GameLost(self.size)
            pygame.event.post(event)

    def render(self, surface: pygame.surface.Surface):
        render_params = self.__camera.get_render_params()

        scene_canvas = pygame.Surface(self.__map_atlas.surface.get_size())
        self.layer_manager.render(scene_canvas)

        if self.__collide_mask_surface:
            scene_canvas.blit(self.__collide_mask_surface, self.__pickle_atlas.position)
            self.__collide_mask_surface = None

        surface.blit(scene_canvas, (0, 0), render_params)
