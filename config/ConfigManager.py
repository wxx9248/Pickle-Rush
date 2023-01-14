# -*- coding: utf-8 -*-
from config.AbstractConfigManager import AbstractConfigManager
from config.JSONConfigManager import JSONConfigManager


class ConfigManager:
    __config_file_path = "config.json"
    __binding_mode = AbstractConfigManager.BindingMode.DOUBLE
    __instance = None

    @classmethod
    def set_config_file_path(cls, config_file_path: str):
        cls.__config_file_path = config_file_path

    @classmethod
    def set_binding_mode(cls, binding_mode: AbstractConfigManager.BindingMode):
        cls.__binding_mode = binding_mode

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = JSONConfigManager(cls.__config_file_path, cls.__binding_mode)

        return cls.__instance
