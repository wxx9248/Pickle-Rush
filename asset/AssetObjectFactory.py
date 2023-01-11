# -*- coding: utf-8 -*-
import logging
import os
import typing

import pygame.image

from core.object_model.Sound import Sound
from core.object_model.Sprite import Sprite
from core.object_model.Text import Text
from core.object_model.Map import Map


class AssetObjectFactory:
    ASSET_DIRS = ("asset/images", "asset/sounds", "asset/texts")
    ASSET_PROPS = {
        "asset/images/pickle-0.png": {"key": "asset.sprite.pickle.0"},
        "asset/images/pickle-1.png": {"key": "asset.sprite.pickle.1"},
        "asset/images/pickle-2.png": {"key": "asset.sprite.pickle.2"},
        "asset/images/senior-pickle.png": {"key": "asset.sprite.senior-pickle"},
        "asset/images/bacteria.png": {"key": "asset.sprite.bacteria"},
        "asset/texts/menu-logo.json": {"key": "asset.text.menu.logo"},
        "asset/texts/menu-start.json": {"key": "asset.text.menu.start"},
        "asset/texts/menu-exit.json": {"key": "asset.text.menu.exit"},
        "asset/texts/menu-cursor.json": {"key": "asset.text.menu.cursor"},
        "asset/texts/gamelost-text.json": {"key": "asset.text.gamelost.text"},
        "asset/texts/gamewin-text.json": {"key": "asset.text.gamewin.text"},
        "asset/maps/level-0.csv": {"key": "asset.map.level.0"}
    }

    __asset_id_path_dict = {value["key"]: key for key, value in ASSET_PROPS.items()}
    __instance = None

    def __new__(cls, *args, **kwargs):
        def init(instance):
            instance.__logger = logging.getLogger(instance.__class__.__name__)

            instance.__logger.info("Scanning asset directories")
            asset_file_paths = []
            for target_dir in AssetObjectFactory.ASSET_DIRS:
                instance.__logger.debug(f"Scanning {target_dir}")
                asset_file_paths.extend([os.path.join(directory, file)
                                         for directory, _, filenames in os.walk(target_dir)
                                         for file in filenames])

            instance.__logger.debug(f"Scan result: {asset_file_paths}")

            for path in asset_file_paths:
                path not in AssetObjectFactory.ASSET_PROPS and instance.__logger.warning(
                    f"Asset {path} is not assigned with an key, thus not addressable with asset manager"
                )

        if cls.__instance is None:
            cls.__instance = super(AssetObjectFactory, cls).__new__(cls)
            init(cls.__instance)

        return cls.__instance

    def new_asset_object(self, asset_key: str, *args, **kwargs) -> typing.Any:
        self.__logger.debug(f"Creating asset object with asset key {asset_key}")
        fields = asset_key.split('.')
        namespace = fields[0]
        asset_type = fields[1]

        if namespace != "asset":
            self.__logger.warning(f"Not an asset key. Object not created")
            return

        if asset_type == "sprite":
            self.__logger.debug("Creating a sprite object")
            return Sprite(pygame.image.load(AssetObjectFactory.__asset_id_path_dict[asset_key]), *args, **kwargs)
        if asset_type == "sound":
            self.__logger.debug("Creating a sound object")
            return Sound(AssetObjectFactory.__asset_id_path_dict[asset_key], *args, **kwargs)
        if asset_type == "text":
            self.__logger.debug("Creating a text object")
            return Text(AssetObjectFactory.__asset_id_path_dict[asset_key], *args, **kwargs)
        if asset_type == "map":
            self.__logger.debug("Creating a map object")
            return Map(AssetObjectFactory.__asset_id_path_dict[asset_key], *args, **kwargs)

        self.__logger.debug(f"Unknown asset type {asset_type}. Object not created")
        return

