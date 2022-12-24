# -*- coding: utf-8 -*-
from config.AbstractConfig import AbstractConfig
from config.serializer.JSONConfigSerializer import JSONConfigSerializer


class JSONConfig(AbstractConfig):
    def __init__(self, file_path: str, binding_mode=AbstractConfig.BindingMode.DOUBLE):
        super().__init__(JSONConfigSerializer(), file_path, binding_mode)
