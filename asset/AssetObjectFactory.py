# -*- coding: utf-8 -*-
import logging
import os
import typing

import pygame.image

from core.ImageObject import ImageObject
from core.SoundObject import SoundObject


class AssetObjectFactory:
    ASSET_DIRS = ("asset/images", "asset/sounds")
    ASSET_PROPS = {
    }

    __asset_id_path_dict = {value["id"]: key for key, value in ASSET_PROPS.items()}

    def __init__(self):
        self.__logger = logging.getLogger(self.__class__.__name__)

        self.__logger.info("Scanning asset directories")
        asset_file_paths = []
        for target_dir in AssetObjectFactory.ASSET_DIRS:
            self.__logger.debug(f"Scanning {target_dir}")
            asset_file_paths.extend([os.path.join(directory, file)
                                     for directory, _, filenames in os.walk(target_dir)
                                     for file in filenames])

        self.__logger.debug(f"Scan result: {asset_file_paths}")

        for path in asset_file_paths:
            path not in AssetObjectFactory.ASSET_PROPS and self.__logger.warning(
                f"Asset {path} is not assigned with an ID, thus not addressable with asset manager"
            )

    def new_asset_object(self, asset_id: str) -> typing.Any:
        self.__logger.debug(f"Creating asset object with asset ID {asset_id}")
        fields = asset_id.split('.')
        namespace = fields[0]
        asset_type = fields[1]

        if namespace != "asset":
            self.__logger.warning(f"Not an asset ID. Object not created")
            return

        if asset_type == "image":
            self.__logger.debug("Creating an image object")
            return ImageObject(pygame.image.load(AssetObjectFactory.__asset_id_path_dict[asset_id]))
        if asset_type == "sound":
            self.__logger.debug("Creating an sound object")
            return SoundObject(AssetObjectFactory.__asset_id_path_dict[asset_id])

        self.__logger.debug("Unknown asset type. Object not created")
        return
